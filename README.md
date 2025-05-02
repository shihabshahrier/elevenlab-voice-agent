# Voice AI Assistant

A simple voice assistant that uses ElevenLabs for speech-to-text and text-to-speech capabilities, and Nebius DeepSeek for AI responses.

## Features

- Records audio from your microphone
- Transcribes speech to text using ElevenLabs
- Processes requests using Nebius DeepSeek AI model
- Converts AI responses to speech using ElevenLabs
- Maintains conversation history for context

## Setup

### Prerequisites

- Python 3.8+
- ElevenLabs API key
- Nebius API key

### Installation

1. Clone this repository or download the code
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project directory with your API keys:

```
ELEVENLABS_API_KEY=your_eleven_labs_api_key_here
NEBIUS_API_KEY=your_nebius_api_key_here
```

### Running the Assistant

Run the assistant with:

```bash
python voice_assistant.py
```

The assistant will:
1. Greet you with a welcome message
2. Listen for your input (default 5 seconds)
3. Process your request and respond
4. Continue the conversation until you say "goodbye" or press Ctrl+C

## Customization

You can customize several aspects of the assistant by modifying the code:

- Change the voice by using a different `voice_id`
- Adjust the AI temperature for more creative or precise responses
- Modify the recording duration
- Add more exit phrases
- Customize the system prompt to change the assistant's personality

## Troubleshooting

- If you encounter issues with PyAudio installation, you may need to install platform-specific dependencies first.
- For Linux: `sudo apt-get install portaudio19-dev`
- For macOS: `brew install portaudio`

## Extensions

This basic implementation can be extended in many ways:
- Add wake word detection
- Implement hotkey activation
- Add GUI interface
- Support for different languages
- Integration with smart home devices