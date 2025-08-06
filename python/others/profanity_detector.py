#!/usr/bin/env python3
"""
Standalone Profanity Detection Tool
Usage: python profanity_detector.py input.mp4|input.wav
"""
import argparse
import logging
import os
from python.audio_processing.whisper_handler import transcriber
from python.audio_processing.audio_cleaner import extract_audio_from_video
from python.text_processing.profanity_filter import filter_transcript

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def detect_profanity(input_path: str):
    """Detect profanity in media file and return analysis data."""
    try:
        # Extract audio if input is video
        if input_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm')):
            # Create temporary output dir for audio extraction
            temp_dir = os.path.dirname(input_path)
            audio_path = extract_audio_from_video(input_path, temp_dir)
        else:
            audio_path = input_path
        
        # Transcribe and analyze
        transcript = transcriber.transcribe_audio(audio_path)
        profanity_report = filter_transcript(transcript)
        
        # Calculate statistics
        total_words = len(transcript)
        profane_segments = len(profanity_report)
        profane_words = sum(len(seg.get('original', '').split()) for seg in profanity_report)
        
        # Get unique profane words
        unique_profane_words = list(set(
            seg.get('original', '').lower() 
            for seg in profanity_report
        ))
        
        # Prepare detailed report with 350ms added to end timestamps
        profanity_details = []
        for i, item in enumerate(profanity_report, 1):
            profanity_details.append({
                'id': i,
                'start_time': round(item['start'], 2),
                'end_time': round(item['end'] + 0.35, 2),  # Add 350ms to end time
                'original_word': item['original'],
                'duration': round((item['end'] + 0.35) - item['start'], 2)
            })
        
        # Clean up extracted audio if it was created
        if audio_path != input_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except:
                pass
        
        return {
            'success': True,
            'total_words': total_words,
            'profane_segments': profane_segments,
            'profane_words': profane_words,
            'unique_profane_words': unique_profane_words,
            'profanity_percentage': round((profane_words / total_words * 100), 2) if total_words > 0 else 0,
            'profanity_details': profanity_details,
            'filename': os.path.basename(input_path)
        }
        
    except Exception as e:
        logger.error(f"Profanity detection failed: {e}")
        return {
            'success': False,
            'error': str(e),
            'filename': os.path.basename(input_path) if input_path else 'Unknown'
        }

def main():
    parser = argparse.ArgumentParser(description="Detect profanity in media files")
    parser.add_argument("input", help="Input video/audio file")
    args = parser.parse_args()

    try:
        result = detect_profanity(args.input)
        
        if result['success']:
            print(f"Profanity Analysis Report for {result['filename']}")
            print("="*50)
            print(f"Total words: {result['total_words']}")
            print(f"Profane segments: {result['profane_segments']}")
            print(f"Profane words: {result['profane_words']}")
            print(f"Profanity percentage: {result['profanity_percentage']}%")
            print(f"Unique profane words: {', '.join(result['unique_profane_words'])}")
            
            if result['profanity_details']:
                print("\nProfanity Details:")
                for detail in result['profanity_details']:
                    print(f"[{detail['start_time']}s-{detail['end_time']}s] {detail['original_word']}")
        else:
            print(f"Error: {result['error']}")
            
    except Exception as e:
        logger.error(f"Detection failed: {e}")

if __name__ == "__main__":
    main()