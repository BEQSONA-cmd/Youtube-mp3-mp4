from flask import Flask, request
from flask_cors import CORS
from send import send_media
from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv("HOST", "http://localhost:3000")

app = Flask(__name__)
CORS(
    app,
    expose_headers=["Content-Disposition", "Content-Length", "ETag"]
    )

def shorten_url(url):
    if "&" in url:
        return url.split("&")[0]
    if "youtube.com/watch?v=" not in url and "youtu.be/" not in url:
        return None
    return url

@app.get("/flask/api/downloadMP3")
def download_mp3():
    reqUrl = request.args.get("link")
    url = shorten_url(reqUrl)
    if not url:
        return "Invalid URL", 400
    return send_media(url, "mp3")

@app.get("/flask/api/downloadMP4")
def download_mp4():
    reqUrl = request.args.get("link")
    url = shorten_url(reqUrl)
    if not url:
        return "Invalid URL", 400
    return send_media(url, "mp4")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)