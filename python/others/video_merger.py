#!/usr/bin/env python3
"""
Standalone Video-Audio Merger
Usage: python video_merger.py video.mp4 audio.wav
"""
import argparse
import logging
from python.main import create_final_video

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Merge video with cleaned audio")
    parser.add_argument("video", help="Original video file")
    parser.add_argument("audio", help="Cleaned audio file")
    args = parser.parse_args()

    try:
        output_path = create_final_video(
            original_video=args.video,
            censored_audio=args.audio,
            output_path="output_merged.mp4"
        )
        logger.info(f"Merged video saved: {output_path}")
    except Exception as e:
        logger.error(f"Merge failed: {e}")

if __name__ == "__main__":
    main()