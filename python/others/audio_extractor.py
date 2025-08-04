#!/usr/bin/env python3
"""
Standalone Audio Extractor Tool
Usage: python audio_extractor.py input.mp4 [--format mp3|wav]
"""
import argparse
import logging
from python.audio_processing.audio_cleaner import extract_audio_from_video

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Extract audio from video files")
    parser.add_argument("input", help="Input video file path")
    parser.add_argument("--format", choices=["mp3", "wav"], default="mp3")
    args = parser.parse_args()

    try:
        output_path = extract_audio_from_video(
            video_path=args.input,
            output_dir="output_audio"
        )
        logger.info(f"Audio extracted successfully: {output_path}")
    except Exception as e:
        logger.error(f"Extraction failed: {e}")

if __name__ == "__main__":
    main()