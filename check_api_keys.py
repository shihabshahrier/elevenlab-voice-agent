#!/usr/bin/env python3
import os
from dotenv import load_dotenv

"""
This script validates your API keys environment setup.
Run it before trying the voice assistant to ensure your API keys are properly configured.
"""

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Check for ElevenLabs API key
    elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY")
    if not elevenlabs_key:
        print("❌ ELEVENLABS_API_KEY not found in environment variables")
    elif elevenlabs_key == "your_eleven_labs_api_key_here":
        print("⚠️  ELEVENLABS_API_KEY is set to the default placeholder value")
    else:
        print(f"✅ ELEVENLABS_API_KEY found: {elevenlabs_key[:4]}...{elevenlabs_key[-4:] if len(elevenlabs_key) > 8 else ''}")
    
    # Check for Nebius API key
    nebius_key = os.environ.get("NEBIUS_API_KEY")
    if not nebius_key:
        print("❌ NEBIUS_API_KEY not found in environment variables")
    elif nebius_key == "your_nebius_api_key_here":
        print("⚠️  NEBIUS_API_KEY is set to the default placeholder value")
    else:
        print(f"✅ NEBIUS_API_KEY found: {nebius_key[:4]}...{nebius_key[-4:] if len(nebius_key) > 8 else ''}")
    
    # Print instructions if issues found
    if not elevenlabs_key or not nebius_key or elevenlabs_key == "your_eleven_labs_api_key_here" or nebius_key == "your_nebius_api_key_here":
        print("\nTo fix API key issues:")
        print("1. Make sure you have a .env file in the same directory as your Python scripts")
        print("2. The .env file should contain the following lines with your actual API keys:")
        print("   ELEVENLABS_API_KEY=your_actual_elevenlabs_key")
        print("   NEBIUS_API_KEY=your_actual_nebius_key")
        print("3. Restart your terminal or IDE after making changes to .env")
        print("\nFor ElevenLabs: Get your API key at https://elevenlabs.io/app/api-keys")
        print("For Nebius: Get your API key from your Nebius account settings")
    else:
        print("\nAPI keys setup looks good! You can now run the voice assistant.")

if __name__ == "__main__":
    main()