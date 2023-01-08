# Projet "Youtube Downloader"

import os
from pytube import YouTube
import ffmpeg


def on_download_progress(stream, chunk, bytes_remaining):
    bytes_downloaded = stream.filesize - bytes_remaining
    percent = bytes_downloaded * 100 / stream.filesize

    print(f"Progression du téléchargement {int(percent)}%")


def download_video(url):
    youtube_video = YouTube(url)

    youtube_video.register_on_progress_callback(on_download_progress)

    # print("TITRE: " + youtube_video.title)
    # print("NB VUES:", youtube_video.views)

    # print("")

    # print("STREAMS")
    streams = youtube_video.streams.filter(progressive=False, file_extension='mp4', type="video").order_by('resolution').desc()
    video_stream = streams[0]

    streams = youtube_video.streams.filter(progressive=False, file_extension='mp4', type="audio").order_by('abr').desc()
    audio_stream = streams[0]
    # for stream in streams:
    #    print(stream)

    # print("Video stream:", video_stream)
    # print("Audio stream:", audio_stream)

    print(f"Téléchargement {youtube_video.title}...")
    video_stream.download("video")
    audio_stream.download("audio")

    audio_filename = os.path.join("audio", video_stream.default_filename)
    video_filename = os.path.join("video", video_stream.default_filename)
    output_filename = video_stream.default_filename

    ffmpeg.output(ffmpeg.input(audio_filename), ffmpeg.input(video_filename), output_filename, vcodec="copy", acodec="copy", loglevel="quiet").run(overwrite_output=True)
    print("OK")

    os.remove(audio_filename)
    os.remove(video_filename)
    os.rmdir("audio")
    os.rmdir("video")
