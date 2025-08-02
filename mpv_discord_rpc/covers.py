import traceback
from html.parser import HTMLParser

import requests


class MyHTMLParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.cover: str | None = None
        self.is_cover_img: bool = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        print("Encountered a start tag:", tag)
        attrs_dict: dict[str, str | None] = {}
        for attr in attrs:
            attrs_dict[attr[0]] = attr[1]
        if (
            tag == "a"
            and attrs_dict.get("class", "") == "popupImage"
            and "https://f4.bcbits.com/img/a" in (attrs_dict.get("href", "") or "")
        ):
            self.cover = attrs_dict["href"]

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)


def bandcamp_music_cover(url: str) -> str | None:
    parser = MyHTMLParser()
    parser.feed(requests.get(url).text)
    return parser.cover


def yt_music_cover(ytb_url: str) -> str:
    ytid = ytb_url.split("?v=")[-1]
    try:
        raw = requests.post(
            "https://music.youtube.com/youtubei/v1/player?prettyPrint=false",
            json={
                "videoId": ytid,
                "context": {
                    "client": {
                        "hl": "fr",
                        "gl": "FR",
                        "remoteHost": "2a01:e0a:5e7:9340:2023:1b0e:57d0:c3f2",
                        "deviceMake": "",
                        "deviceModel": "",
                        "visitorData": "CgtzMlY0LWY5azFVdyjtsrXEBjInCgJGUhIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiAh",
                        "userAgent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0,gzip(gfe)",
                        "clientName": "WEB_REMIX",
                        "clientVersion": "1.20250730.03.00",
                        "osName": "X11",
                        "osVersion": "",
                        "originalUrl": "https://music.youtube.com/",
                        "platform": "DESKTOP",
                        "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                        "configInfo": {
                            "appInstallData": "CO2ytcQGELjkzhwQsIbPHBDiuLAFELbWzxwQr9fPHBCZmLEFEImXgBMQrtbPHBCc188cEMXDzxwQudnOHBDFy88cEJbWzxwQu9nOHBDv1M8cEMzAzxwQzN-uBRD92M8cEM6szxwQiIewBRDw4s4cEKiZgBMQvZmwBRDa984cEJOGzxwQ8sTPHBC9irAFEL22rgUQmLnPHBDiys8cEIHNzhwQ9quwBRDT4a8FEKHXzxwQhtnPHBD9zs8cEObJzxwQh6zOHBCJsM4cEJmNsQUQntCwBRD8ss4cEMn3rwUQ8djPHBCKgoATEPbLzxwQt-r-EhDwnc8cEL3ZzxwQ3rzOHBDjvs8cEJT-sAUQqp3PHBCAl88cEKfSzxwQ_o7PHCosQ0FNU0d4VVFvTDJ3RE5Ia0J1SGRoUXFCbFEweXYxX3AxUVVEem53ZEJ3PT0%3D",
                            "coldConfigData": "CO2ytcQGGjJBT2pGb3gxTUVZZDVGamlyZThUVXphT3l6QlZXd3l4SnRmUGE3TlQxUG5seEphOUZ5QSIyQU9qRm94MTVvbDJlSHJVc3lnTDFvb002YXF0czJyVGdJcXQxSTd0cThvNmppbnUyZmc%3D",
                            "coldHashData": "CO2ytcQGEhM4MzcyMjg4Nzg1MDY2MDg0NzkyGO2ytcQGMjJBT2pGb3gxTUVZZDVGamlyZThUVXphT3l6QlZXd3l4SnRmUGE3TlQxUG5seEphOUZ5QToyQU9qRm94MTVvbDJlSHJVc3lnTDFvb002YXF0czJyVGdJcXQxSTd0cThvNmppbnUyZmc%3D",
                            "hotHashData": "CO2ytcQGEhM0ODM0MDgxNTExNDAyNjgwMTA2GO2ytcQGMjJBT2pGb3gxTUVZZDVGamlyZThUVXphT3l6QlZXd3l4SnRmUGE3TlQxUG5seEphOUZ5QToyQU9qRm94MTVvbDJlSHJVc3lnTDFvb002YXF0czJyVGdJcXQxSTd0cThvNmppbnUyZmc%3D",
                        },
                        "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                        "timeZone": "Europe/Paris",
                        "browserName": "Firefox",
                        "browserVersion": "140.0",
                        "acceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "deviceExperimentId": "ChxOelV6TXpjM05qQTNOalU0TVRnNU56UTJOZz09EO2ytcQGGO2ytcQG",
                        "rolloutToken": "CJzO7rat4OzVygEQr4uzyPbXjQMY8pCZ6qrpjgM%3D",
                        "screenWidthPoints": 1600,
                        "screenHeightPoints": 525,
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
                        "internalExperimentFlags": [],
                        "consistencyTokenJars": [
                            {
                                "encryptedTokenJarContents": "AKreu9vuVhZ7mgLYAgw5EPwRRJJnTlPZAO1Ys7Prjz4G9HY8jUdk_IOUl0nUHIJ7bx2GdRVNw-rYtcmyykEzZCxLgl7pqyuhv4S4IPZT_BGv5f6TvRseba_X7vJDXfUXaVuEHrYS9rPUaMZMNQehHo0E"
                            }
                        ],
                    },
                    "clientScreenNonce": "tMpnFFxwzgdGO0tf",
                    "adSignalsInfo": {
                        "params": [
                            {"key": "dt", "value": "1754093936479"},
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
                            {"key": "bih", "value": "525"},
                            {"key": "biw", "value": "1600"},
                            {
                                "key": "brdim",
                                "value": "0,0,0,0,1600,0,1600,1156,1600,525",
                            },
                            {"key": "vis", "value": "1"},
                            {"key": "wgl", "value": "true"},
                            {"key": "ca_type", "value": "image"},
                        ]
                    },
                    "clickTracking": {
                        "clickTrackingParams": "CJ0FEMn0AhgDIhMI59m3ju3qjgMV1NBJBx2XnShZ"
                    },
                },
                "playbackContext": {
                    "contentPlaybackContext": {
                        "html5Preference": "HTML5_PREF_WANTS",
                        "lactMilliseconds": "35",
                        "referer": "https://music.youtube.com/",
                        "signatureTimestamp": 20299,
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
                "cpn": "0lhBxSpnzJZiKM6i",
                "playlistId": "RDAMVMsWcLccMuCA8",
                "captionParams": {},
            },
        ).json()
        return raw["videoDetails"]["thumbnail"]["thumbnails"][-1]["url"]
    except Exception as exc:
        traceback.print_exception(exc)
        return f"https://img.youtube.com/vi/{ytid}/0.jpg"
