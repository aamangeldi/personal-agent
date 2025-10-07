# HW4: Speech Capabilities Implementation Plan

## Overview
Extend the existing Amir agent (CrewAI-based) with speech-to-text (STT) and text-to-speech (TTS) capabilities to enable voice-based interactions.

## Architecture Decision

### Libraries Selected
- **Speech-to-Text**: OpenAI Whisper (openai-whisper)
  - Robust, multilingual support (important for Russian translation feature)
  - Well-documented and actively maintained
  - Multiple model sizes for flexibility

- **Text-to-Speech**: OpenAI TTS API
  - High-quality neural voices
  - Simple API integration
  - Supports multiple languages including Russian
  - Alternative fallback: pyttsx3 for offline use

### Integration Points
1. Input pipeline: Audio file → Whisper → Text → Agent
2. Output pipeline: Agent → Text → TTS → Audio file
3. File-based interaction for simplicity

---

## Stage 1: Setup and Dependencies
**Goal**: Install required libraries and verify they work independently
**Success Criteria**:
- All dependencies installed without conflicts
- Whisper can transcribe a test audio file
- TTS can generate a test audio file
**Tests**:
- Run simple Whisper transcription on sample audio
- Generate TTS audio from sample text
- Verify audio quality and language support
**Status**: ✅ Complete

---

## Stage 2: Speech-to-Text Module
**Goal**: Create a reusable STT module that converts audio to text
**Success Criteria**:
- Module accepts audio file paths and returns transcribed text
- Supports both English and Russian transcription
- Handles errors gracefully
**Tests**:
- Test with English and Russian audio samples
- Test with invalid audio files
**Status**: ✅ Complete - Created `speech_to_text.py`

---

## Stage 3: Text-to-Speech Module
**Goal**: Create a reusable TTS module that converts text to audio
**Success Criteria**:
- Module accepts text and returns audio file path
- Supports both English and Russian synthesis
- Audio quality is clear and understandable
**Tests**:
- Test with English text
- Test with Russian text
**Status**: ✅ Complete - Created `text_to_speech.py`

---

## Stage 4: Voice-Enabled Agent Integration
**Goal**: Extend amir_agent.py to support voice input/output
**Success Criteria**:
- Agent can accept audio file as input
- Agent processes audio → text → agent logic → text → audio
- Output audio contains both English and Russian responses
**Tests**:
- Test voice question → voice response flow
- Verify bilingual output in audio
**Status**: ✅ Complete - Created `voice_agent.py`

---

## Stage 5: Demo and Documentation
**Goal**: Create demo script and documentation
**Success Criteria**:
- Demo script runs end-to-end voice interaction
- Video recording shows working system
- Write-up explains implementation and insights
**Status**: ✅ Complete - Created `demo_voice_agent.py` and `WRITEUP.md`

---

## Next Steps

1. **Test the system** - Run `python demo_voice_agent.py` to verify end-to-end functionality
2. **Record video demo** - Capture the system working and upload to YouTube
3. **Update WRITEUP.md** - Fill in actual example output and add video link
4. **Final review** - Test all components individually and together
