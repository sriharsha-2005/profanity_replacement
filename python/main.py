"""
Video Profanity Replacer - Core Processing Module
Created by: Sriharsha Chittipothu
GitHub: https://github.com/sriharsha-2005
Email: sriharshachittipothu@gmail.com
"""

import argparse
import json
import logging
import os
import subprocess
import sys
import gc
from typing import Dict, Any, List

from python.audio_processing.whisper_handler import transcriber
from python.audio_processing.edge_tts_handler import generate_speech
from python.audio_processing.audio_replacer import replace_profanity_audio
from python.text_processing.profanity_filter import filter_transcript
from python.utils.file_utils import create_dir_if_not_exists

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_audio(video_path: str, audio_path: str) -> None:
    """Extract audio from video using ffmpeg with memory optimization"""
    command = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn",                    # No video
        "-acodec", "pcm_s16le",   # Standard audio codec
        "-ar", "16000",           # Lower sample rate for memory efficiency
        "-ac", "1",               # Mono audio to reduce memory usage
        "-f", "wav",              # Force WAV format
        "-hide_banner", "-loglevel", "error",
        "-threads", "1",          # Single thread to reduce memory usage
        audio_path
    ]
    try:
        subprocess.run(command, check=True)
        logger.info(f"Successfully extracted audio to {audio_path}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Audio extraction failed: {e.stderr.decode()}")
        raise RuntimeError("Audio extraction failed")

def create_final_video(original_video: str, censored_audio: str, output_path: str) -> None:
    """Directly merge video with censored audio with memory optimization"""
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        logger.info(f"Creating final video at: {output_path}")
        
        subprocess.run([
            "ffmpeg", "-y",
            "-i", original_video,
            "-i", censored_audio,
            "-c:v", "copy",          # Preserve video quality
            "-c:a", "aac",           # Encode audio to MP4-compatible AAC
            "-ar", "16000",          # Match the extracted audio sample rate
            "-map", "0:v:0",         # Take video from input 0
            "-map", "1:a:0",         # Take audio from input 1
            "-shortest",
            "-threads", "1",         # Single thread to reduce memory usage
            output_path
        ], check=True)
        logger.info(f"Successfully created final video at {output_path}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Merge failed: {e.stderr.decode()}")
        raise RuntimeError("Final video creation failed")

def process_video(
    video_path: str,
    output_dir: str,
    voice_gender: str = "female",
    language: str = None
) -> Dict[str, Any]:
    """Pipeline: Video → Audio → Transcript → Filtered Audio → Final Video."""
    logger.info("Starting video processing pipeline...")
    
    # Convert to absolute paths
    video_path = os.path.abspath(video_path)
    output_dir = os.path.abspath(output_dir)
    
    logger.info(f"Input video path: {video_path}")
    logger.info(f"Output directory: {output_dir}")
    
    # Check file size (optimized for efficiency)
    file_size = os.path.getsize(video_path)
    max_size = 25 * 1024 * 1024  # 25MB for best efficiency
    if file_size > max_size:
        raise RuntimeError(f"File too large ({file_size / 1024 / 1024:.1f}MB). Maximum size is 25MB for optimal processing.")
    
    logger.info(f"File size: {file_size / 1024 / 1024:.1f}MB - Processing allowed")
    
    # Ensure output directory exists
    create_dir_if_not_exists(output_dir)
    
    # Clean up any existing files
    for file in os.listdir(output_dir):
        if file.startswith('replacement_') or file.endswith('.wav') or file.startswith('CLEAN_'):
            try:
                os.remove(os.path.join(output_dir, file))
            except:
                pass
    
    # Force garbage collection at start
    gc.collect()
    
    # Step 1: Extract audio
    logger.info("Step 1: Extracting audio from video...")
    audio_path = os.path.join(output_dir, "extracted.wav")
    extract_audio(video_path, audio_path)
    logger.info("Audio extraction completed")
    
    # Force garbage collection after audio extraction
    gc.collect()

    # Step 2: Transcribe
    logger.info("Step 2: Starting Whisper AI transcription (this may take several minutes)...")
    transcript = transcriber.transcribe_audio(audio_path, language=language)
    logger.info(f"Transcription completed - {len(transcript)} words processed")
    
    # Force garbage collection after transcription
    gc.collect()
    
    # Clear any cached data
    import psutil
    process = psutil.Process()
    if hasattr(process, 'memory_info'):
        logger.info(f"Memory usage after transcription: {process.memory_info().rss / 1024 / 1024:.1f}MB")

    # Step 3: Filter profanity
    logger.info("Step 3: Filtering profanity...")
    profane_segments = filter_transcript(transcript) or []
    logger.info(f"Profanity filtering completed - {len(profane_segments)} segments found")
    
    # Force garbage collection after filtering
    gc.collect()

    # Step 4: Generate replacement audio
    logger.info(f"Step 4: Generating replacement audio for {len(profane_segments)} segments...")
    for idx, entry in enumerate(profane_segments):
        logger.info(f"Generating replacement {idx + 1}/{len(profane_segments)}: '{entry['replacement']}'")
        out_path = os.path.join(output_dir, f"replacement_{idx}.mp3")
        generate_speech(entry["replacement"], out_path, voice_gender)
        entry["replacement_audio"] = out_path
        # Force garbage collection after each audio generation
        gc.collect()
    logger.info("Replacement audio generation completed")

    # Step 5: Create censored audio
    logger.info("Step 5: Creating censored audio...")
    censored_audio = os.path.join(output_dir, "censored_audio.wav")
    replace_profanity_audio(
        original_audio=audio_path,
        replacements=profane_segments,
        output_audio_file=censored_audio,
        temp_dir=os.path.join(output_dir, "temp_audio")
    )
    logger.info("Censored audio creation completed")
    
    # Force garbage collection before final video creation
    gc.collect()

    # Step 6: Create final video
    logger.info("Step 6: Creating final video...")
    # Use the original filename (without path) for output
    original_filename = os.path.basename(video_path)
    name_without_ext = os.path.splitext(original_filename)[0]
    final_video = os.path.join(output_dir, f"CLEAN_{name_without_ext}.mp4")
    
    create_final_video(video_path, censored_audio, final_video)
    logger.info("Final video creation completed")
    
    # Verify the output file exists
    if not os.path.exists(final_video):
        raise FileNotFoundError(f"Final output video not created at {final_video}")
    
    # Final cleanup and garbage collection
    gc.collect()
    logger.info("Video processing pipeline completed successfully!")

    return {
        "transcript": transcript,
        "profane_segments": profane_segments,
        "final_video": final_video,
        "censored_audio": censored_audio
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process a video to censor profanity with replacement audio."
    )
    parser.add_argument("video_path", help="Input video file path")
    parser.add_argument("output_dir", help="Output directory path")
    parser.add_argument("--gender", choices=["male", "female"], default="female")
    parser.add_argument("--language", help="Force language (e.g., 'en')", default=None)
    args = parser.parse_args()

    try:
        result = process_video(
            args.video_path,
            args.output_dir,
            voice_gender=args.gender,
            language=args.language
        )
        print(json.dumps(result, indent=2))
        logger.info(f"Final video saved to: {result['final_video']}")
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        sys.exit(1)