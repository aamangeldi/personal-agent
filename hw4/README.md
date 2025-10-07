## Demo
[https://youtu.be/fxPTb5ZxR9Y](https://youtu.be/fxPTb5ZxR9Y)

## Setting up:
1. Create a venv and sync the dependencies:
    ```
    uv venv
    source .venv/bin/activate
    uv sync
    ```

2. Run the demo:
    ```
    python demo_voice_agent.py
    ```

## Short write-up

This project implements a fully voice-interactive bilingual personal agent that can engage in natural conversations about Amir's background, experience, and interests. The agent supports end-to-end voice interaction: from spoken questions to spoken responses in both English and Russian.

### Implementation Architecture

The system implements a complete voice interaction pipeline:

```
Voice Input → Whisper STT → CrewAI Agents → OpenAI TTS → Audio Playback
```

**Speech-to-Text**: OpenAI's Whisper (base model) transcribes audio with automatic language detection. Implemented in `speech_to_text.py`, supporting multiple formats (WAV, MP3, M4A).

**Audio Recording**: `sounddevice` library captures microphone input with voice activity detection (auto-stops after 2s silence). Configuration: 16kHz mono WAV optimized for Whisper.

**Agent Processing**: CrewAI orchestrates three Claude 3.5 Haiku agents in `amir_agent.py`:
  - Personal Representative: Responds as Amir (50-word limit)
  - Translator: Natural Russian translation (50-word limit)
  - Response Formatter: Combines bilingual output with clear labels

**Text-to-Speech**: OpenAI TTS-1 API generates MP3 audio files using different voices per language (English: "alloy", Russian: "nova") in `text_to_speech.py`.

**Demo Interface**: `demo_voice_agent.py` provides interactive mode with voice recording, automatic playback, and support for custom audio files.

### Example Run Analysis

**Input (Spoken)**: "Please introduce yourself."

**Processing Flow** (~8 seconds total):

1. **Audio Capture**: Voice activity detection recorded 2.3s, auto-stopped after 2s silence → `demo_output/recorded_question.wav`

2. **Speech Recognition** (~1.5s): Whisper detected English, transcribed: "Please introduce yourself."

3. **Agent Processing** (~5s): Three sequential tasks generated a 37-word English introduction (covering origin, education, work, interests), natural 36-word Russian translation, and formatted bilingual output.

4. **Speech Synthesis** (~1.5s): Generated two MP3 files with different voices (English 6.2s, Russian 5.8s) → `demo_output/response_english.mp3` and `demo_output/response_russian.mp3`, then auto-played both.

**Final Output (in text)**:

```
🇬🇧 English:
Hi, I'm Amir - originally from Kazakhstan, now a grad student at Harvard
studying engineering and business. Former software engineer at Twitch,
tennis enthusiast, and passionate about tech and startups.

🇷🇺 Russian:
Привет! Я Амир - родом из Казахстана, сейчас аспирант в Гарварде,
изучаю инженерное дело и бизнес. Бывший программист в Twitch,
люблю теннис и увлечен технологиями и стартапами.
```

### Key Insights and Observations

**1. Voice Activity Detection Effectiveness**
The 2-second silence threshold works well for natural speech patterns. It gives users enough time to pause and think without prematurely cutting off their question, while being responsive enough to feel natural.

**2. Conciseness Improves Voice UX**
The 50-word limit dramatically improved the user experience. Longer responses became tedious to listen to. The constraint forces the agent to prioritize the most relevant information, making the voice interaction feel more natural and conversational.

**3. Bilingual Output Quality**
The Russian translations are surprisingly natural. The translator agent doesn't just do literal word-for-word translation but adapts phrasing to sound natural in Russian (e.g., "grad student" → "аспирант" rather than a literal translation).

**4. Different Voices Enhance Clarity**
Using distinct voices for each language (alloy vs. nova) helps listeners mentally separate the two responses, especially useful for bilingual audiences who might prefer one language but appreciate hearing both.

**5. End-to-End Latency**
The total processing time (~8 seconds) is acceptable for this demo but could be optimized:
- Whisper base model on CPU: ~1.5s (could use GPU or smaller "tiny" model)
- CrewAI agent processing: ~5s (could optimize with caching or faster LLM)
- TTS generation: ~1.5s (minimal optimization potential)

### Future Enhancements

- **Streaming TTS**: Stream audio playback while generating to reduce perceived latency
- **GPU Acceleration**: Use GPU for Whisper inference on supported systems
- **Conversation Memory**: Maintain context across multiple questions in a session
- **Emotion Detection**: Analyze voice tone to adjust response style
- **Multi-turn Dialogue**: Support follow-up questions without re-recording
