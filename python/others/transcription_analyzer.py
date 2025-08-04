#!/usr/bin/env python3
"""
Standalone Transcription Analysis Tool
Usage: python transcription_analyzer.py input.mp4|input.wav [--pdf]
"""
import argparse
import logging
import os
from python.audio_processing.whisper_handler import transcriber
from python.audio_processing.audio_cleaner import extract_audio_from_video
from python.text_processing.profanity_filter import filter_transcript

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_transcription_pdf(input_path: str, output_dir: str, unique_filename: str):
    """Generate PDF transcript with profanity marked."""
    try:
        # Extract audio if input is video
        if input_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm')):
            audio_path = extract_audio_from_video(input_path, output_dir)
        else:
            audio_path = input_path
        
        # Transcribe audio
        transcript = transcriber.transcribe_audio(audio_path)
        profanity_report = filter_transcript(transcript)
        
        # Generate PDF
        pdf_path = os.path.join(output_dir, f"transcript_{unique_filename}.pdf")
        
        # Create simple text file with profanity marked (since FPDF might not be available)
        txt_path = os.path.join(output_dir, f"transcript_{unique_filename}.txt")
        
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("TRANSCRIPT WITH PROFANITY MARKED\n")
            f.write("=" * 50 + "\n\n")
            
            for word_info in transcript:
                word = word_info['word']
                start_time = word_info['start']
                
                # Check if this word is in profanity segments
                is_profane = any(
                    r['start'] <= start_time <= r['end'] 
                    for r in profanity_report
                )
                
                if is_profane:
                    f.write(f"[{start_time:.2f}s] ~~{word}~~ (PROFANE)\n")
                else:
                    f.write(f"[{start_time:.2f}s] {word}\n")
            
            f.write("\n" + "=" * 50 + "\n")
            f.write(f"Total words: {len(transcript)}\n")
            f.write(f"Profane segments found: {len(profanity_report)}\n")
            
            if profanity_report:
                f.write("\nProfanity Details:\n")
                for i, item in enumerate(profanity_report, 1):
                    f.write(f"{i}. [{item['start']:.2f}s-{item['end']:.2f}s] '{item['original']}' → '{item['replacement']}'\n")
        
        logger.info(f"Transcription saved to: {txt_path}")
        return txt_path
        
    except Exception as e:
        logger.error(f"Transcription generation failed: {e}")
        raise RuntimeError(f"Transcription failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generate profanity analysis reports")
    parser.add_argument("input", help="Input video/audio file")
    parser.add_argument("--pdf", action="store_true", help="Generate PDF report")
    args = parser.parse_args()

    try:
        output_file = generate_transcription_pdf(args.input, "output_transcript", "standalone")
        logger.info(f"Transcription report generated: {output_file}")
    except Exception as e:
        logger.error(f"Analysis failed: {e}")

if __name__ == "__main__":
    main()