## Overview
This repository contains a bilingual personal agent representing Amir Amangeldi, with both text and voice interaction capabilities.

### Features
- **Text-based agent** (HW1-3): CrewAI multi-agent system with NANDA integration
- **Voice-enabled agent** (HW4): Speech-to-text and text-to-speech capabilities
- **Bilingual support**: Always responds in both English and Russian

## Feedback for NANDA
- The sandbox UI is unclear -- it took me some time to realize that messages sent by default are not routed through my agent. Only after digging through the codebase I realized I had to tag my agent with `@` within my Sandbox chat, to route the messages through my agent.
- The adapter codebase is poorly documented.

## Evidence
Chat in NANDA UI:
![alt text](./screenshot-0.png)

Corresponding logs:
![alt text](./screenshot-1.png)

Registration link in logs:
![alt text](./screenshot-2.png)

## Setting up

### Voice Agent (HW4)

1. Set your API key:
```bash
export ANTHROPIC_API_KEY=your-api-key
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the demo:
```bash
# Run with sample audio (auto-generated)
python demo_voice_agent.py

# Or process your own audio file
python voice_agent.py your_audio.wav
```

4. Test individual components:
```bash
# Test speech-to-text
python speech_to_text.py audio.wav

# Test text-to-speech
python text_to_speech.py "Hello world" output.mp3
```

### Text-based Agent (HW1-3) with NANDA

1. Set your Anthropic key and domain:
```bash
export ANTHROPIC_API_KEY=my-anthropic-key
export DOMAIN_NAME=my-domain
```

2. Check out [projnanda/adapter](https://github.com/projnanda/adapter).

3. Navigate to `adapter/nanda_adapter/examples` and install dependencies:
```bash
pip install -r requirements.txt
```

4. Drop `amir_agent.py` into the `examples` folder and run:
```bash
nohup python3 amir_agent.py > out.log 2>&1 &
```
