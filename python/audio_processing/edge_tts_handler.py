import os
import subprocess
import edge_tts
import asyncio
import logging
import math
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VOICE_MAP = {
    "male": "en-US-GuyNeural",
    "female": "en-US-JennyNeural"
}

async def async_generate_speech(
    text: str,
    output_path: str,
    gender: str,
    target_duration: float = None  # New: Target duration in seconds
) -> None:
    """Generate TTS audio with precise duration control"""
    try:
        voice = VOICE_MAP.get(gender.lower(), VOICE_MAP["female"])
        
        # First generate without rate control to get natural duration
        communicate = edge_tts.Communicate(text, voice)
        temp_path = str(Path(output_path).with_suffix('.temp.mp3'))
        await communicate.save(temp_path)
        
        # Calculate current duration
        duration = float(subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", temp_path
        ], stdout=subprocess.PIPE, text=True).stdout.strip())
        
        # If no target duration needed, just use natural speech
        if target_duration is None:
            # Remove output file if it exists
            if os.path.exists(output_path):
                os.remove(output_path)
            os.rename(temp_path, output_path)
            return
            
        # Calculate required rate adjustment (+/- 20% limit for natural sound)
        rate_adjustment = min(max(duration / target_duration, 0.8), 1.2)
        rate_percent = int(round(rate_adjustment * 100))
        
        # Regenerate with rate control
        communicate = edge_tts.Communicate(
            text, 
            voice,
            rate=f"+{rate_percent}%" if rate_percent >= 100 else f"-{100-rate_percent}%"
        )
        # Remove output file if it exists
        if os.path.exists(output_path):
            os.remove(output_path)
        await communicate.save(output_path)
        
        # Final duration check and padding if needed
        final_duration = float(subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", output_path
        ], stdout=subprocess.PIPE, text=True).stdout.strip())
        
        if final_duration < target_duration:
            subprocess.run([
                "ffmpeg", "-y",
                "-i", output_path,
                "-af", f"apad=pad_dur={target_duration-final_duration}",
                "-c:a", "libmp3lame", "-q:a", "2",
                output_path + ".padded.mp3"
            ], check=True)
            os.replace(output_path + ".padded.mp3", output_path)
            
        os.unlink(temp_path)
        logger.info(f"Generated TTS: '{text}' → {output_path} (target: {target_duration}s, actual: {final_duration}s)")

    except Exception as e:
        logger.error(f"TTS generation failed: {e}")
        if Path(temp_path).exists():
            os.unlink(temp_path)
        raise RuntimeError(f"EdgeTTS error: {e}")

def generate_speech(
    text: str,
    output_path: str,
    gender: str,
    target_duration: float = None
) -> None:
    """Sync wrapper with duration control"""
    try:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    loop.run_until_complete(async_generate_speech(
        text, output_path, gender, target_duration
    ))