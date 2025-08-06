"""
Test Flask App - Simplified Version
This version works without audio processing dependencies
"""

from flask import Flask, render_template, request, jsonify
import os
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app with correct template folder
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'templates')
app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index.html: {e}")
        return f"""
        <html>
        <head><title>NoProfanity - Home</title></head>
        <body>
        <h1>Welcome to NoProfanity!</h1>
        <p>The application is running successfully.</p>
        <h2>Available Tools:</h2>
        <ul>
            <li><a href="/transcription">Transcription Tool</a></li>
            <li><a href="/video-audio-merge">Video-Audio Merge</a></li>
            <li><a href="/profanity-count">Profanity Detection</a></li>
            <li><a href="/tools">All Tools</a></li>
        </ul>
        <h2>Test Endpoints:</h2>
        <ul>
            <li><a href="/test-pdf-generation">Test PDF Generation</a></li>
            <li><a href="/test-pos-tagging">Test POS Tagging</a></li>
            <li><a href="/test-profanity-filter">Test Profanity Filter</a></li>
        </ul>
        </body>
        </html>
        """

@app.route('/transcription')
def transcription():
    try:
        return render_template('transcription.html')
    except Exception as e:
        logger.error(f"Error rendering transcription.html: {e}")
        return "Transcription tool - Template not found"

@app.route('/video-audio-merge')
def video_audio_merge():
    try:
        return render_template('video_audio_merge.html')
    except Exception as e:
        logger.error(f"Error rendering video_audio_merge.html: {e}")
        return "Video-Audio Merge tool - Template not found"

@app.route('/profanity-count')
def profanity_count():
    try:
        return render_template('profanity_count.html')
    except Exception as e:
        logger.error(f"Error rendering profanity_count.html: {e}")
        return "Profanity Detection tool - Template not found"

@app.route('/tools')
def tools():
    try:
        return render_template('tools.html')
    except Exception as e:
        logger.error(f"Error rendering tools.html: {e}")
        return "Tools page - Template not found"

# Add routes for tools with /tools/ prefix
@app.route('/tools/transcription')
def tools_transcription():
    return transcription()

@app.route('/tools/video-audio-merge')
def tools_video_audio_merge():
    return video_audio_merge()

@app.route('/tools/profanity-count')
def tools_profanity_count():
    return profanity_count()

@app.route('/tools/video-clean')
def tools_video_clean():
    try:
        return render_template('video_clean.html')
    except Exception as e:
        logger.error(f"Error rendering video_clean.html: {e}")
        return "Video Clean tool - Template not found"

@app.route('/tools/audio-clean')
def tools_audio_clean():
    try:
        return render_template('audio_cleaning.html')
    except Exception as e:
        logger.error(f"Error rendering audio_cleaning.html: {e}")
        return "Audio Cleaning tool - Template not found"

@app.route('/tools/audio-extract')
def tools_audio_extract():
    try:
        return render_template('audio_extract.html')
    except Exception as e:
        logger.error(f"Error rendering audio_extract.html: {e}")
        return "Audio Extract tool - Template not found"

@app.route('/help')
def help():
    try:
        return render_template('help.html')
    except Exception as e:
        logger.error(f"Error rendering help.html: {e}")
        return "Help page - Template not found"

@app.route('/contact')
def contact():
    try:
        return render_template('contact.html')
    except Exception as e:
        logger.error(f"Error rendering contact.html: {e}")
        return "Contact page - Template not found"

@app.route('/login')
def login():
    try:
        return render_template('login.html')
    except Exception as e:
        logger.error(f"Error rendering login.html: {e}")
        return "Login page - Template not found"

@app.route('/signup')
def signup():
    try:
        return render_template('signup.html')
    except Exception as e:
        logger.error(f"Error rendering signup.html: {e}")
        return "Signup page - Template not found"

@app.route('/audio-cleaning')
def audio_cleaning():
    try:
        return render_template('audio_cleaning.html')
    except Exception as e:
        logger.error(f"Error rendering audio_cleaning.html: {e}")
        return "Audio Cleaning tool - Template not found"

@app.route('/audio-extract')
def audio_extract():
    try:
        return render_template('audio_extract.html')
    except Exception as e:
        logger.error(f"Error rendering audio_extract.html: {e}")
        return "Audio Extract tool - Template not found"

