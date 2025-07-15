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
            'extract_flat': True,
            'force_ipv4': True,
            'no_check_certificate': True,
            'source_address': '0.0.0.0',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'throttledratelimit': 500000,  # Limit download speed
        }

        filename = run_with_timeout(download_worker, TIMEOUT, url, ydl_opts, output_path)
        return filename

    except TimeoutError as e:
        return None
    except Exception as e:
        return None

def download_youtube_as_mp4(url, output_path="videos/"):
    try:
        os.makedirs(output_path, exist_ok=True)
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': True,
            'ratelimit': 1000000,
            'sleep_interval': 5,
        }
        filename = run_with_timeout(download_worker, TIMEOUT, url, ydl_opts, output_path)
        return filename
            
    except TimeoutError as e:
        return None
    except Exception as e:
        return None