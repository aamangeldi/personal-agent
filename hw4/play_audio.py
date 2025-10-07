#!/usr/bin/env python3
"""
Audio playback module for playing audio files.
Uses sounddevice and soundfile for cross-platform audio playback.
"""
import sounddevice as sd
import soundfile as sf
from pathlib import Path


def play_audio(file_path: str, wait: bool = True):
    """
    Play an audio file.

    Args:
        file_path: Path to the audio file
        wait: If True, wait until playback is complete before returning
    """
    audio_file = Path(file_path)
    if not audio_file.exists():
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    # Read the audio file
    data, sample_rate = sf.read(audio_file)

    # Play the audio
    sd.play(data, sample_rate)

    # Wait until playback is complete if requested
    if wait:
        sd.wait()


def main():
    """Test the audio playback."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python play_audio.py <audio_file>")
        sys.exit(1)

    audio_file = sys.argv[1]
    print(f"Playing: {audio_file}")
    play_audio(audio_file)
    print("Playback complete!")


if __name__ == "__main__":
    main()
