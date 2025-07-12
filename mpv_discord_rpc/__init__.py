import asyncio
import json
import secrets
import socket
import time
import uuid

import requests
from websockets.asyncio.client import connect


async def run() -> None:
    mpv_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    mpv_socket.connect("/tmp/mpv.sock")

    async with connect("ws://127.0.0.1:6463", ping_timeout=None) as websocket:
        dispatch = await websocket.recv()
        print(dispatch)
        music_name = "Loading..."
        music_artist = "Loading..."
        music_album = "Loading..."
        playlist_current = 0
        playlist_count = 1
        current_time_s = 0
        remaining_time_s = 0
        playlist_path = "..."
        music_url = "https://www.youtube.com/"
        mpv_pid = 0
        mpv_version = "?"
        cover_url = ""

        request_id = 0
        requests_ids = {
            "media-title": 0,
            "playlist/count": 0,
            "playlist-pos": 0,
            "metadata/by-key/Artist": 0,
            "metadata/by-key/Album": 0,
            "metadata/by-key/Comment": 0,
            "time-pos": 0,
            "time-remaining": 0,
            "playlist-path": 0,
            "pid": 0,
            "mpv-version": 0,
        }
        while True:
            activity_data: str = json.dumps(
                {
                    "cmd": "SET_ACTIVITY",
                    "args": {
                        "pid": mpv_pid,
                        "activity": {
                            "name": "mpv",
                            "type": 2,  # 2
                            "url": music_url,
                            "created_at": time.time() * 1000,
                            "timestamps": {
                                "start": (time.time() - current_time_s)
                                * 1000,  # MPV music start time
                                "end": (time.time() + remaining_time_s)
                                * 1000,  # MPV music end time
                            },
                            "application_id": "1393273649016082472",
                            "details": music_name,  # Music name
                            "state": music_artist,  # Music artist
                            "emoji": {
                                "name": "mpvlogo128",
                                "id": "1393306728849739908",
                                "animated": False,
                            },
                            "party": {
                                "id": playlist_path,
                                "size": [playlist_current, playlist_count],
                            },
                            "assets": {
                                "large_image": cover_url,
                                "large_text": music_album,
                                "small_image": "mpv-gradient",
                                "small_text": mpv_version,
                            },
                            "secrets": {
                                "join": secrets.token_hex(20),
                                "spectate": secrets.token_hex(20),
                                "match": secrets.token_hex(20),
                            },
                            "flags": 0,  # IDK tbh
                            "buttons": [
                                {
                                    "label": "Listen on YouTube",
                                    "url": music_url,
                                },
                            ],
                        },
                    },
                    "nonce": str(uuid.uuid4()),
                }
            )

            data = b""
            char = b""
            while char != b"\n":
                char = mpv_socket.recv(1)
                data += char
                if char == "":
                    break
            parsed = json.loads(data)
            print(parsed)
            if parsed.get("event", "") == "file-loaded":
                request_id = secrets.randbelow(2**16)
                mpv_socket.send(
                    (
                        json.dumps(
                            {
                                "command": [
                                    "get_property",
                                    "media-title",
                                    "playlist/count",
                                ],
                                "request_id": request_id,
                            }
                        )
                        + "\n"
                    ).encode()
                )
                for property_name in requests_ids:
                    requests_ids[property_name] = secrets.randbelow(2**16)
                    mpv_socket.send(
                        (
                            json.dumps(
                                {
                                    "command": ["get_property", property_name],
                                    "request_id": requests_ids[property_name],
                                }
                            )
                            + "\n"
                        ).encode()
                    )
            elif parsed.get("request_id", -1) in requests_ids.values():
                key = next(
                    key
                    for key, value in requests_ids.items()
                    if value == parsed["request_id"]
                )
                if "error" in parsed and parsed["error"] != "success":
                    print(f"whoopsie {parsed['error']} for {key}")

                    if key == "metadata/by-key/Album":
                        music_album = ""

                    continue
                print(f"FOUND {parsed['data']}")
                if key == "media-title":
                    music_name = parsed["data"]
                elif key == "playlist/count":
                    playlist_count = int(parsed["data"])
                elif key == "playlist-pos":
                    playlist_current = int(parsed["data"])
                elif key == "metadata/by-key/Artist":
                    music_artist = parsed["data"]
                elif key == "metadata/by-key/Album":
                    music_album = parsed["data"]
                elif key == "metadata/by-key/Comment":
                    music_url = parsed["data"]
                    ytid = music_url.split("?v=")[-1]

                    try:
                        cover_url = requests.post(
                            "https://music.youtube.com/youtubei/v1/player?prettyPrint=false",
                            json={
                                "videoId": ytid,
                                "context": {
                                    "client": {
                                        "hl": "fr",
                                        "gl": "FR",
                                        "remoteHost": "2a01:e0a:5e7:9340:d90f:a928:c59a:e986",
                                        "deviceMake": "",
                                        "deviceModel": "",
                                        "visitorData": "CgtzMlY0LWY5azFVdyj0w8bDBjInCgJGUhIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiAh",
                                        "userAgent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0,gzip(gfe)",
                                        "clientName": "WEB_REMIX",
                                        "clientVersion": "1.20250709.03.01",
                                        "osName": "X11",
                                        "osVersion": "",
                                        "originalUrl": "https://music.youtube.com/",
                                        "platform": "DESKTOP",
                                        "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                                        "configInfo": {
                                            "appInstallData": "CPTDxsMGEIuvzxwQvYqwBRCQvM8cELfq_hIQmZixBRDlrs8cEParsAUQ4riwBRDM364FEMvAzxwQiZeAExCqnc8cEJT-sAUQ8J3PHBD2us8cELWwzxwQpLbPHBCJsM4cELnZzhwQn6HPHBCwhs8cELjkzhwQvbauBRDa984cEMn3rwUQ_LLOHBDevM4cEIqCgBMQiIewBRCXtc8cELvZzhwQ4OD_EhCBzc4cEJ7QsAUQhsDPHBCZjbEFEMW7zxwQ8OLOHBCThs8cEL2czxwQ0rbPHBCYuc8cENPhrwUQvZmwBRCCoM8cEIjjrwUQ6rvPHBDuoM8cENeczxwQh6zOHBCAl88cEP6OzxwqKENBTVNHaFVSb0wyd0ROSGtCdUhkaFFyTDNBNnZpQWF2MndhTldoMEg%3D",
                                            "coldConfigData": "CPXDxsMGGjJBT2pGb3gxTUVZZDVGamlyZThUVXphT3l6QlZXd3l4SnRmUGE3TlQxUG5seEphOUZ5QSIyQU9qRm94MTVvbDJlSHJVc3lnTDFvb002YXF0czJyVGdJcXQxSTd0cThvNmppbnUyZmc%3D",
                                            "coldHashData": "CPXDxsMGEhM4MzcyMjg4Nzg1MDY2MDg0NzkyGPXDxsMGMjJBT2pGb3gxTUVZZDVGamlyZThUVXphT3l6QlZXd3l4SnRmUGE3TlQxUG5seEphOUZ5QToyQU9qRm94MTVvbDJlSHJVc3lnTDFvb002YXF0czJyVGdJcXQxSTd0cThvNmppbnUyZmc%3D",
                                            "hotHashData": "CPXDxsMGEhM0ODM0MDgxNTExNDAyNjgwMTA2GPXDxsMGMjJBT2pGb3gxTUVZZDVGamlyZThUVXphT3l6QlZXd3l4SnRmUGE3TlQxUG5seEphOUZ5QToyQU9qRm94MTVvbDJlSHJVc3lnTDFvb002YXF0czJyVGdJcXQxSTd0cThvNmppbnUyZmc%3D",
                                        },
                                        "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                                        "timeZone": "Europe/Paris",
                                        "browserName": "Firefox",
                                        "browserVersion": "140.0",
                                        "acceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                        "deviceExperimentId": "ChxOelV5TlRrM05EVXlNVFkzTkRjNU5Ua3dNQT09EPTDxsMGGPTDxsMG",
                                        "rolloutToken": "CJzO7rat4OzVygEQr4uzyPbXjQMY_OSAup21jgM%3D",
                                        "screenWidthPoints": 1349,
                                        "screenHeightPoints": 617,
                                        "screenPixelDensity": 1,
                                        "screenDensityFloat": 1,
                                        "utcOffsetMinutes": 120,
                                        "playerType": "UNIPLAYER",
                                        "tvAppInfo": {
                                            "livingRoomAppMode": "LIVING_ROOM_APP_MODE_UNSPECIFIED"
                                        },
                                        "clientScreen": "WATCH_FULL_SCREEN",
                                    },
                                    "user": {"lockedSafetyMode": False},
                                    "request": {
                                        "useSsl": True,
                                        "consistencyTokenJars": [
                                            {
                                                "encryptedTokenJarContents": "AKreu9vGJvh9GzxuQ81FzAo70zR1kbtoBwBMwnjJXKluHq-ghNDdhhskWwkQjns-W5tj2RU2kk2Ldgc48MkIU6LXwPJUheySf0waSizGkY8tXeeS34t07Q9JVJbO9s6s1KR8elNgoCEG6-LMkhbx4a4d"
                                            }
                                        ],
                                        "internalExperimentFlags": [],
                                    },
                                    "clientScreenNonce": "zYFx0JyL5kImjtZD",
                                    "adSignalsInfo": {
                                        "params": [
                                            {"key": "dt", "value": "1752277495708"},
                                            {"key": "flash", "value": "0"},
                                            {"key": "frm", "value": "0"},
                                            {"key": "u_tz", "value": "120"},
                                            {"key": "u_his", "value": "2"},
                                            {"key": "u_h", "value": "1200"},
                                            {"key": "u_w", "value": "1600"},
                                            {"key": "u_ah", "value": "1200"},
                                            {"key": "u_aw", "value": "1600"},
                                            {"key": "u_cd", "value": "24"},
                                            {"key": "bc", "value": "31"},
                                            {"key": "bih", "value": "617"},
                                            {"key": "biw", "value": "1349"},
                                            {
                                                "key": "brdim",
                                                "value": "0,0,0,0,1600,0,1600,1156,1349,617",
                                            },
                                            {"key": "vis", "value": "1"},
                                            {"key": "wgl", "value": "true"},
                                            {"key": "ca_type", "value": "image"},
                                        ]
                                    },
                                    "clickTracking": {
                                        "clickTrackingParams": "CP8DEMjeAiITCLKIk6z-tY4DFYfuSQcdgekAjw=="
                                    },
                                },
                                "playbackContext": {
                                    "contentPlaybackContext": {
                                        "html5Preference": "HTML5_PREF_WANTS",
                                        "lactMilliseconds": "29",
                                        "referer": "https://music.youtube.com/",
                                        "signatureTimestamp": 20278,
                                        "autonavState": "STATE_OFF",
                                        "autoCaptionsDefaultOn": False,
                                        "mdxContext": {},
                                        "vis": 10,
                                    },
                                    "devicePlaybackCapabilities": {
                                        "supportsVp9Encoding": True,
                                        "supportXhr": True,
                                    },
                                },
                                "cpn": "s5r09cveqj9AF0hT",
                                "playlistId": "RDAMVMeeMC0SG2cnA",
                                "captionParams": {},
                                "serviceIntegrityDimensions": {
                                    "poToken": "MlsTL8zoXUnQHhMXgcKyJpn8uF3kIpkEvmPiIDvX6cXsAaQKrIdaNyEZ9dw4IpS6i_6d7Htuu7Rv2sEmPpFGYnLIgN68z5D0KUtUKqe2JrbeFaNi_4FoCs4Ul76M"
                                },
                            },
                        ).json()["videoDetails"]["thumbnail"]["thumbnails"][-1]["url"]
                    except Exception as e:
                        print(e)

                        cover_url = f"https://img.youtube.com/vi/{ytid}/0.jpg"
                elif key == "time-pos":
                    current_time_s = int(parsed["data"])
                elif key == "time-remaining":
                    remaining_time_s = int(parsed["data"])
                elif key == "pid":
                    mpv_pid = int(parsed["data"])
                elif key == "playlist-path":
                    playlist_path = parsed["data"]
                elif key == "mpv-version":
                    mpv_version = parsed["data"]
            elif parsed.get("event", "") == "playback-restart":
                await websocket.send(activity_data)
                answer = await websocket.recv()
                print(answer)


def main():
    asyncio.run(run())
