#!/usr/bin/env python3
"""
Demo script for the voice-enabled Amir agent.
This script demonstrates the full voice interaction pipeline with sample questions.
"""
import os
import sys
from pathlib import Path
from voice_agent import VoiceAgent


def create_sample_audio_if_needed():
    """
    Creates a sample audio file for testing if one doesn't exist.
    Uses text-to-speech to create a test question.
    """
    from text_to_speech import TextToSpeech

    sample_dir = Path("sample_audio")
    sample_dir.mkdir(exist_ok=True)

    sample_file = sample_dir / "sample_question.mp3"

    if not sample_file.exists():
        print("Creating sample audio file for testing...")
        tts = TextToSpeech()

        # Create a sample question about Amir
        sample_text = "Tell me about your background and experience in software engineering."

        tts.synthesize(sample_text, str(sample_file), voice="echo")
        print(f"Sample audio created: {sample_file}")

    return str(sample_file)


def run_demo():
    """Run the voice agent demonstration."""
    print("="*70)
    print("AMIR VOICE AGENT DEMONSTRATION")
    print("="*70)
    print("\nThis demo shows the full voice interaction pipeline:")
    print("  1. Audio input (speech)")
    print("  2. Speech-to-text transcription")
    print("  3. Agent processing (CrewAI)")
    print("  4. Text-to-speech synthesis (bilingual)")
    print()

    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("ERROR: Please set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)

    # Initialize voice agent
    print("Initializing voice agent...")
    agent = VoiceAgent(stt_model_size="base", output_dir="demo_output")

    # Get or create sample audio
    sample_audio = create_sample_audio_if_needed()

    print(f"\nProcessing audio file: {sample_audio}")
    print("="*70)

    # Process the voice input
    try:
        result = agent.process_voice(sample_audio, save_audio=True)

        # Display results
        print("\n" + "="*70)
        print("DEMO RESULTS")
        print("="*70)

        print("\n📝 TRANSCRIPTION")
        print(f"Language: {result['transcription']['language']}")
        print(f"Text: {result['transcription']['text']}")

        print("\n🤖 AGENT RESPONSE")
        print(result['agent_response'])

        if 'audio_files' in result:
            print("\n🔊 GENERATED AUDIO FILES")
            for lang, path in result['audio_files'].items():
                print(f"  {lang.capitalize()}: {path}")

        print("\n" + "="*70)
        print("DEMO COMPLETE!")
        print("="*70)
        print("\nTo test with your own audio:")
        print("  python voice_agent.py <your_audio_file>")
        print()
        print("Or use the demo script with a custom file:")
        print("  python demo_voice_agent.py <your_audio_file>")

    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def run_custom_demo(audio_file: str):
    """
    Run demo with a custom audio file.

    Args:
        audio_file: Path to audio file to process
    """
    if not Path(audio_file).exists():
        print(f"Error: Audio file not found: {audio_file}")
        sys.exit(1)

    print("="*70)
    print("AMIR VOICE AGENT - CUSTOM AUDIO")
    print("="*70)

    # Initialize voice agent
    agent = VoiceAgent(stt_model_size="base", output_dir="demo_output")

    # Process the audio
    result = agent.process_voice(audio_file, save_audio=True)

    # Display results
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)

    print(f"\n📝 Transcription: {result['transcription']['text']}")
    print(f"\n🤖 Response:\n{result['agent_response']}")

    if 'audio_files' in result:
        print("\n🔊 Audio outputs:")
        for lang, path in result['audio_files'].items():
            print(f"  {lang}: {path}")


def main():
    """Main entry point for the demo."""
    if len(sys.argv) > 1:
        # Run with custom audio file
        run_custom_demo(sys.argv[1])
    else:
        # Run default demo
        run_demo()


if __name__ == "__main__":
    main()
