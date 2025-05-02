from elevenlabs import ElevenLabs
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API keys
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)
client.speech_to_text.convert(
    model_id="scribe_v1",
    file="user_input.wav",
)