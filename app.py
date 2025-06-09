from flask import Flask, request, jsonify, send_from_directory
from utils.transcript import get_transcript_or_audio
from utils.summary import summarize_text
from utils.estimate import estimate_processing_time
from utils.video import get_video_info

app = Flask(__name__)

@app.route("/api/summarize", methods=["POST"])
def summarize():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    transcript, used_vosk = get_transcript_or_audio(url)
    duration = get_video_info(url)
    estimate = estimate_processing_time(duration, used_vosk)
    summary = summarize_text(transcript)

    return jsonify({
        "summary": summary,
        "used_vosk": used_vosk,
        "duration_seconds": duration,
        "estimated_time": estimate
    })

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/")
def home():
    return send_from_directory("frontend", "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory("frontend", path)
