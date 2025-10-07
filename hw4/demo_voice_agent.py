#!/usr/bin/env python3
"""
Demo script for the voice-enabled Amir agent.
This script demonstrates the full voice interaction pipeline with live microphone input.
"""
import os
import sys
from pathlib import Path
from voice_agent import VoiceAgent
from record_audio import AudioRecorder


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


def run_interactive_demo():
    """Run the interactive voice agent demonstration with live microphone input."""
    print("="*70)
    print("AMIR VOICE AGENT - INTERACTIVE MODE")
    print("="*70)
    print("\nThis demo shows the full voice interaction pipeline:")
    print("  1. 🎤 Record your question using microphone")
    print("  2. 📝 Speech-to-text transcription (Whisper)")
    print("  3. 🤖 Agent processing (CrewAI)")
    print("  4. 🔊 Text-to-speech synthesis (bilingual)")
    print()

    # Check for API keys
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("ERROR: Please set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: Please set OPENAI_API_KEY environment variable")
        sys.exit(1)

    # Initialize voice agent and recorder
    print("Initializing voice agent...")
    agent = VoiceAgent(stt_model_size="base", output_dir="demo_output")
    recorder = AudioRecorder()

    # Record audio from microphone
    print("\n" + "="*70)
    print("READY TO RECORD YOUR QUESTION")
    print("="*70)
    print("\nYou can ask Amir about:")
    print("  • His background and experience")
    print("  • His work at Amazon, Twitch, or startups")
    print("  • His studies at Harvard")
    print("  • Any other topic!")
    print()

    input("Press Enter when you're ready to record your question...")

    # Record with voice activity detection (auto-stops after silence)
    audio_file = recorder.record_with_vad(
        output_path="demo_output/recorded_question.wav",
        silence_duration=2.0
    )

    print("\n" + "="*70)
    print("PROCESSING YOUR QUESTION")
    print("="*70)

    # Process the voice input
    try:
        result = agent.process_voice(audio_file, save_audio=True)

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
        print("\n💡 The audio responses have been saved:")
        print(f"  • English: {result['audio_files']['english']}")
        print(f"  • Russian: {result['audio_files']['russian']}")
        print("\nYou can play them with any audio player!")

    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def run_demo():
    """Run the voice agent demonstration with sample audio."""
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
        if sys.argv[1] == "--interactive" or sys.argv[1] == "-i":
            # Run interactive demo with microphone
            run_interactive_demo()
        else:
            # Run with custom audio file
            run_custom_demo(sys.argv[1])
    else:
        # Show menu
        print("="*70)
        print("AMIR VOICE AGENT")
        print("="*70)
        print("\nChoose a mode:")
        print("  1. Interactive mode (record from microphone)")
        print("  2. Sample audio demo")
        print()

        choice = input("Enter choice (1 or 2): ").strip()

        if choice == "1":
            run_interactive_demo()
        elif choice == "2":
            run_demo()
        else:
            print("Invalid choice. Exiting.")
            sys.exit(1)


if __name__ == "__main__":
    main()
