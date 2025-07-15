import tempfile, shutil, os
from flask import send_file, after_this_request, make_response

def send_media(url, download_func, media_type):
    if not url:
        return make_response("Invalid URL", 400)

    tmpfiles_dir = os.path.join(os.path.dirname(__file__), "tmp")
    os.makedirs(tmpfiles_dir, exist_ok=True)
    temp_dir = tempfile.mkdtemp(prefix=f"yt{media_type}_", dir=tmpfiles_dir)

    try:
        filepath = download_func(url, output_path=temp_dir)
        if not filepath or not os.path.exists(filepath):
            shutil.rmtree(temp_dir, ignore_errors=True)
            return make_response("File is too large to download", 413)

        filename = os.path.basename(filepath)

        @after_this_request
        def cleanup(response):
            shutil.rmtree(temp_dir, ignore_errors=True)
            return response

        mimetype = "audio/mpeg" if media_type == "mp3" else "video/mp4"
        
        response = make_response(send_file(
            filepath,
            mimetype=mimetype,
            as_attachment=True,
            download_name=filename,
            max_age=0
        ))
        
        return response

    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        return make_response(f"Error: {str(e)}", 500)
