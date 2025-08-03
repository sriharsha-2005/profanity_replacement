#!/usr/bin/env python3
"""
Standalone Profanity Detection Tool
Usage: python profanity_detector.py input.mp4|input.wav
"""
import argparse
import logging
from python.audio_processing.whisper_handler import transcriber
from python.text_processing.profanity_filter import filter_transcript

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Detect profanity in media files")
    parser.add_argument("input", help="Input video/audio file")
    args = parser.parse_args()

    try:
        # Transcribe and analyze
        transcript = transcriber.transcribe_audio(args.input)
        profanity_report = filter_transcript(transcript)
        
        # Generate report
        print(f"Profanity Analysis Report for {args.input}")
        print("="*50)
        for item in profanity_report:
            print(f"[{item['start']:.2f}s-{item['end']:.2f}s] {item['original']} → {item['replacement']}")
        
        logger.info(f"Found {len(profanity_report)} profane segments")
    except Exception as e:
        logger.error(f"Detection failed: {e}")

if __name__ == "__main__":
    main()