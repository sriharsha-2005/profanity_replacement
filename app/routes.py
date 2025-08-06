from flask import render_template, request, send_file, jsonify
import os
import uuid
import logging
from werkzeug.utils import secure_filename
from python.main import process_video
from python.audio_processing.audio_cleaner import extract_audio_from_video
from python.audio_processing.whisper_handler import transcriber
from python.others.audio_cleaner import process_audio_standalone
from python.others.video_merger import merge_video_audio
from python.others.transcription_analyzer import generate_transcription_pdf
from python.others.profanity_detector import detect_profanity
from app import app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure upload settings
UPLOAD_FOLDER = os.path.abspath("uploads")
OUTPUT_FOLDER = os.path.abspath("output")
ALLOWED_EXTENSIONS = {
    "video": {"mp4", "avi", "mkv", "mov", "wmv", "flv", "webm"},
    "audio": {"mp3", "wav", "m4a", "aac", "ogg"}
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # 25MB

# Ensure upload and output directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename, file_type):
    """Check if file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS.get(file_type, set())

@app.route("/")
def index():
    """Home page."""
    return render_template("index.html")

@app.route("/tools")
def tools():
    """Tools page."""
    return render_template("tools.html")

@app.route("/tools/video-clean")
def video_clean():
    """Video cleaning tool page."""
    return render_template("video_clean.html")

@app.route("/tools/audio-extract")
def audio_extract():
    """Audio extraction tool page."""
    return render_template("audio_extract.html")

@app.route("/tools/audio-clean")
def audio_clean():
    """Audio cleaning tool page."""
    return render_template("audio_cleaning.html")

@app.route("/tools/video-audio-merge")
def video_audio_merge():
    """Video and audio merge tool page."""
    return render_template("video_audio_merge.html")

@app.route("/tools/transcription")
def transcription():
    """Transcription tool page."""
    return render_template("transcription.html")

@app.route("/tools/profanity-count")
def profanity_count():
    """Profanity count dashboard page."""
    return render_template("profanity_count.html")

@app.route("/contact")
def contact():
    """Contact page."""
    return render_template("contact.html")

@app.route("/help")
def help():
    """Help page."""
    return render_template("help.html")

@app.route("/login")
def login():
    """Login page."""
    return render_template("login.html")

@app.route("/signup")
def signup():
    """Signup page."""
    return render_template("signup.html")

@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "message": "NoProfanity service is running"})

@app.route("/process", methods=["POST"])
def process():
    """Process video/audio files."""
    try:
        # Check if file was uploaded
        if "video" not in request.files and "media" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        # Handle both video and media file inputs
        file = request.files.get("video") or request.files.get("media")
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        # Get processing option
        option = request.form.get("option", "video-clean")
        gender = request.form.get("gender", "female")

        # Validate file type based on option
        if option in ["video-clean", "audio-extract"]:
            if not allowed_file(file.filename, "video"):
                return jsonify({"error": "Invalid video file format"}), 400
        elif option == "audio-clean":
            if not allowed_file(file.filename, "video") and not allowed_file(file.filename, "audio"):
                return jsonify({"error": "Invalid file format"}), 400
        elif option == "transcription":
            # For transcription, accept both audio and video files
            if not (allowed_file(file.filename, "video") or allowed_file(file.filename, "audio")):
                return jsonify({"error": "Invalid file format for transcription"}), 400
        elif option == "profanity-count":
            # For profanity detection, accept both audio and video files
            if not (allowed_file(file.filename, "video") or allowed_file(file.filename, "audio")):
                return jsonify({"error": "Invalid file format for profanity detection"}), 400

        # Generate unique filename
        file_extension = file.filename.rsplit(".", 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)

        # Save uploaded file
        file.save(file_path)

        logger.info(f"Processing {option}: {file.filename}")
        logger.info(f"Upload path: {file_path}")

        # Get absolute path to output directory
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Output directory: {output_dir}")

        # Process the file based on option
        if option == "video-clean":
            result = process_video(file_path, output_dir, gender)
            output_file = result["final_video"]
            
            logger.info(f"Looking for output file at: {output_file}")
            if not os.path.exists(output_file):
                raise FileNotFoundError(f"Output file not found at {output_file}")

        elif option == "audio-extract":
            # Extract audio only
            output_file = extract_audio_from_video(file_path, output_dir)
            logger.info(f"Audio extracted to: {output_file}")
            
        elif option == "audio-clean":
            # Process audio file for cleaning
            result = process_audio_standalone(file_path, output_dir, gender)
            output_file = result["cleaned_audio"]
            
        elif option == "transcription":
            # Handle transcription
            output_file = generate_transcription_pdf(file_path, output_dir, unique_filename)
            logger.info(f"Transcription saved to: {output_file}")
            
        elif option == "profanity-count":
            # Handle profanity detection (returns JSON data, not file)
            profanity_data = detect_profanity(file_path)
            # Clean up uploaded file
            os.remove(file_path)
            return jsonify(profanity_data)
            
        else:
            return jsonify({"error": "Invalid processing option"}), 400

        # Clean up uploaded file
        os.remove(file_path)

        # Return processed file
        return send_file(
            output_file,
            as_attachment=True,
            download_name=os.path.basename(output_file)
        )

    except Exception as e:
        logger.error(f"Processing error: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/merge", methods=["POST"])
def merge():
    """Merge video with audio file."""
    try:
        # Check if both files were uploaded
        if "video" not in request.files or "audio" not in request.files:
            return jsonify({"error": "Both video and audio files are required"}), 400

        video_file = request.files["video"]
        audio_file = request.files["audio"]
        
        if video_file.filename == "" or audio_file.filename == "":
            return jsonify({"error": "Both video and audio files must be selected"}), 400

        # Validate file types
        if not allowed_file(video_file.filename, "video"):
            return jsonify({"error": "Invalid video file format"}), 400
        
        if not allowed_file(audio_file.filename, "audio"):
            return jsonify({"error": "Invalid audio file format"}), 400

        # Generate unique filenames
        video_extension = video_file.filename.rsplit(".", 1)[1].lower()
        audio_extension = audio_file.filename.rsplit(".", 1)[1].lower()
        video_unique_filename = f"{uuid.uuid4()}_video.{video_extension}"
        audio_unique_filename = f"{uuid.uuid4()}_audio.{audio_extension}"
        
        video_path = os.path.join(app.config["UPLOAD_FOLDER"], video_unique_filename)
        audio_path = os.path.join(app.config["UPLOAD_FOLDER"], audio_unique_filename)

        # Save uploaded files
        video_file.save(video_path)
        audio_file.save(audio_path)

        logger.info(f"Merging video: {video_file.filename} with audio: {audio_file.filename}")

        # Get absolute path to output directory
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))
        os.makedirs(output_dir, exist_ok=True)

        # Merge video with audio
        output_file = merge_video_audio(video_path, audio_path, output_dir)
        logger.info(f"Merge completed: {output_file}")

        # Clean up uploaded files
        os.remove(video_path)
        os.remove(audio_path)

        # Return merged file
        return send_file(
            output_file,
            as_attachment=True,
            download_name=os.path.basename(output_file)
        )

    except Exception as e:
        logger.error(f"Merge error: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)




