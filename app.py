from flask import Flask, request, jsonify, send_file, render_template
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')
    quality = data.get('quality')

    if not url:
        return jsonify({'message': 'URL is required'}), 400

    try:
        print(f"Downloading video from URL: {url} with quality: {quality}")
        
        # Updated options to avoid using ffmpeg for merging, just download separate audio and video
        options = {'format': 'best'}
        
        with yt_dlp.YoutubeDL(options) as ydl:
            result = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(result)
        print(f"Video downloaded successfully: {filename}")

        return send_file(filename, as_attachment=True, download_name='video.mp4')

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
