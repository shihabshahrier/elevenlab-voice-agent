import os
import time
import sounddevice as sd
import soundfile as sf
import numpy as np
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from openai import OpenAI

# Load environment variables
load_dotenv()

# API keys
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
NEBIUS_API_KEY = os.environ.get("NEBIUS_API_KEY")

# Initialize clients
eleven = ElevenLabs(api_key=ELEVENLABS_API_KEY)
ai = OpenAI(
    base_url="https://api.studio.nebius.com/v1/",
    api_key=NEBIUS_API_KEY
)

# Settings
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # Default ElevenLabs voice
TTS_MODEL = "eleven_multilingual_v2"
STT_MODEL = "speech-recognition-default"
AI_MODEL = "deepseek-ai/DeepSeek-V3-0324"
RECORD_SECONDS = 5
SAMPLE_RATE = 44100
CHANNELS = 1

# Conversation history
conversation_history = [
    {"role": "system", "content": "You are a helpful, friendly AI assistant. Keep your responses concise and natural."}
]

def record_audio():
    """Record audio from the microphone"""
    print(f"Recording for {RECORD_SECONDS} seconds...")
    print("Listening...")
    
    # Record audio
    recording = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype='float32'
    )
    sd.wait()
    
    print("Recording finished")
    
    # Save recording
    audio_file = "user_input.wav"
    sf.write(audio_file, recording, SAMPLE_RATE)
    
    return audio_file

def transcribe_audio(audio_file):
    """Convert speech to text"""
    print("Transcribing audio...")
    
    try:
        with open(audio_file, 'rb') as f:
            result = eleven.speech_to_text.convert(
                audio=f,
                model_id=STT_MODEL
            )
        
        transcript = result.text
        print(f"Transcript: {transcript}")
        return transcript
    
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return "Sorry, I couldn't understand that."

def get_ai_response(user_input):
    """Get AI response"""
    print("Getting AI response...")
    
    # Add user message to conversation history
    conversation_history.append({"role": "user", "content": user_input})
    
    try:
        response = ai.chat.completions.create(
            model=AI_MODEL,
            max_tokens=512,
            temperature=0.7,
            messages=conversation_history
        )
        
        ai_response = response.choices[0].message.content
        
        # Add AI response to conversation history
        conversation_history.append({"role": "assistant", "content": ai_response})
        
        print(f"AI response: {ai_response}")
        return ai_response
    
    except Exception as e:
        print(f"Error getting AI response: {e}")
        return "Sorry, I'm having trouble connecting to my brain right now."

def speak_response(text):
    """Convert text to speech"""
    print("Converting text to speech...")
    
    try:
        audio_stream = eleven.text_to_speech.convert_as_stream(
            voice_id=VOICE_ID,
            output_format="mp3_44100_128",
            text=text,
            model_id=TTS_MODEL
        )
        
        # Save the audio stream to a file
        audio_file = "assistant_response.mp3"
        with open(audio_file, "wb") as f:
            for chunk in audio_stream:
                if chunk:
                    f.write(chunk)
        
        # Play the audio
        play_audio(audio_file)
        
    except Exception as e:
        print(f"Error in text-to-speech: {e}")

def play_audio(audio_file):
    """Play audio file"""
    print(f"Playing audio: {audio_file}")
    
    try:
        # Load and play the audio file
        data, fs = sf.read(audio_file)
        sd.play(data, fs)
        sd.wait()
    except Exception as e:
        print(f"Error playing audio: {e}")

def main():
    """Run the voice assistant"""
    print("Starting Voice AI Assistant...")
    
    # Check if API keys are set
    if not ELEVENLABS_API_KEY or not NEBIUS_API_KEY:
        print("Error: API keys not found. Please check your .env file.")
        return
    
    # Initial greeting
    greeting = "Hello! How can I help you today?"
    print(f"Assistant: {greeting}")
    speak_response(greeting)
    
    try:
        while True:
            # Record and transcribe user input
            audio_file = record_audio()
            user_input = transcribe_audio(audio_file)
            print(f"You: {user_input}")
            
            # Check for exit command
            if any(word in user_input.lower() for word in ["goodbye", "bye", "exit", "quit"]):
                farewell = "Goodbye! Have a great day!"
                print(f"Assistant: {farewell}")
                speak_response(farewell)
                break
            
            # Process and respond
            ai_response = get_ai_response(user_input)
            print(f"Assistant: {ai_response}")
            speak_response(ai_response)
    
    except KeyboardInterrupt:
        print("\nAssistant stopped by user. Goodbye!")

if __name__ == "__main__":
    main()