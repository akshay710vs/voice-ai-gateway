from asyncio import streams
from openai import OpenAI
from record import record_audio
from transcribe import transcribe
from speak import speak

# Initialize OpenAI client pointed to local LiteLLM proxy gateway
gateway = OpenAI(base_url="http://localhost:4000", api_key="sk-local-test-1234")

def ask_llm_stream(text):
    """Sends user text prompt to the primary voice model hosted on the gateway."""
    # Request completion from LiteLLM proxy using the primary voice route
    stream = gateway.chat.completions.create(
        model="voice-primary",
        messages=[{"role":"user", "content":text}],
        stream=True,
    )
    # Extract and return the generated message text
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# def run_once():
#     """Executes a full voice loop: record microphone -> transcribe -> query LLM -> TTS -> playback."""
#     # Step 1: Capture 5 seconds of audio from the microphone
#     record_audio("input.wav", duration=5)
    
#     # Step 2: Convert recorded audio to text using Groq Whisper API
#     user_text = transcribe("input.wav")
#     print("You said:", user_text)

#     # Step 3: Query the LLM gateway with the transcribed text
#     reply_text = ask_llm(user_text)
#     print("AI replied:", reply_text)

#     # Step 4: Convert AI text response to synthesized speech audio file
#     speak(reply_text, "output.wav")

#     # Step 5: Read synthesized audio and play back through system speakers
#     import sounddevice as sd
#     import soundfile as sf
#     data, samplerate = sf.read("output.wav")
#     sd.play(data, samplerate)
#     sd.wait() # Wait until audio playback completes

# if __name__ == "__main__":
#     run_once()
