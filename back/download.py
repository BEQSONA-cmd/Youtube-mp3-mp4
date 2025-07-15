import yt_dlp
import os
from multiprocessing import Process, Queue

TIMEOUT = 60 

def download_worker(url, ydl_opts, output_path, queue):
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if ydl_opts.get('postprocessors'):
                filename = os.path.join(output_path, f"{info['title']}.mp3")
            else:
                filename = os.path.join(output_path, f"{info['title']}.mp4")
            queue.put(filename)
    except Exception as e:
        queue.put(e)

def run_with_timeout(func, timeout, *args, **kwargs):
    queue = Queue()
    p = Process(target=func, args=args + (queue,), kwargs=kwargs)
    p.start()
    p.join(timeout=timeout)
    
    if p.is_alive():
        p.terminate()
        p.join()
        raise TimeoutError(f"Download took longer than {timeout} seconds")
    
    if not queue.empty():
        result = queue.get()
        if isinstance(result, Exception):
            raise result
        return result
    raise RuntimeError("Download process failed")

def get_ydl_opts(format_type, output_path):
    common_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'quiet': False,
        # Anti-bot evasion settings:
        'extractor_args': {'youtube': {'player_client': ['android']}},
        'throttledratelimit': 1000000,  # Limit download speed (1MB/s)
        'retries': 10,
        'fragment_retries': 10,
        'skip_unavailable_fragments': True,
        'extract_flat': 'discard',
        'force_ipv4': True,
        'source_address': '0.0.0.0',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'http_headers': {
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Fetch-Mode': 'navigate',
        }
    }

    if format_type == 'mp3':
        common_opts.update({
            'format': 'bestaudio/best',
            'writethumbnail': True,
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
                {'key': 'EmbedThumbnail'},
                {'key': 'FFmpegMetadata'}
            ],
            'prefer_ffmpeg': True,
        })
    else:  # mp4
        common_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        })
    
    return common_opts

def download_youtube_as_mp3(url, output_path="music/"):
    try:
        os.makedirs(output_path, exist_ok=True)
        ydl_opts = get_ydl_opts('mp3', output_path)
        filename = run_with_timeout(download_worker, TIMEOUT, url, ydl_opts, output_path)
        return filename
    except Exception as e:
        print(f"Error downloading MP3: {str(e)}")
        return None

def download_youtube_as_mp4(url, output_path="videos/"):
    try:
        os.makedirs(output_path, exist_ok=True)
        ydl_opts = get_ydl_opts('mp4', output_path)
        filename = run_with_timeout(download_worker, TIMEOUT, url, ydl_opts, output_path)
        return filename
    except Exception as e:
        print(f"Error downloading MP4: {str(e)}")
        return None