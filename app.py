import os
import uuid
import threading
from pathlib import Path
from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
from pypdf import PdfReader
from pydub import AudioSegment

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["OUTPUT_FOLDER"] = "output"
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100MB

jobs = {}


def extract_pdf_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text.strip())
    return "\n\n".join(pages)


def split_into_chunks(text: str, max_chars: int = 250) -> list[str]:
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current = ""
    for sentence in sentences:
        if len(current) + len(sentence) <= max_chars:
            current += (" " if current else "") + sentence
        else:
            if current:
                chunks.append(current)
            current = sentence
    if current:
        chunks.append(current)
    return [c for c in chunks if c.strip()]


def convert_to_wav(src_path: str) -> str:
    wav_path = str(Path(src_path).with_suffix(".wav"))
    audio = AudioSegment.from_file(src_path)
    audio = audio.set_channels(1).set_frame_rate(22050).set_sample_width(2)
    audio.export(wav_path, format="wav")
    return wav_path


def run_tts_job(job_id: str, pdf_path: str, voice_path: str):
    try:
        jobs[job_id]["status"] = "extracting"
        text = extract_pdf_text(pdf_path)
        if not text.strip():
            jobs[job_id]["status"] = "error"
            jobs[job_id]["error"] = "Could not extract text from PDF. It may be a scanned image PDF."
            return

        chunks = split_into_chunks(text)
        jobs[job_id]["total"] = len(chunks)

        wav_voice_path = convert_to_wav(voice_path)

        from TTS.api import TTS

        jobs[job_id]["status"] = "loading_model"
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

        jobs[job_id]["status"] = "generating"
        segment_paths = []
        tmp_dir = Path(app.config["OUTPUT_FOLDER"]) / job_id
        tmp_dir.mkdir(parents=True, exist_ok=True)

        for i, chunk in enumerate(chunks):
            seg_path = tmp_dir / f"chunk_{i:05d}.wav"
            tts.tts_to_file(
                text=chunk,
                speaker_wav=wav_voice_path,
                language="en",
                file_path=str(seg_path),
            )
            segment_paths.append(str(seg_path))
            jobs[job_id]["done"] = i + 1

        jobs[job_id]["status"] = "stitching"
        combined = AudioSegment.empty()
        for path in segment_paths:
            combined += AudioSegment.from_wav(path)

        out_path = Path(app.config["OUTPUT_FOLDER"]) / f"{job_id}.mp3"
        combined.export(str(out_path), format="mp3")

        for path in segment_paths:
            os.remove(path)
        tmp_dir.rmdir()

        jobs[job_id]["status"] = "done"
        jobs[job_id]["output"] = f"{job_id}.mp3"

    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    if "pdf" not in request.files or "voice" not in request.files:
        return jsonify({"error": "Both a PDF and a voice sample are required."}), 400

    pdf_file = request.files["pdf"]
    voice_file = request.files["voice"]

    if pdf_file.filename == "" or voice_file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    job_id = str(uuid.uuid4())
    upload_dir = Path(app.config["UPLOAD_FOLDER"]) / job_id
    upload_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = upload_dir / secure_filename(pdf_file.filename)
    voice_path = upload_dir / secure_filename(voice_file.filename)
    pdf_file.save(str(pdf_path))
    voice_file.save(str(voice_path))

    jobs[job_id] = {"status": "queued", "done": 0, "total": 0}

    thread = threading.Thread(
        target=run_tts_job,
        args=(job_id, str(pdf_path), str(voice_path)),
        daemon=True,
    )
    thread.start()

    return jsonify({"job_id": job_id})


@app.route("/status/<job_id>")
def status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Unknown job."}), 404
    return jsonify(job)


@app.route("/download/<job_id>")
def download(job_id):
    job = jobs.get(job_id)
    if not job or job.get("status") != "done":
        return jsonify({"error": "Not ready."}), 404
    out_path = Path(app.config["OUTPUT_FOLDER"]) / job["output"]
    return send_file(str(out_path), as_attachment=True, download_name="audiobook.mp3")


if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["OUTPUT_FOLDER"], exist_ok=True)
    app.run(debug=False, port=5000)
