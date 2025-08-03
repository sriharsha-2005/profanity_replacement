import os
import subprocess
import logging
from typing import Dict, Any
from python.audio_processing.whisper_handler import transcriber
from python.audio_processing.edge_tts_handler import generate_speech
from python.audio_processing.audio_replacer import replace_profanity_audio
from python.text_processing.profanity_filter import filter_transcript

logger = logging.getLogger(__name__)

def process_audio(
    audio_path: str,
    output_dir: str,
    voice_gender: str = "female"
) -> Dict[str, Any]:
    """Process audio file to detect and replace profanity."""
    try:
        # Step 1: Transcribe audio
        logger.info("Transcribing audio...")
        transcript = transcriber.transcribe(audio_path)
        
        if not transcript or not transcript.text:
            raise RuntimeError("No speech detected in audio file")
        
        # Step 2: Filter profanity
        logger.info("Filtering profanity...")
        filtered_transcript = filter_transcript(transcript.text)
        
        if filtered_transcript == transcript.text:
            logger.info("No profanity detected, returning original audio")
            # If no profanity found, just return the original audio
            return {
                'original_audio': audio_path,
                'cleaned_audio': audio_path,
                'transcript': transcript.text,
                'filtered_transcript': filtered_transcript
            }
        
        # Step 3: Generate replacement audio for profanity segments
        logger.info("Generating replacement audio...")
        cleaned_audio_path = os.path.join(output_dir, "cleaned_audio.wav")
        
        # Use the existing audio replacer to handle the replacement
        result = replace_profanity_audio(
            audio_path,
            transcript,
            filtered_transcript,
            cleaned_audio_path,
            voice_gender
        )
        
        if not result or not os.path.exists(cleaned_audio_path):
            raise RuntimeError("Failed to generate cleaned audio")
        
        # Convert to MP3 for better compatibility
        mp3_output_path = os.path.join(output_dir, "cleaned_audio.mp3")
        subprocess.run([
            'ffmpeg', '-y', '-i', cleaned_audio_path,
            '-acodec', 'libmp3lame', '-q:a', '2',
            mp3_output_path
        ], check=True, capture_output=True)
        
        return {
            'original_audio': audio_path,
            'cleaned_audio': mp3_output_path,
            'transcript': transcript.text,
            'filtered_transcript': filtered_transcript
        }
        
    except Exception as e:
        logger.error(f"Audio processing failed: {e}")
        raise RuntimeError(f"Audio processing error: {e}")

def extract_audio_from_video(video_path: str, output_dir: str) -> str:
    """Extract audio from video file."""
    try:
        output_path = os.path.join(output_dir, "extracted_audio.mp3")
        
        subprocess.run([
            'ffmpeg', '-y', '-i', video_path,
            '-vn', '-acodec', 'libmp3lame', '-q:a', '2',
            output_path
        ], check=True, capture_output=True)
        
        if not os.path.exists(output_path):
            raise RuntimeError("Failed to extract audio from video")
        
        logger.info(f"Audio extracted successfully: {output_path}")
        return output_path
        
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg error during audio extraction: {e}")
        raise RuntimeError(f"Audio extraction failed: {e}")
    except Exception as e:
        logger.error(f"Audio extraction failed: {e}")
        raise RuntimeError(f"Audio extraction error: {e}") 