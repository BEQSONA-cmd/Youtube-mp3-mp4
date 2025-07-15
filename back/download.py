import yt_dlp
import os

def download_youtube_as_mp3(url, output_path="music/"):
    try:
        os.makedirs(output_path, exist_ok=True)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'writethumbnail': True,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                },
                {
                    'key': 'EmbedThumbnail',
                },
                {
                    'key': 'FFmpegMetadata',
                }
            ],
            'prefer_ffmpeg': True,
            'quiet': False,
        }

        print(f"Downloading: {url}...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = os.path.join(output_path, f"{info['title']}.mp3")
            print(f"Downloaded as MP3: {filename}")
            return filename

    except Exception as e:
        print(f"Error: {e}")
        return None



def download_youtube_as_mp4(url, output_path="videos/"):
    try:
        os.makedirs(output_path, exist_ok=True)
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'quiet': False,
        }
        
        print(f"Downloading: {url}...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = os.path.join(output_path, f"{info['title']}.mp4")
            print(f"Downloaded as MP4: {filename}")
            return filename
            
    except Exception as e:
        print(f"Error: {e}")
        return None