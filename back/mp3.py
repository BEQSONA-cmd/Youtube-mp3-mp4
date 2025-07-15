import yt_dlp
import os
from multiprocessing import Process, Queue

TIMEOUT = 30 

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
        }

        filename = run_with_timeout(download_worker, TIMEOUT, url, ydl_opts, output_path)
        return filename

    except TimeoutError as e:
        return None
    except Exception as e:
        return None
    
download_youtube_as_mp3("https://www.youtube.com/watch?v=mNrzmpA8JU4")