import asyncio
import json
import secrets
import select
import socket
import time
import uuid
from typing import Type

from websockets.asyncio.client import ClientConnection, connect

from .covers import bandcamp_music_cover, yt_music_cover


class MpvDiscordRpc:
    def __init__(self, websocket: ClientConnection, sock: socket.socket) -> None:
        self.pid: int | None = None
        self.url: str | None = None
        self.start: float | None = None
        """In milliseconds"""
        self.end: float | None = None
        """In milliseconds"""
        self.name: str | None = None
        self.artist: str | None = None
        self.playlist: str | None = None
        """Playlist path"""
        self.playlist_current: int | None = None
        self.playlist_count: int | None = None
        self.cover: str | None = None
        """URL"""
        self.album: str | None = None
        self.version: str | None = None
        self.paused: bool = False

        self._websocket: ClientConnection = websocket
        self._socket: socket.socket = sock
        self._created_at: float = time.time() * 1000
        """In milliseconds"""
        self._requests: int = 0
        """Total requests count, increased every request"""
        self._first_run: bool = False

    async def mainloop(self) -> None:
        if not self._first_run:
            self.test_paused()
            self.update_mpv()
            self._first_run = True
        while True:
            start_time: float = time.time()
            """Time where this tick was started"""
            ready: list[socket.socket] = select.select([self._socket], [], [], 5)[0]
            if ready:
                self.handle_event()
            self.test_paused()
            self.update_mpv()
            await self.update_discord()
            time.sleep(max((start_time + 5 - time.time(), 0)))

    def handle_event(self) -> None:
        events: list[bytes] = self._socket.recv(4096).split(b"\n")
        for raw in events:
            if raw:
                data: dict = json.loads(raw)
                print("->", data)
                if "event" in data and data["event"] == "file-loaded":
                    self.update_mpv()

    def update_mpv(self) -> None:
        self.pid = self.mpv_request("pid", int)
        self.url = self.mpv_request("metadata/by-key/Comment", str)
        if current_time_s := self.mpv_request("time-pos", float):
            self.start = (time.time() - current_time_s) * 1000
        if remaining_time_s := self.mpv_request("time-remaining", float):
            self.end = (time.time() + remaining_time_s) * 1000
        self.name = self.mpv_request("media-title", str)
        self.artist = self.mpv_request("metadata/by-key/Artist", str)
        self.playlist = self.mpv_request("playlist-path", str)
        self.playlist_current = self.mpv_request("playlist-pos", int)
        self.playlist_count = self.mpv_request("playlist/count", int)
        self.cover = self.get_cover()
        self.album = self.mpv_request("metadata/by-key/Album", str)
        self.version = self.mpv_request("mpv-version", str)

    def test_paused(self) -> None:
        self.paused = self.mpv_request("core-idle", bool) or False

    def get_cover(self) -> str | None:
        if self.url is None:
            return None
        elif "youtube" in self.url:
            return yt_music_cover(self.url)
        elif "bandcamp" in self.url:
            return bandcamp_music_cover(self.url)
        else:
            return None

    def mpv_request[V](self, field: str, expected_type: Type[V]) -> V | None:
        payload: bytes = (
            json.dumps(
                {
                    "command": ["get_property", field],
                    "request_id": self._requests,
                }
            )
            + "\n"
        ).encode()
        print("<=", payload)
        self._socket.send(payload)
        request_id: int = -1
        data: dict = {"data": None}
        while request_id != self._requests:
            events = self._socket.recv(2**16).split(b"\n")
            for event in events:
                if not event:
                    continue
                data = json.loads(event)
                print("=>", data)
                if "request_id" in data:
                    request_id = data["request_id"]
                    break
                elif "event" in data and data["event"] == "file-loaded":
                    self.update_mpv()
        if "error" in data and data["error"] != "success":
            return None
        self._requests += 1
        assert isinstance(data["data"], expected_type)
        return data["data"]

    @classmethod
    async def run(cls) -> None:
        async with connect("ws://127.0.0.1:6463", ping_timeout=None) as websocket:
            dispatch = await websocket.recv()
            print(">", dispatch)
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                sock.connect("/tmp/mpv.sock")
                instance: MpvDiscordRpc = cls(websocket, sock)
                await instance.mainloop()

    async def update_discord(self) -> None:
        activity_data: dict = {
            "cmd": "SET_ACTIVITY",
            "args": {
                "activity": {
                    "name": "mpv",
                    "type": 2,  # 2
                    "created_at": self._created_at,
                    "timestamps": {},
                    "application_id": "1393273649016082472",
                    "emoji": {
                        "name": "mpvlogo128",
                        "id": "1393306728849739908",
                        "animated": False,
                    },
                    "party": {},
                    "assets": {
                        "small_image": "mpv-gradient",
                    },
                    "secrets": {
                        "join": secrets.token_hex(20),
                        "spectate": secrets.token_hex(20),
                        "match": secrets.token_hex(20),
                    },
                    "flags": 0,  # IDK tbh
                },
            },
            "nonce": str(uuid.uuid4()),
        }
        buttons: list[dict] = []
        if self.paused:
            buttons.append(
                {
                    "label": "Paused",
                    "url": "#",
                }
            )
        if self.pid:
            activity_data["args"]["pid"] = self.pid
        if self.url:
            activity_data["args"]["activity"]["url"] = self.url
            buttons.append(
                {
                    "label": (
                        "Listen on YouTube"
                        if "youtube" in self.url
                        else "Listen online"
                    ),
                    "url": self.url,
                }
            )
        if not self.paused and self.start:
            activity_data["args"]["activity"]["timestamps"]["start"] = self.start
        if not self.paused and self.end:
            activity_data["args"]["activity"]["timestamps"]["end"] = self.end
        if self.name:
            activity_data["args"]["activity"]["details"] = self.name
        if self.artist:
            activity_data["args"]["activity"]["state"] = self.artist
        if self.playlist:
            activity_data["args"]["activity"]["party"]["id"] = self.playlist
        if self.playlist_current and self.playlist_count:
            activity_data["args"]["activity"]["party"]["size"] = [
                self.playlist_current,
                self.playlist_count,
            ]
        if self.cover:
            activity_data["args"]["activity"]["assets"]["large_image"] = self.cover
        if self.album:
            activity_data["args"]["activity"]["assets"]["large_text"] = self.album
        if self.version:
            activity_data["args"]["activity"]["assets"]["small_text"] = self.version
        if buttons:
            activity_data["args"]["activity"]["buttons"] = buttons

        activity_json: str = json.dumps(activity_data)
        print("<", activity_json)
        await self._websocket.send(activity_json)
        answer = await self._websocket.recv()
        print(">", answer)


def main() -> None:
    asyncio.run(MpvDiscordRpc.run())
