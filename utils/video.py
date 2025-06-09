from yt_dlp import YoutubeDL

def get_video_info(url):
    with YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get("duration", 0)