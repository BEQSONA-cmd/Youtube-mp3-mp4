import yt_dlp

def download_youtube_as_mp4(url, output_path="videos/"):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': f'{output_path}%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        
download_youtube_as_mp4("https://www.youtube.com/watch?v=J42wXiRIauI")