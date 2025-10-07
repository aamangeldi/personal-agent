#!/usr/bin/env python3
"""
Voice-enabled version of Amir's agent.
Extends the text-based agent with speech input/output capabilities.
"""
import os
import re
from pathlib import Path
from speech_to_text import SpeechToText
from text_to_speech import TextToSpeech
from amir_agent import create_amir_assistant


class VoiceAgent:
    """Voice-enabled wrapper for Amir's agent."""

    def __init__(
        self,
        stt_model_size: str = "base",
        output_dir: str = "voice_output"
    ):
        """
        Initialize the voice agent.

        Args:
            stt_model_size: Whisper model size for speech-to-text
            output_dir: Directory to save generated audio files
        """
        print("Initializing Voice Agent...")

        # Initialize speech modules
        self.stt = SpeechToText(model_size=stt_model_size)
        self.tts = TextToSpeech()

        # Initialize the text-based agent
        self.agent = create_amir_assistant()

        # Setup output directory
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        print(f"Voice Agent ready. Audio output: {self.output_dir}")

    def process_voice(
        self,
        audio_input_path: str,
        save_audio: bool = True
    ) -> dict:
        """
        Process voice input through the full pipeline:
        Audio → Text → Agent → Text → Audio

        Args:
            audio_input_path: Path to input audio file
            save_audio: Whether to generate and save TTS output

        Returns:
            dict containing:
                - 'transcription': Input transcription result
                - 'agent_response': Text response from agent
                - 'audio_files': Paths to generated audio (if save_audio=True)
        """
        result = {}

        # Step 1: Speech-to-Text
        print("\n" + "="*60)
        print("STEP 1: Converting speech to text...")
        print("="*60)

        transcription = self.stt.transcribe(audio_input_path)
        result['transcription'] = transcription

        print(f"Transcribed ({transcription['language']}): {transcription['text']}")

        # Step 2: Process through agent
        print("\n" + "="*60)
        print("STEP 2: Processing through Amir's agent...")
        print("="*60)

        agent_response = self.agent(transcription['text'])
        result['agent_response'] = agent_response

        print(f"Agent response:\n{agent_response}")

        # Step 3: Text-to-Speech (if requested)
        if save_audio:
            print("\n" + "="*60)
            print("STEP 3: Converting response to speech...")
            print("="*60)

            # Parse English and Russian parts from response
            english_text, russian_text = self._parse_bilingual_response(agent_response)

            audio_files = {}

            if english_text:
                english_path = str(self.output_dir / "response_english.mp3")
                self.tts.synthesize(english_text, english_path, voice="alloy")
                audio_files['english'] = english_path

            if russian_text:
                russian_path = str(self.output_dir / "response_russian.mp3")
                self.tts.synthesize(russian_text, russian_path, voice="nova")
                audio_files['russian'] = russian_path

            result['audio_files'] = audio_files

            print("\n" + "="*60)
            print("Audio files generated:")
            for lang, path in audio_files.items():
                print(f"  {lang.capitalize()}: {path}")
            print("="*60)

        return result

    def _parse_bilingual_response(self, response: str) -> tuple[str, str]:
        """
        Parse English and Russian sections from agent response.

        The agent typically formats responses with clear language markers.
        This method attempts to extract both parts.

        Args:
            response: Full agent response text

        Returns:
            Tuple of (english_text, russian_text)
        """
        # Try to find sections marked with language headers
        # Common patterns: "English:", "Russian:", "---", etc.

        # Simple heuristic: Split on common markers
        parts = response.split('\n\n')

        english_text = ""
        russian_text = ""

        for part in parts:
            part = part.strip()
            if not part:
                continue

            # Check if this part contains Cyrillic (Russian)
            has_cyrillic = bool(re.search('[а-яА-Я]', part))

            if has_cyrillic:
                # Remove any language markers
                cleaned = re.sub(r'^(Russian|Русский):?\s*', '', part, flags=re.IGNORECASE)
                russian_text += cleaned + " "
            else:
                # Remove any language markers
                cleaned = re.sub(r'^(English|Английский):?\s*', '', part, flags=re.IGNORECASE)
                english_text += cleaned + " "

        # If we couldn't split properly, just use the whole response for English
        if not english_text and not russian_text:
            english_text = response

        return english_text.strip(), russian_text.strip()

    def process_text(self, text_input: str) -> str:
        """
        Process text input (bypass STT, still useful for testing).

        Args:
            text_input: Text question/message

        Returns:
            Agent's text response
        """
        return self.agent(text_input)


def main():
    """Command-line interface for the voice agent."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python voice_agent.py <audio_file>")
        print("Example: python voice_agent.py input.wav")
        sys.exit(1)

    audio_file = sys.argv[1]

    # Initialize voice agent
    try:
        agent = VoiceAgent(stt_model_size="base")

        # Process voice input
        result = agent.process_voice(audio_file, save_audio=True)

        print("\n" + "="*60)
        print("PROCESSING COMPLETE")
        print("="*60)
        print(f"\nInput (transcribed): {result['transcription']['text']}")
        print(f"\nAgent response:\n{result['agent_response']}")

        if 'audio_files' in result:
            print("\nGenerated audio files:")
            for lang, path in result['audio_files'].items():
                print(f"  {lang}: {path}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
