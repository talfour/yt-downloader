import os, time
from pytube import YouTube

SAVE_PATH = os.getcwd() + "/download/"


def get_file(links):

    if len(links) == 1:
        try:
            yt = YouTube(links[0])
            yt.streams.filter(type="audio", mime_type="audio/mp4").order_by(
                "abr"
            ).desc().first().download(SAVE_PATH)
            return True
        except Exception as e:
            return e

    else:
        for i in links:
            try:
                yt = YouTube(i)
                yt.streams.filter(type="audio", mime_type="audio/mp4").order_by(
                    "abr"
                ).desc().first().download(SAVE_PATH)
                # Added 5 sec sleep to do not send too many requests
                time.sleep(5)

            except Exception as e:
                return e
        return True