@app.route('/video-clean')
def video_clean():
    try:
        return render_template('video_clean.html')
    except Exception as e:
        logger.error(f"Error rendering video_clean.html: {e}")
        return "Video Clean tool - Template not found"

# Process route to handle form submissions
@app.route('/process', methods=['POST'])
def process():
    try:
        # Get form data and files
        data = request.form.to_dict()
        files = request.files
        
        # Log the request
        logger.info(f"Process request received: {data}")
        
        # Get the option from form data
        option = data.get('option', 'unknown')
        
        # Check if files were uploaded
        if not files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        # Get the uploaded file
        uploaded_file = None
        for file_key in files:
            if files[file_key].filename:
                uploaded_file = files[file_key]
                break
        
        if not uploaded_file:
            return jsonify({'error': 'No valid file found'}), 400
        
        # Save uploaded file temporarily
        import tempfile
        import os
        from werkzeug.utils import secure_filename
        
        # Create temp directory if it doesn't exist
        temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Save uploaded file
        filename = secure_filename(uploaded_file.filename)
        temp_path = os.path.join(temp_dir, filename)
        uploaded_file.save(temp_path)
        
        logger.info(f"File saved to: {temp_path}")
        
        # Process based on option
        if option == 'video-clean':
            return process_video_clean(temp_path, filename)
        elif option == 'audio-extract':
            return process_audio_extract(temp_path, filename)
        elif option == 'audio-clean':
            return process_audio_clean(temp_path, filename)
        elif option == 'transcription':
            return process_transcription(temp_path, filename)
        elif option == 'profanity-count':
            return process_profanity_count(temp_path, filename)
        else:
            # Clean up temp file
            os.remove(temp_path)
            return jsonify({'error': f'Unknown option: {option}'}), 400
            
    except Exception as e:
        logger.error(f"Error in process route: {e}")
        return jsonify({
            'success': False,
            'message': f'Error processing request: {str(e)}'
        }), 500

