# HW4: Voice-Enabled Agent - Implementation Write-up

**Author:** Amir Amangeldi
**Date:** [Add date]
**Video Demo:** [Add YouTube link]

---

## 1. Implementation Overview

This project extends the CrewAI-based personal agent from HW1-3 by adding voice interaction capabilities. The system now supports a complete voice-to-voice interaction pipeline.

### Architecture

The implementation consists of four main components:

1. **Speech-to-Text Module** (`speech_to_text.py`)
   - Library: OpenAI Whisper
   - Model: Base (configurable: tiny, base, small, medium, large)
   - Features: Automatic language detection, multilingual support

2. **Text-to-Speech Module** (`text_to_speech.py`)
   - Library: OpenAI TTS API
   - Voices: Multiple options (alloy, echo, fable, onyx, nova, shimmer)
   - Features: Bilingual output generation (English & Russian)

3. **Voice Agent** (`voice_agent.py`)
   - Orchestrates the full pipeline: Audio → STT → Agent → TTS → Audio
   - Handles bilingual response parsing
   - Manages file I/O and output organization

4. **Base Agent** (`amir_agent.py`)
   - Original CrewAI-based agent (unchanged)
   - Multi-agent system with personal assistant, translator, and formatter
   - Bilingual response generation

### Data Flow

```
User Audio Input
    ↓
[Speech-to-Text] → Transcribed Text
    ↓
[Amir Agent] → Bilingual Response (English + Russian)
    ↓
[Response Parser] → Separate English/Russian Text
    ↓
[Text-to-Speech] → Audio Files (English + Russian)
    ↓
Output Audio Files
```

---

## 2. Technology Stack

### Libraries & APIs Used

| Component | Library/API | Version | Purpose |
|-----------|-------------|---------|---------|
| STT | OpenAI Whisper | Latest | Speech-to-text transcription |
| TTS | OpenAI TTS API | 1.0+ | Text-to-speech synthesis |
| Agent | CrewAI | 0.201.1 | Multi-agent orchestration |
| LLM | Claude (Anthropic) | Haiku 3.5 | Language model for agent |
| Audio | soundfile, pydub | Latest | Audio processing utilities |

### Key Design Decisions

1. **Whisper for STT**: Chosen for robust multilingual support (critical for Russian translation feature) and offline capability.

2. **OpenAI TTS API**: Selected for high-quality neural voices and simple API integration. Alternative: pyttsx3 for offline use.

3. **Bilingual Audio Output**: Generate separate audio files for English and Russian responses rather than combining them, giving users flexibility to choose which language to listen to.

4. **File-based Interaction**: Using file I/O rather than real-time streaming for simplicity and reliability in this prototype.

---

## 3. Example Run Walkthrough

### Input
**Audio File:** `sample_question.mp3`
**Question (spoken):** "Tell me about your background and experience in software engineering."

### Processing Steps

#### Step 1: Speech-to-Text Transcription
```
Transcribing: sample_audio/sample_question.mp3
Detected language: en
Transcribed text: "Tell me about your background and experience in software engineering."
```

#### Step 2: Agent Processing
The agent processes the question through three specialized agents:

1. **Personal Assistant Agent**: Generates authentic response about Amir's background
2. **Translator Agent**: Translates the response to Russian
3. **Formatter Agent**: Combines both responses with clear formatting

**Agent Output:**
```
[English Response]
I'm a software engineer with a rich international background. Born in Kazakhstan,
I grew up across Ukraine and Turkmenistan before attending an international high
school in Oxford. I studied Computer Science and Economics at Middlebury College
and I'm currently pursuing a joint MS in Engineering and MBA at Harvard.

My professional experience spans senior software engineering roles at major tech
companies. I've worked at Twitch, where I most recently built ML infrastructure,
Amazon, and EverQuote. I also had a brief stint as a sales engineer at InterSystems.
What excites me most is the intersection of technology and real-world impact...

[Russian Translation]
Я инженер-программист с богатым международным опытом. Родился в Казахстане...
[Full Russian translation]
```

#### Step 3: Text-to-Speech Synthesis
The system parses the bilingual response and generates two audio files:

- `response_english.mp3` (Voice: "alloy")
- `response_russian.mp3` (Voice: "nova")

### Output Files
```
demo_output/
├── response_english.mp3 (English audio response)
└── response_russian.mp3 (Russian audio response)
```

---

## 4. Insights & Observations

### Technical Insights

1. **Language Detection Accuracy**: Whisper's automatic language detection worked flawlessly for English inputs. For multilingual contexts, explicit language specification improves accuracy.

2. **Response Parsing Challenge**: The bilingual response format from the agent required heuristic parsing to separate English and Russian text. The current implementation uses Cyrillic character detection, which works well but could be improved with more structured output from the agent.

3. **Audio Quality**: OpenAI's TTS API produces natural-sounding speech. The "alloy" voice for English and "nova" for Russian were selected after testing for naturalness and clarity.

4. **Processing Time**:
   - STT (Whisper base model): ~2-3 seconds for 10-second audio
   - Agent processing: ~5-10 seconds (depends on CrewAI pipeline)
   - TTS: ~1-2 seconds per response
   - **Total**: ~10-15 seconds for end-to-end processing

### UX Insights

1. **Bilingual Audio Separation**: Generating separate audio files for each language is preferable to a single combined file. Users can choose which language to listen to based on preference.

2. **Voice Selection**: Different voices for different languages helps distinguish between them and makes the experience more natural.

3. **Error Handling**: Robust error handling is critical. Issues can occur at any stage (invalid audio format, API failures, transcription errors).

### Potential Improvements

1. **Streaming**: Implement real-time streaming for faster perceived latency
2. **Voice Selection**: Allow users to choose their preferred voice
3. **Structured Output**: Modify agent to output JSON with separate English/Russian fields for easier parsing
4. **Caching**: Cache Whisper model loading to avoid repeated initialization
5. **Audio Recording**: Add microphone input support for live voice interaction

---

## 5. Running the System

### Prerequisites
```bash
# Set API key
export ANTHROPIC_API_KEY=your-api-key

# Install dependencies
pip install -r requirements.txt
```

### Usage

**Option 1: Run demo with sample audio**
```bash
python demo_voice_agent.py
```

**Option 2: Process your own audio file**
```bash
python voice_agent.py your_audio.wav
```

**Option 3: Test individual components**
```bash
# Test STT only
python speech_to_text.py audio.wav

# Test TTS only
python text_to_speech.py "Hello world" output.mp3
```

---

## 6. Conclusion

This implementation successfully extends the text-based personal agent with voice capabilities, demonstrating how speech interfaces can be orchestrated with existing AI systems. The modular design allows each component (STT, TTS, Agent) to be tested and improved independently.

The most interesting challenge was bridging the bilingual nature of the original agent with audio output. The solution of generating separate audio files for each language proved to be both technically simpler and better for user experience.

**Key Takeaways:**
- Voice interfaces add significant value but also complexity
- Modular design is essential for debugging and testing
- Processing latency is a key consideration for production systems
- Bilingual support requires careful consideration at each pipeline stage

---

## Repository
[Add GitHub repository link]

## Video Demonstration
[Add unlisted YouTube link showing the system in action]
