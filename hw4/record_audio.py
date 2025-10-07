#!/usr/bin/env python3
"""
Audio recording module for capturing microphone input.
Uses sounddevice and soundfile for cross-platform audio recording.
"""
import sounddevice as sd
import soundfile as sf
import numpy as np
from pathlib import Path
from typing import Optional


class AudioRecorder:
    """Handles microphone audio recording."""

    def __init__(self, sample_rate: int = 16000):
        """
        Initialize the audio recorder.

        Args:
            sample_rate: Sample rate for recording (default: 16000 Hz, optimal for Whisper)
        """
        self.sample_rate = sample_rate
        self.channels = 1  # Mono audio

    def record(
        self,
        duration: Optional[float] = None,
        output_path: str = "recorded_audio.wav",
        countdown: int = 3
    ) -> str:
        """
        Record audio from microphone.

        Args:
            duration: Recording duration in seconds. If None, press Enter to stop
            output_path: Path to save the recording
            countdown: Countdown seconds before starting recording

        Returns:
            Path to the saved audio file
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        print("\n" + "="*60)
        print("🎤 MICROPHONE RECORDING")
        print("="*60)

        # Countdown
        if countdown > 0:
            print(f"\nRecording will start in:")
            for i in range(countdown, 0, -1):
                print(f"  {i}...")
                import time
                time.sleep(1)

        if duration:
            print(f"\n🔴 Recording for {duration} seconds...")
            print("Speak now!\n")

            # Record for specified duration
            recording = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype='float32'
            )
            sd.wait()  # Wait until recording is finished

        else:
            print("\n🔴 Recording... (Press Enter to stop)")
            print("Speak now!\n")

            # Record until user presses Enter
            recording = []

            def callback(indata, frames, time, status):
                """Callback for streaming audio."""
                if status:
                    print(f"Status: {status}")
                recording.append(indata.copy())

            # Start recording stream
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                callback=callback,
                dtype='float32'
            ):
                input("Press Enter to stop recording...\n")

            # Concatenate all recorded chunks
            recording = np.concatenate(recording, axis=0)

        # Save to file
        sf.write(output_file, recording, self.sample_rate)

        print(f"✅ Recording saved to: {output_path}")
        print("="*60)

        return str(output_file)

    def record_with_vad(
        self,
        output_path: str = "recorded_audio.wav",
        silence_duration: float = 2.0,
        countdown: int = 3
    ) -> str:
        """
        Record audio with voice activity detection (stops after silence).

        Args:
            output_path: Path to save the recording
            silence_duration: Duration of silence (seconds) before auto-stop
            countdown: Countdown seconds before starting recording

        Returns:
            Path to the saved audio file
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        print("\n" + "="*60)
        print("🎤 VOICE-ACTIVATED RECORDING")
        print("="*60)
        print(f"\nRecording will auto-stop after {silence_duration}s of silence")

        # Countdown
        if countdown > 0:
            print(f"\nRecording will start in:")
            for i in range(countdown, 0, -1):
                print(f"  {i}...")
                import time
                time.sleep(1)

        print("\n🔴 Recording... (Speak now, will stop after silence)")

        recording = []
        silence_samples = int(silence_duration * self.sample_rate)
        silence_threshold = 0.01  # Amplitude threshold for silence
        consecutive_silent = 0

        def callback(indata, frames, time, status):
            nonlocal consecutive_silent
            if status:
                print(f"Status: {status}")

            recording.append(indata.copy())

            # Check if current frame is silent
            if np.max(np.abs(indata)) < silence_threshold:
                consecutive_silent += len(indata)
            else:
                consecutive_silent = 0

        # Start recording stream
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=callback,
            dtype='float32'
        ):
            # Wait until enough silence is detected
            while consecutive_silent < silence_samples:
                sd.sleep(100)  # Check every 100ms

        # Concatenate all recorded chunks
        recording = np.concatenate(recording, axis=0)

        # Save to file
        sf.write(output_file, recording, self.sample_rate)

        print(f"\n✅ Recording complete! Saved to: {output_path}")
        print("="*60)

        return str(output_file)


def main():
    """Test the audio recorder."""
    import sys

    recorder = AudioRecorder()

    if len(sys.argv) > 1 and sys.argv[1] == "--vad":
        # Use voice activity detection
        output = recorder.record_with_vad("test_recording.wav")
    elif len(sys.argv) > 1:
        # Record for specified duration
        try:
            duration = float(sys.argv[1])
            output = recorder.record(duration=duration, output_path="test_recording.wav")
        except ValueError:
            print("Usage: python record_audio.py [duration_in_seconds | --vad]")
            sys.exit(1)
    else:
        # Record until Enter is pressed
        output = recorder.record(output_path="test_recording.wav")

    print(f"\nRecorded audio saved to: {output}")


if __name__ == "__main__":
    main()
