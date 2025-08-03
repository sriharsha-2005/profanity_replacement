#!/usr/bin/env python3
"""
Standalone Transcription Analysis Tool
Usage: python transcription_analyzer.py input.mp4|input.wav [--pdf]
"""
import argparse
import logging
from python.audio_processing.whisper_handler import transcriber
from python.text_processing.profanity_filter import filter_transcript
from fpdf import FPDF  # Requires PyFPDF

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_pdf(transcript, report, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Profanity Analysis Report", ln=1, align="C")
    
    for word in transcript:
        if any(r['start'] <= word['start'] <= r['end'] for r in report):
            pdf.set_text_color(255,0,0)
            pdf.cell(200, 10, txt=f"[{word['start']:.2f}s] ~~{word['word']}~~", ln=1)
        else:
            pdf.set_text_color(0,0,0)
            pdf.cell(200, 10, txt=f"[{word['start']:.2f}s] {word['word']}", ln=1)
    
    pdf.output(filename)

def main():
    parser = argparse.ArgumentParser(description="Generate profanity analysis reports")
    parser.add_argument("input", help="Input video/audio file")
    parser.add_argument("--pdf", action="store_true", help="Generate PDF report")
    args = parser.parse_args()

    try:
        transcript = transcriber.transcribe_audio(args.input)
        report = filter_transcript(transcript)
        
        if args.pdf:
            pdf_path = f"{args.input}_report.pdf"
            generate_pdf(transcript, report, pdf_path)
            logger.info(f"PDF report generated: {pdf_path}")
        else:
            print("Full Transcript with Profanity Marked:")
            print("="*50)
            for word in transcript:
                if any(r['start'] <= word['start'] <= r['end'] for r in report):
                    print(f"[{word['start']:.2f}s] ~~{word['word']}~~")
                else:
                    print(f"[{word['start']:.2f}s] {word['word']}")
    except Exception as e:
        logger.error(f"Analysis failed: {e}")

if __name__ == "__main__":
    main()