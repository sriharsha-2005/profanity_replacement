#!/usr/bin/env python3
"""
Standalone Transcription Analysis Tool
Usage: python transcription_analyzer.py input.mp4|input.wav [--pdf]
"""
import argparse
import logging
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from python.audio_processing.whisper_handler import transcriber
from python.audio_processing.audio_cleaner import extract_audio_from_video
from python.text_processing.profanity_filter import filter_transcript

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_pdf_transcript(transcript, profanity_report, output_path, filename):
    """Create a professional PDF transcript with profanity highlighting."""
    try:
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkred
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_LEFT
        )
        
        profane_style = ParagraphStyle(
            'ProfaneStyle',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_LEFT,
            textColor=colors.red,
            backColor=colors.yellow
        )
        
        # Add title
        story.append(Paragraph("TRANSCRIPT WITH PROFANITY ANALYSIS", title_style))
        story.append(Spacer(1, 12))
        
        # Add file information
        story.append(Paragraph(f"File: {filename}", subtitle_style))
        story.append(Spacer(1, 12))
        
        # Add summary statistics
        total_words = len(transcript)
        profane_segments = len(profanity_report)
        profane_words = sum(len(seg.get('original', '').split()) for seg in profanity_report)
        profanity_percentage = round((profane_words / total_words * 100), 2) if total_words > 0 else 0
        
        summary_data = [
            ['Total Words', str(total_words)],
            ['Profane Segments', str(profane_segments)],
            ['Profane Words', str(profane_words)],
            ['Profanity Percentage', f"{profanity_percentage}%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 1*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(Paragraph("Summary Statistics", subtitle_style))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Add transcript with profanity highlighting
        story.append(Paragraph("Detailed Transcript", subtitle_style))
        story.append(Spacer(1, 12))
        
        # Create a list to track profanity timestamps
        profanity_timestamps = []
        for seg in profanity_report:
            profanity_timestamps.append((seg['start'], seg['end']))
        
        # Process transcript with timestamps
        current_time = 0
        for word_info in transcript:
            word = word_info['word']
            start_time = word_info['start']
            end_time = word_info['end']
            
            # Check if this word is in a profanity segment
            is_profane = any(
                start <= start_time <= end 
                for start, end in profanity_timestamps
            )
            
            # Format timestamp
            timestamp = f"[{start_time:.2f}s-{end_time:.2f}s]"
            
            if is_profane:
                text = f"{timestamp} ~~{word}~~ (PROFANE)"
                story.append(Paragraph(text, profane_style))
            else:
                text = f"{timestamp} {word}"
                story.append(Paragraph(text, normal_style))
        
        story.append(Spacer(1, 20))
        
        # Add profanity details if any found
        if profanity_report:
            story.append(Paragraph("Profanity Details", subtitle_style))
            story.append(Spacer(1, 12))
            
            # Create profanity details table
            profanity_data = [['#', 'Original Word', 'Time Range', 'Duration']]
            for i, item in enumerate(profanity_report, 1):
                duration = item['end'] - item['start']
                profanity_data.append([
                    str(i),
                    item['original'],
                    f"{item['start']:.2f}s - {item['end']:.2f}s",
                    f"{duration:.2f}s"
                ])
            
            profanity_table = Table(profanity_data, colWidths=[0.5*inch, 2*inch, 1.5*inch, 1*inch])
            profanity_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.red),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9)
            ]))
            
            story.append(profanity_table)
        else:
            story.append(Paragraph("No profanity detected in this content.", normal_style))
        
        # Build PDF
        doc.build(story)
        logger.info(f"PDF transcript created successfully: {output_path}")
        
    except Exception as e:
        logger.error(f"PDF creation failed: {e}")
        raise RuntimeError(f"PDF generation error: {e}")

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
        
        # Create PDF with proper formatting
        create_pdf_transcript(transcript, profanity_report, pdf_path, os.path.basename(input_path))
        
        logger.info(f"Transcription PDF saved to: {pdf_path}")
        return pdf_path
        
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