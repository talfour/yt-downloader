import os, time
from pytube import YouTube

SAVE_PATH = os.getcwd() + "/download/"


def get_file(links):

    if len(links) == 1:
        try:
            yt = YouTube(links[0])
            audios = yt.streams.filter(only_audio=True).first()
            audios.download(SAVE_PATH)
        except Exception as e:
            return e

    else:
        for i in links:
            try:
                yt = YouTube(i)
                audios = yt.streams.filter(only_audio=True).first()
                audios.download(SAVE_PATH)
                # Added 5 sec sleep to do not send too many requests
                time.sleep(5)
            except Exception as e:
                return e
