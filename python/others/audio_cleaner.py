#!/usr/bin/env python3
"""
Standalone Audio Cleaning Tool
Usage: python audio_cleaner.py input.wav [--gender male|female]
"""
import argparse
import logging
from python.audio_processing.audio_cleaner import process_audio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Clean profanity from audio files")
    parser.add_argument("input", help="Input audio file path")
    parser.add_argument("--gender", choices=["male", "female"], default="female")
    args = parser.parse_args()

    try:
        result = process_audio(
            audio_path=args.input,
            output_dir="output_clean",
            voice_gender=args.gender
        )
        logger.info(f"Cleaned audio saved: {result['cleaned_audio']}")
    except Exception as e:
        logger.error(f"Cleaning failed: {e}")

if __name__ == "__main__":
    main()