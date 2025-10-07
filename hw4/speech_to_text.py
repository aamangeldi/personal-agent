#!/usr/bin/env python3
"""
Speech-to-Text module using OpenAI Whisper.
Converts audio files to text with support for multiple languages.
"""
import os
import whisper
from pathlib import Path
from typing import Optional


class SpeechToText:
    """Handles speech-to-text transcription using Whisper."""

    def __init__(self, model_size: str = "base"):
        """
        Initialize the Speech-to-Text module.

        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
                       Larger models are more accurate but slower.
        """
        self.model_size = model_size
        self.model = None
        print(f"Initializing Whisper model: {model_size}")

    def _load_model(self):
        """Lazy load the Whisper model."""
        if self.model is None:
            self.model = whisper.load_model(self.model_size)

    def transcribe(
        self,
        audio_path: str,
        language: Optional[str] = None
    ) -> dict:
        """
        Transcribe audio file to text.

        Args:
            audio_path: Path to audio file (supports WAV, MP3, M4A, etc.)
            language: Optional language code (e.g., 'en', 'ru').
                     If None, language is auto-detected.

        Returns:
            dict with keys:
                - 'text': Transcribed text
                - 'language': Detected/specified language
                - 'segments': Detailed transcription segments

        Raises:
            FileNotFoundError: If audio file doesn't exist
            Exception: If transcription fails
        """
        # Validate file exists
        audio_file = Path(audio_path)
        if not audio_file.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        # Load model if needed
        self._load_model()

        try:
            # Transcribe with optional language specification
            print(f"Transcribing: {audio_path}")
            options = {}
            if language:
                options['language'] = language

            result = self.model.transcribe(str(audio_file), **options)

            print(f"Transcription complete. Detected language: {result['language']}")

            return {
                'text': result['text'].strip(),
                'language': result['language'],
                'segments': result.get('segments', [])
            }

        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")


def main():
    """Test the speech-to-text module."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python speech_to_text.py <audio_file> [language]")
        print("Example: python speech_to_text.py recording.wav en")
        sys.exit(1)

    audio_file = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else None

    # Initialize STT
    stt = SpeechToText(model_size="base")

    # Transcribe
    try:
        result = stt.transcribe(audio_file, language=language)
        print("\n" + "="*50)
        print("TRANSCRIPTION RESULT")
        print("="*50)
        print(f"Language: {result['language']}")
        print(f"Text: {result['text']}")
        print("="*50)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
