from flask import Flask, request, send_file, abort, after_this_request
from flask_cors import CORS
import tempfile, shutil, os
from download import download_youtube_as_mp3, download_youtube_as_mp4

app = Flask(__name__)
CORS(app)

def download_media(url, download_func, media_type):
    if not url:
        abort(400, "Missing ?link=… parameter")

    tmpfiles_dir = os.path.join(os.path.dirname(__file__), "tmp")
    os.makedirs(tmpfiles_dir, exist_ok=True)
    temp_dir = tempfile.mkdtemp(prefix=f"yt{media_type}_", dir=tmpfiles_dir)

    try:
        filepath = download_func(url, output_path=temp_dir)
        if not filepath or not os.path.exists(filepath):
            abort(500, "Could not download the video")

        filename = os.path.basename(filepath)

        @after_this_request
        def cleanup(response):
            shutil.rmtree(temp_dir, ignore_errors=True)
            return response

        mimetype = "audio/mpeg" if media_type == "mp3" else "video/mp4"
        return send_file(
            filepath,
            mimetype=mimetype,
            as_attachment=True,
            download_name=filename,
            max_age=0
        )

    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        abort(500, str(e))

@app.get("/api/downloadMP3")
def download_mp3():
    url = request.args.get("link")
    return download_media(url, download_youtube_as_mp3, "mp3")

@app.get("/api/downloadMP4")
def download_mp4():
    url = request.args.get("link")
    return download_media(url, download_youtube_as_mp4, "mp4")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)