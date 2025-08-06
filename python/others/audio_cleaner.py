#!/usr/bin/env python3
"""
Standalone Audio Cleaning Tool
Usage: python audio_cleaner.py input.wav [--gender male|female]
"""
import argparse
import logging
import os
from python.audio_processing.audio_cleaner import process_audio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_audio_standalone(audio_path: str, output_dir: str, voice_gender: str = "female"):
    """Process audio file to clean profanity and return result dict."""
    try:
        # If input is video, extract audio first
        if audio_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm')):
            from python.audio_processing.audio_cleaner import extract_audio_from_video
            audio_path = extract_audio_from_video(audio_path, output_dir)
        
        result = process_audio(
            audio_path=audio_path,
            output_dir=output_dir,
            voice_gender=voice_gender
        )
        logger.info(f"Cleaned audio saved: {result['cleaned_audio']}")
        return result
    except Exception as e:
        logger.error(f"Cleaning failed: {e}")
        raise RuntimeError(f"Audio cleaning failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="Clean profanity from audio files")
    parser.add_argument("input", help="Input audio/video file path")
    parser.add_argument("--gender", choices=["male", "female"], default="female")
    args = parser.parse_args()

    try:
        result = process_audio_standalone(
            audio_path=args.input,
            output_dir="output_clean",
            voice_gender=args.gender
        )
        logger.info(f"Cleaned audio saved: {result['cleaned_audio']}")
    except Exception as e:
        logger.error(f"Cleaning failed: {e}")

if __name__ == "__main__":
    main()