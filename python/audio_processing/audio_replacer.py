import os
import shutil
import subprocess
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def replace_profanity_audio(
    original_audio: str,
    replacements: List[Dict[str, Any]],
    output_audio_file: str,
    temp_dir: str
) -> None:
    """Version that preserves space before words (no pre-cut) with 350ms post-cut"""
    original_audio = os.path.abspath(original_audio)
    output_audio_file = os.path.abspath(output_audio_file)
    temp_dir = os.path.abspath(temp_dir)
    
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    try:
        # Get original duration
        orig_duration = float(subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", original_audio
        ], stdout=subprocess.PIPE, text=True).stdout.strip())
        
        replacements.sort(key=lambda x: x["start"])
        concat_list = []
        last_end = 0.0
        
        for i, repl in enumerate(replacements):
            word_start = repl["start"]
            word_end = min(orig_duration, repl["end"] + 0.35)  # 350ms post-cut only
            
            # 1. Add clean segment before replacement (keep as WAV)
            if word_start > last_end:
                clean_seg = os.path.join(temp_dir, f"clean_{i}.wav")
                subprocess.run([
                    "ffmpeg", "-y",
                    "-i", original_audio,
                    "-ss", str(last_end),
                    "-to", str(word_start),
                    "-c:a", "pcm_s16le",  # Keep as WAV
                    "-ar", "44100",
                    "-ac", "2",
                    clean_seg
                ], check=True, stderr=subprocess.DEVNULL)
                concat_list.append(clean_seg)
            
            # 2. Process replacement (convert MP3 to WAV)
            repl_seg = os.path.join(temp_dir, f"repl_{i}.wav")
            # First get duration of replacement audio
            repl_duration = word_end - word_start
            subprocess.run([
                "ffmpeg", "-y",
                "-i", repl["replacement_audio"],
                "-t", str(repl_duration),
                "-af", "apad=pad_dur=0.35",
                "-c:a", "pcm_s16le",  # Convert to WAV
                "-ar", "44100",
                "-ac", "2",
                repl_seg
            ], check=True, stderr=subprocess.DEVNULL)
            concat_list.append(repl_seg)
            
            last_end = word_end
        
        # Add final segment (keep as WAV)
        if last_end < orig_duration:
            final_seg = os.path.join(temp_dir, "final.wav")
            subprocess.run([
                "ffmpeg", "-y",
                "-i", original_audio,
                "-ss", str(last_end),
                "-to", str(orig_duration),
                "-c:a", "pcm_s16le",
                "-ar", "44100",
                "-ac", "2",
                final_seg
            ], check=True, stderr=subprocess.DEVNULL)
            concat_list.append(final_seg)
        
        # Concatenate all WAV files
        with open(os.path.join(temp_dir, "list.txt"), "w") as f:
            for seg in concat_list:
                f.write(f"file '{os.path.abspath(seg)}'\n")
        
        # Change the last FFmpeg command in replace_profanity_audio() to:
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", os.path.join(temp_dir, "list.txt"),
            "-c:a", "pcm_s16le",
            "-ar", "48000",  # Match video standard
            "-ac", "2",
            output_audio_file
        ], check=True)

    except subprocess.CalledProcessError as e:
        logger.error(f"Processing failed: {e.stderr.decode('utf-8') if e.stderr else 'Unknown error'}")
        raise RuntimeError("Audio replacement failed")
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)