from groq import Groq

# Initialize Groq SDK client using GROQ_API_KEY environment variable
client = Groq()

def transcribe(filename="input.wav"):
    """Transcribes audio file to text using Groq's Whisper API endpoint."""
    # Open audio file in binary read mode
    with open(filename, "rb") as f:
        # Create audio transcription request with whisper-large-v3-turbo model
        result = client.audio.transcriptions.create(
            file=f,
            model="whisper-large-v3-turbo",
        )
    # Return transcribed text result
    return result.text

if __name__ == "__main__":
    text = transcribe()
    print("Transcript:", text)

