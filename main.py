import os
import time
import pyaudio
import wave
import logging
from elevenlabs import ElevenLabs
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VoiceAssistant:
    def __init__(self):
        # Initialize API keys - replace these with your actual keys or use environment variables
        self.elevenlabs_api_key = os.environ.get("ELEVENLABS_API_KEY", "YOUR_ELEVENLABS_API_KEY")
        self.nebius_api_key = os.environ.get("NEBIUS_API_KEY", "YOUR_NEBIUS_API_KEY")
        
        # Initialize ElevenLabs client
        self.eleven_client = ElevenLabs(api_key=self.elevenlabs_api_key)
        
        # Initialize Nebius/DeepSeek client
        self.ai_client = OpenAI(
            base_url="https://api.studio.nebius.com/v1/",
            api_key=self.nebius_api_key
        )
        
        # Voice settings
        self.voice_id = "JBFqnCBsd6RMkjVDRZzb"  # Default ElevenLabs voice
        self.tts_model = "eleven_multilingual_v2"
        self.stt_model = "speech-recognition-default"
        
        # AI model settings
        self.ai_model = "deepseek-ai/DeepSeek-V3-0324"
        self.ai_temperature = 0.7
        self.ai_max_tokens = 512
        
        # Conversation history
        self.conversation_history = []
        
        # Recording settings
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk = 1024
        self.record_seconds = 5  # Default recording duration
        self.audio_file = "user_input.wav"
        
        logger.info("Voice Assistant initialized")

    def record_audio(self, duration=None):
        """Record audio from the microphone"""
        if duration:
            self.record_seconds = duration
            
        logger.info(f"Recording for {self.record_seconds} seconds...")
        
        audio = pyaudio.PyAudio()
        
        # Start recording
        stream = audio.open(format=self.format, channels=self.channels,
                            rate=self.rate, input=True,
                            frames_per_buffer=self.chunk)
        
        print("Listening...")
        frames = []
        
        for i in range(0, int(self.rate / self.chunk * self.record_seconds)):
            data = stream.read(self.chunk)
            frames.append(data)
        
        print("Recording finished")
        
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # Save the recorded audio as a WAV file
        with wave.open(self.audio_file, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))
        
        logger.info(f"Audio saved to {self.audio_file}")
        return self.audio_file

    def transcribe_audio(self, audio_file):
        """Convert speech to text using ElevenLabs"""
        logger.info("Transcribing audio...")
        
        try:
            with open(audio_file, 'rb') as f:
                result = self.eleven_client.speech_to_text.convert(
                    audio=f,
                    model_id=self.stt_model
                )
            
            transcript = result.text
            logger.info(f"Transcription: {transcript}")
            return transcript
        
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return "Sorry, I couldn't understand that."

    def get_ai_response(self, user_input):
        """Get AI response from Nebius DeepSeek"""
        logger.info("Getting AI response...")
        
        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        try:
            response = self.ai_client.chat.completions.create(
                model=self.ai_model,
                max_tokens=self.ai_max_tokens,
                temperature=self.ai_temperature,
                messages=self.conversation_history
            )
            
            ai_response = response.choices[0].message.content
            
            # Add AI response to conversation history
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            logger.info(f"AI response: {ai_response}")
            return ai_response
        
        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            return "Sorry, I'm having trouble connecting to my brain right now."

    def speak_response(self, text):
        """Convert text to speech using ElevenLabs"""
        logger.info("Converting text to speech...")
        
        try:
            audio_stream = self.eleven_client.text_to_speech.convert_as_stream(
                voice_id=self.voice_id,
                output_format="mp3_44100_128",
                text=text,
                model_id=self.tts_model
            )
            
            # Save the audio stream to a file
            audio_file = "assistant_response.mp3"
            with open(audio_file, "wb") as f:
                for chunk in audio_stream:
                    if chunk:
                        f.write(chunk)
            
            logger.info(f"Response saved to {audio_file}")
            
            # Play the audio (platform dependent)
            self.play_audio(audio_file)
            
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
            print("Failed to generate speech. Check logs for details.")

    def play_audio(self, audio_file):
        """Play audio file (basic implementation, might need OS-specific code)"""
        # This is a simple implementation that will work on many systems
        # For better cross-platform support, consider pygame or another library
        import os
        
        logger.info(f"Playing audio: {audio_file}")
        
        if os.name == 'posix':  # Linux or Mac
            os.system(f"afplay {audio_file}" if os.uname().sysname == 'Darwin' else f"aplay {audio_file}")
        elif os.name == 'nt':  # Windows
            os.system(f"start {audio_file}")
        else:
            logger.warning("Unsupported OS for audio playback")
            
    def run_conversation(self, initial_greeting="Hello! How can I help you today?"):
        """Run a continuous conversation loop"""
        # Initial greeting
        print(initial_greeting)
        self.speak_response(initial_greeting)
        
        try:
            while True:
                # Record user audio
                audio_file = self.record_audio()
                
                # Convert speech to text
                user_input = self.transcribe_audio(audio_file)
                print(f"You: {user_input}")
                
                # Exit if user says goodbye
                if any(word in user_input.lower() for word in ["goodbye", "bye", "exit", "quit"]):
                    farewell = "Goodbye! Have a great day!"
                    print(f"Assistant: {farewell}")
                    self.speak_response(farewell)
                    break
                
                # Get AI response
                ai_response = self.get_ai_response(user_input)
                print(f"Assistant: {ai_response}")
                
                # Convert text to speech and play
                self.speak_response(ai_response)
        
        except KeyboardInterrupt:
            print("\nThank you for using the Voice Assistant. Goodbye!")

if __name__ == "__main__":
    assistant = VoiceAssistant()
    
    # Add system message to set the assistant's behavior
    assistant.conversation_history.append({
        "role": "system", 
        "content": "You are a helpful, friendly AI assistant. Keep your responses concise and natural."
    })
    
    # Start the conversation
    assistant.run_conversation()