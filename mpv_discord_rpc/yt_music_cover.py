import traceback

import requests


def yt_music_cover(ytb_url: str) -> str:
    ytid = ytb_url.split("?v=")[-1]
    try:
        return requests.post(
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
    except Exception as exc:
        traceback.print_exception(exc)
        return f"https://img.youtube.com/vi/{ytid}/0.jpg"
