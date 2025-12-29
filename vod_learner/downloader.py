import yt_dlp
import tempfile
import os
import shutil

def download_vod(url: str, temp_dir: str) -> str:
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(temp_dir, 'valorant_vod.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    # Return first (only) mp4 file
    for file in os.listdir(temp_dir):
        if file.startswith('valorant_vod') and file.endswith('.mp4'):
            return os.path.join(temp_dir, file)
    raise ValueError("Download failed")