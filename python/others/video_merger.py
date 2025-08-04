#!/usr/bin/env python3
"""
Standalone Video-Audio Merger
Usage: python video_merger.py video.mp4 audio.wav
"""
import argparse
import logging
import os
import uuid
from python.main import create_final_video

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def merge_video_audio(video_path: str, audio_path: str, output_dir: str):
    """Merge video with audio and return output path."""
    try:
        # Generate unique output filename
        unique_id = str(uuid.uuid4())[:8]
        output_path = os.path.join(output_dir, f"merged_video_{unique_id}.mp4")
        
        create_final_video(
            original_video=video_path,
            censored_audio=audio_path,
            output_path=output_path
        )
        logger.info(f"Merged video saved: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Merge failed: {e}")
        raise RuntimeError(f"Video-audio merge failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="Merge video with cleaned audio")
    parser.add_argument("video", help="Original video file")
    parser.add_argument("audio", help="Cleaned audio file")
    args = parser.parse_args()

    try:
        output_path = merge_video_audio(
            video_path=args.video,
            audio_path=args.audio,
            output_dir="output_merged"
        )
        logger.info(f"Merged video saved: {output_path}")
    except Exception as e:
        logger.error(f"Merge failed: {e}")

if __name__ == "__main__":
    main()