import youtube_downloader


urls = ("https://www.youtube.com/watch?v=9bZkp7q19f0",
"https://www.youtube.com/watch?v=XXYlFuWEuKI",
"https://www.youtube.com/watch?v=Zi_XLOBDo_Y")

for url in urls:
    youtube_downloader.download_video(url)