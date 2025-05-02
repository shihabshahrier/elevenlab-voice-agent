#!/usr/bin/env python3
"""
Mock Voice Assistant - For testing without API keys
This version simulates the voice assistant functionality using keyboard input and 
console output instead of actual speech recognition and synthesis APIs.
"""

import time
import os

# Mock conversation history
conversation_history = [
    {"role": "system", "content": "You are a helpful, friendly AI assistant. Keep your responses concise and natural."}
]

def simulate_recording():
    """Simulate recording by asking for keyboard input"""
    print("\n[Recording] Type your message and press Enter:")
    user_input = input("> ")
    return user_input

def simulate_ai_response(user_input):
    """Simulate AI processing - just returns a simple response based on input"""
    # Add user message to conversation history
    conversation_history.append({"role": "user", "content": user_input})
    
    # Generate a simple response based on the input
    if "hello" in user_input.lower() or "hi" in user_input.lower():
        response = "Hello there! How can I help you today?"
    elif "weather" in user_input.lower():
        response = "I don't have real-time weather data, but I can discuss weather patterns in general."
    elif "name" in user_input.lower():
        response = "I'm your mock voice assistant. In the real version, I'd be powered by DeepSeek AI."
    elif "joke" in user_input.lower():
        response = "Why don't scientists trust atoms? Because they make up everything!"
    elif "time" in user_input.lower():
        response = f"The current time is {time.strftime('%H:%M:%S')}."
    elif "date" in user_input.lower():
        response = f"Today is {time.strftime('%A, %B %d, %Y')}."
    elif "help" in user_input.lower():
        response = "I can simulate a conversation. Try asking me about the weather, time, date, or ask for a joke."
    else:
        response = "That's interesting. In the full version, I'd give you a more contextual response using DeepSeek AI."
    
    # Add assistant response to conversation history
    conversation_history.append({"role": "assistant", "content": response})
    
    return response

def simulate_speech(text):
    """Simulate text-to-speech by displaying the text with a typing effect"""
    print("\n[Assistant speaking]:")
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.03)  # Adjust speed of typing effect
    print("\n")

def main():
    """Run the mock voice assistant"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*50)
    print("MOCK VOICE ASSISTANT")
    print("This is a simulation only - no API calls will be made")
    print("="*50)
    
    # Initial greeting
    greeting = "Hello! I'm your mock voice assistant. How can I help you today?"
    print("\n[Assistant]:")
    print(greeting)
    
    try:
        while True:
            # Get user input via keyboard
            user_input = simulate_recording()
            
            # Check for exit command
            if any(word in user_input.lower() for word in ["goodbye", "bye", "exit", "quit"]):
                farewell = "Goodbye! Thanks for testing the mock assistant."
                simulate_speech(farewell)
                break
            
            # Process user input and get response
            response = simulate_ai_response(user_input)
            
            # Display response with typing effect
            simulate_speech(response)
    
    except KeyboardInterrupt:
        print("\n\nAssistant stopped by user. Goodbye!")

if __name__ == "__main__":
    main()