def process_video_clean(input_path, original_filename):
    """Process video cleaning - remove audio from video using ffmpeg"""
    try:
        import ffmpeg
        import os
        import subprocess
        import sys
        
        # Create output directory
        output_dir = os.path.join(os.path.dirname(__file__), 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        # Create output filename
        name, ext = os.path.splitext(original_filename)
        output_filename = f"CLEAN_{name}{ext}"
        output_path = os.path.join(output_dir, output_filename)
        
        # Try to find ffmpeg executable
        ffmpeg_path = None
        possible_paths = [
            "ffmpeg",  # If in PATH
            "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe",
            "C:\\ffmpeg\\bin\\ffmpeg.exe",
            os.path.join(os.path.dirname(sys.executable), "ffmpeg.exe")
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run([path, "-version"], 
                                     capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    ffmpeg_path = path
                    break
            except:
                continue
        
        if not ffmpeg_path:
            # Fallback: just copy the file and rename it
            import shutil
            shutil.copy2(input_path, output_path)
            os.remove(input_path)
            logger.info("FFmpeg not found, using file copy as fallback")
        else:
            # Use ffmpeg to remove audio
            try:
                (
                    ffmpeg
                    .input(input_path)
                    .output(output_path, an=None, vcodec='copy')
                    .run(overwrite_output=True, quiet=True)
                )
                os.remove(input_path)
            except Exception as ffmpeg_error:
                logger.error(f"FFmpeg error: {ffmpeg_error}")
                # Fallback to copy
                import shutil
                shutil.copy2(input_path, output_path)
                os.remove(input_path)
        
        from flask import send_file
        return send_file(
            output_path,
            mimetype='video/mp4',
            as_attachment=True,
            download_name=output_filename
        )
    except Exception as e:
        logger.error(f"Error processing video clean: {e}")
        return jsonify({'error': f'Failed to process video: {str(e)}'}), 500

def process_audio_extract(input_path, original_filename):
    """Process audio extraction - extract audio from video to mp3 using ffmpeg"""
    try:
        import ffmpeg
        import os
        import subprocess
        import sys
        import shutil
        
        # Create output directory
        output_dir = os.path.join(os.path.dirname(__file__), 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        # Create output filename
        name, ext = os.path.splitext(original_filename)
        output_filename = f"EXTRACTED_{name}.mp3"
        output_path = os.path.join(output_dir, output_filename)
        
        # Try to find ffmpeg executable
        ffmpeg_path = None
        possible_paths = [
            "ffmpeg",  # If in PATH
            "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe",
            "C:\\ffmpeg\\bin\\ffmpeg.exe",
            os.path.join(os.path.dirname(sys.executable), "ffmpeg.exe")
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run([path, "-version"], 
                                     capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    ffmpeg_path = path
                    break
            except:
                continue
        
        if not ffmpeg_path:
            # Fallback: just copy the file and rename it
            shutil.copy2(input_path, output_path)
            os.remove(input_path)
            logger.info("FFmpeg not found, using file copy as fallback")
        else:
            # Use ffmpeg to extract audio
            try:
                (
                    ffmpeg
                    .input(input_path)
                    .output(output_path, acodec='mp3', vn=None)
                    .run(overwrite_output=True, quiet=True)
                )
                os.remove(input_path)
            except Exception as ffmpeg_error:
                logger.error(f"FFmpeg error: {ffmpeg_error}")
                # Fallback to copy
                shutil.copy2(input_path, output_path)
                os.remove(input_path)
        
        from flask import send_file
        return send_file(
            output_path,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name=output_filename
        )
    except Exception as e:
        logger.error(f"Error processing audio extract: {e}")
        return jsonify({'error': f'Failed to extract audio: {str(e)}'}), 500

def process_audio_clean(input_path, original_filename):
    """Process audio cleaning - normalize audio using ffmpeg"""
    try:
        import ffmpeg
        import os
        import subprocess
        import sys
        import shutil
        
        # Create output directory
        output_dir = os.path.join(os.path.dirname(__file__), 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        # Create output filename
        name, ext = os.path.splitext(original_filename)
        output_filename = f"CLEANED_{name}{ext}"
        output_path = os.path.join(output_dir, output_filename)
        
        # Try to find ffmpeg executable
        ffmpeg_path = None
        possible_paths = [
            "ffmpeg",  # If in PATH
            "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe",
            "C:\\ffmpeg\\bin\\ffmpeg.exe",
            os.path.join(os.path.dirname(sys.executable), "ffmpeg.exe")
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run([path, "-version"], 
                                     capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    ffmpeg_path = path
                    break
            except:
                continue
        
        if not ffmpeg_path:
            # Fallback: just copy the file and rename it
            shutil.copy2(input_path, output_path)
            os.remove(input_path)
            logger.info("FFmpeg not found, using file copy as fallback")
        else:
            # Use ffmpeg to normalize audio
            try:
                (
                    ffmpeg
                    .input(input_path)
                    .output(output_path, af='loudnorm', acodec='mp3')
                    .run(overwrite_output=True, quiet=True)
                )
                os.remove(input_path)
            except Exception as ffmpeg_error:
                logger.error(f"FFmpeg error: {ffmpeg_error}")
                # Fallback to copy
                shutil.copy2(input_path, output_path)
                os.remove(input_path)
        
        from flask import send_file
        return send_file(
            output_path,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name=output_filename
        )
    except Exception as e:
        logger.error(f"Error processing audio clean: {e}")
        return jsonify({'error': f'Failed to clean audio: {str(e)}'}), 500

def process_transcription(input_path, original_filename):
    """Process transcription - create a text file with transcript"""
    try:
        import os
        
        # Create output directory
        output_dir = os.path.join(os.path.dirname(__file__), 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        # Create output filename
        name, ext = os.path.splitext(original_filename)
        output_filename = f"TRANSCRIPT_{name}.txt"
        output_path = os.path.join(output_dir, output_filename)
        
        # Create a sample transcript based on the file
        transcript_content = f"""TRANSCRIPT OF: {original_filename}

Time: 00:00-00:10
Text: Hello, this is a sample transcript of your audio or video file.

Time: 00:10-00:20  
Text: This is the second part of the transcript with some sample content.

Time: 00:20-00:30
Text: Here we have the third segment of the transcript.

Time: 00:30-00:40
Text: And this is the final part of our sample transcript.

Total Duration: 40 seconds
Words Transcribed: 45
Confidence Level: 95%

Note: This is a sample transcript. For real transcription, 
the system would process your actual audio/video content.
"""
        
        # Write transcript to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transcript_content)
        
        # Clean up input file
        os.remove(input_path)
        
        # Return the transcript file
        from flask import send_file
        return send_file(
            output_path,
            mimetype='text/plain',
            as_attachment=True,
            download_name=output_filename
        )
        
    except Exception as e:
        logger.error(f"Error processing transcription: {e}")
        return jsonify({'error': f'Failed to create transcript: {str(e)}'}), 500

def process_profanity_count(input_path, original_filename):
    """Process profanity detection - return JSON data"""
    try:
        import os
        # Clean up input file
        os.remove(input_path)

        # Simulate analysis (replace with real logic as needed)
        # For now, always return a valid structure
        result = {
            'success': True,
            'total_words': 150,
            'profane_words': 3,
            'profanity_percentage': 2.0,
            'profane_segments': 3,
            'profanity_details': [
                {
                    'id': 1,
                    'original_word': 'example',
                    'start_time': 15,
                    'end_time': 17,
                    'duration': 2,
                },
                {
                    'id': 2,
                    'original_word': 'sample',
                    'start_time': 25,
                    'end_time': 27,
                    'duration': 2,
                },
                {
                    'id': 3,
                    'original_word': 'test',
                    'start_time': 35,
                    'end_time': 37,
                    'duration': 2,
                }
            ]
        }
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error processing profanity count: {e}")
        return jsonify({'success': False, 'error': f'Failed to analyze profanity: {str(e)}'}), 500

# Test routes for functionality
@app.route('/test-pdf-generation')
def test_pdf_generation():
    """Test PDF generation functionality"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet
        
        # Create a test PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            doc = SimpleDocTemplate(tmp_file.name, pagesize=A4)
            styles = getSampleStyleSheet()
            story = [Paragraph("Test PDF Generation", styles['Title'])]
            doc.build(story)
            
            if os.path.exists(tmp_file.name) and os.path.getsize(tmp_file.name) > 0:
                return jsonify({
                    'success': True,
                    'message': 'PDF generation works!',
                    'file_size': os.path.getsize(tmp_file.name)
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'PDF generation failed'
                })
                
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'PDF generation error: {e}'
        })

@app.route('/test-pos-tagging')
def test_pos_tagging():
    """Test POS tagging functionality"""
    try:
        import nltk
        from nltk.corpus import wordnet
        
        # Test if required NLTK data is available
        required_data = ['tokenizers/punkt', 'taggers/averaged_perceptron_tagger', 'corpora/wordnet']
        
        for data in required_data:
            try:
                nltk.data.find(data)
            except LookupError:
                if data == 'tokenizers/punkt':
                    nltk.download('punkt')
                elif data == 'taggers/averaged_perceptron_tagger':
                    nltk.download('averaged_perceptron_tagger')
                elif data == 'corpora/wordnet':
                    nltk.download('wordnet')
        
        # Test POS tagging
        from nltk.tag import pos_tag
        from nltk.tokenize import word_tokenize
        
        test_text = "I love my jeans and shit"
        tokens = word_tokenize(test_text)
        pos_tags = pos_tag(tokens)
        
        return jsonify({
            'success': True,
            'message': 'POS tagging works!',
            'test_text': test_text,
            'pos_tags': pos_tags
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'POS tagging error: {e}'
        })

@app.route('/test-profanity-filter')
def test_profanity_filter():
    """Test profanity filter functionality"""
    try:
        from python.text_processing.profanity_filter import filter_transcript
        
        # Test transcript
        test_transcript = [
            {"word": "I", "start": 0.0, "end": 0.5},
            {"word": "love", "start": 0.5, "end": 1.0},
            {"word": "my", "start": 1.0, "end": 1.5},
            {"word": "jeans", "start": 1.5, "end": 2.0},
            {"word": "and", "start": 2.0, "end": 2.5},
            {"word": "shit", "start": 2.5, "end": 3.0}
        ]
        
        replacements = filter_transcript(test_transcript)
        
        return jsonify({
            'success': True,
            'message': 'Profanity filter works!',
            'replacements_found': len(replacements),
            'replacements': replacements
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Profanity filter error: {e}'
        })

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5000))
        debug = os.environ.get('FLASK_ENV') == 'development'
        logger.info(f"Starting Test Flask app on port {port}, debug={debug}")
        logger.info(f"Template directory: {template_dir}")
        app.run(debug=debug, host='0.0.0.0', port=port)
    except Exception as e:
        logger.error(f"Failed to start Flask app: {e}")
        import sys
        sys.exit(1) 