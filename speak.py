
from deepgram import DeepgramClient

def speak(text, filename="output.wav"):
    """Synthesizes text into speech using Deepgram TTS API and saves output to a WAV file."""
    # Initialize the Deepgram client using DEEPGRAM_API_KEY environment variable
    client = DeepgramClient()
    
    # Request text-to-speech audio stream generation with Aura voice model
    audio_stream = client.speak.v1.audio.generate(
        text=text,
        model="aura-2-asteria-en", # Voice model for English synthesis
        encoding="linear16",        # Uncompressed 16-bit linear PCM audio
        container="wav",           # WAV container format
    )

    # Stream and write raw audio chunks to the output WAV file
    with open(filename, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)
    print(f"Saved speech to {filename}")

if __name__ == "__main__":
    speak("Hello, how are you doing today?")