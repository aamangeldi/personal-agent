#!/usr/bin/env python3
"""
Text-to-Speech module using OpenAI TTS API.
Converts text to audio with support for multiple languages and voices.
"""
import os
from pathlib import Path
from openai import OpenAI
from typing import Optional


class TextToSpeech:
    """Handles text-to-speech synthesis using OpenAI TTS."""

    # Available voices: alloy, echo, fable, onyx, nova, shimmer
    VOICES = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Text-to-Speech module.

        Args:
            api_key: OpenAI API key. If None, reads from OPENAI_API_KEY env var
        """
        # Use OpenAI API key
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not provided. Set OPENAI_API_KEY environment variable.")

        self.client = OpenAI(api_key=self.api_key)

    def synthesize(
        self,
        text: str,
        output_path: str,
        voice: str = "alloy",
        model: str = "tts-1"
    ) -> str:
        """
        Convert text to speech and save as audio file.

        Args:
            text: Text to convert to speech
            output_path: Path where audio file will be saved (MP3 format)
            voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
            model: TTS model to use (tts-1 or tts-1-hd for higher quality)

        Returns:
            Path to the generated audio file

        Raises:
            ValueError: If voice is invalid or text is empty
            Exception: If synthesis fails
        """
        # Validate inputs
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        if voice not in self.VOICES:
            raise ValueError(f"Invalid voice. Choose from: {', '.join(self.VOICES)}")

        # Ensure output directory exists
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            print(f"Synthesizing speech with voice '{voice}'...")

            # Generate speech
            response = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text
            )

            # Save to file
            response.stream_to_file(output_file)

            print(f"Audio saved to: {output_path}")
            return str(output_file)

        except Exception as e:
            raise Exception(f"Speech synthesis failed: {str(e)}")

    def synthesize_bilingual(
        self,
        english_text: str,
        russian_text: str,
        output_dir: str = "output",
        english_voice: str = "alloy",
        russian_voice: str = "nova"
    ) -> dict:
        """
        Generate separate audio files for English and Russian text.

        Args:
            english_text: English text to synthesize
            russian_text: Russian text to synthesize
            output_dir: Directory to save audio files
            english_voice: Voice for English speech
            russian_voice: Voice for Russian speech

        Returns:
            dict with keys 'english' and 'russian' containing file paths
        """
        results = {}

        # Generate English audio
        english_path = os.path.join(output_dir, "response_english.mp3")
        results['english'] = self.synthesize(
            english_text,
            english_path,
            voice=english_voice
        )

        # Generate Russian audio
        russian_path = os.path.join(output_dir, "response_russian.mp3")
        results['russian'] = self.synthesize(
            russian_text,
            russian_path,
            voice=russian_voice
        )

        return results


def main():
    """Test the text-to-speech module."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python text_to_speech.py <text> [output_file] [voice]")
        print("Example: python text_to_speech.py 'Hello world' output.mp3 alloy")
        print(f"Available voices: {', '.join(TextToSpeech.VOICES)}")
        sys.exit(1)

    text = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.mp3"
    voice = sys.argv[3] if len(sys.argv) > 3 else "alloy"

    # Initialize TTS
    try:
        tts = TextToSpeech()

        # Synthesize
        result = tts.synthesize(text, output_file, voice=voice)
        print("\n" + "="*50)
        print("SPEECH SYNTHESIS COMPLETE")
        print("="*50)
        print(f"Audio file: {result}")
        print("="*50)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
