import subprocess
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from pytube import YouTube
import vosk
import wave
import json
import os

def extract_video_id(url):
    import re
    match = re.search(r"(?:v=|youtu\.be/)([\w-]+)", url)
    return match.group(1) if match else None

def get_transcript_or_audio(url):
    video_id = extract_video_id(url)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([t["text"] for t in transcript])
        return full_text, False
    except TranscriptsDisabled:
        audio_path = "audio.mp3"
        subprocess.call(["yt-dlp", "-x", "--audio-format", "mp3", "-o", audio_path, url])

        # Transcribe with VOSK
        model = vosk.Model(lang="pl")
        wf = wave.open(audio_path, "rb")
        rec = vosk.KaldiRecognizer(model, wf.getframerate())
        result = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result += json.loads(rec.Result())["text"] + " "
        result += json.loads(rec.FinalResult())["text"]
        return result, True