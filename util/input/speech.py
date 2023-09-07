#!/usr/bin/python3
import os
from elevenlabs import generate, set_api_key, voices
from pydub.utils import mediainfo
import uuid  # Add this import

def generate_speech(text, save_path=None):
    # Set the API key from the environment variable
    api_key = os.environ.get('ELEVENLABS_API_KEY')
    if not api_key:
        raise ValueError("Please set the 'ELEVENLABS_API_KEY' environment variable.")

    set_api_key(api_key)

    found_voices = voices()
    index = -1
    for i, voice in enumerate(found_voices):
        if voice.name == 'Adam':
            index = i
            break

    if index == -1:
        raise ValueError("Voice not found.")

    # Generate the audio
    audio = generate(text=text, voice='Adam', model="eleven_monolingual_v1")
    
    # If save_path is provided, save the audio to the local file
    if save_path:
        unique_string = str(uuid.uuid4())[:8]  # Create a random string from a UUID
        save_path = os.path.join(save_path, unique_string + ".wav")  # Modify the save_path

        with open(save_path, 'wb') as file:
            file.write(audio)

        audio_info = mediainfo(save_path)
        audio_length = float(audio_info['duration'])  # This will give the duration in seconds

        return audio_length, save_path

if __name__ == '__main__':
    try:
        print("Generating speech...")
        result = generate_speech("Hello world!", save_path="test2.wav")
        print(result)
    except ValueError as e:
        print(e)
