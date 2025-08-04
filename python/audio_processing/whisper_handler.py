from typing import List, Dict, Any
from pathlib import Path
import logging
from faster_whisper import WhisperModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhisperTranscriber:
    """Handles audio transcription using FasterWhisper with word-level timestamps."""
    
    def __init__(self, model_size: str = "base", compute_type: str = "int8"):
        self.model = WhisperModel(model_size, compute_type=compute_type, cpu_threads=1)
        logger.info(f"Loaded Whisper model: {model_size} with {compute_type} precision")

    def transcribe_audio(self, audio_path: str, language: str = None) -> List[Dict[str, Any]]:
        """
        Transcribe audio and return words with timestamps.
        
        Args:
            audio_path (str): Path to audio file (WAV/MP3).
            language (str, optional): Force language (e.g., "en"). Faster if known.
        
        Returns:
            List[Dict]: [{"word": str, "start": float, "end": float}]
        
        Raises:
            FileNotFoundError: If audio file missing.
            RuntimeError: Transcription failed.
        """
        if not Path(audio_path).exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        try:
            segments, _ = self.model.transcribe(
                audio_path,
                language=language,
                word_timestamps=True
            )
            transcript = [
                {"word": word.word, "start": word.start, "end": word.end}
                for segment in segments
                for word in segment.words
            ]
            logger.info(f"Transcribed {len(transcript)} words from {audio_path}")
            return transcript

        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise RuntimeError(f"Whisper error: {e}")

# Singleton instance (avoids reloading model)
transcriber = WhisperTranscriber()