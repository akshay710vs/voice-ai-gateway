import sounddevice as sd
import numpy as np
import wave

# Audio device index and sampling configuration constants
MIC_DEVICE = 15  # Microphone index (Realtek(R) Audio), Windows WASAPI
NATIVE_RATE = 48000  # Hardware native sampling rate (48 kHz)
TARGET_RATE = 16000  # Target sample rate for downstream speech processing models

def record_audio(filename="input.wav", duration=5):
    """Records mono audio from the configured microphone device and exports a WAV file."""
    print(f"Recording for {duration} seconds... speak now.")
    
    # Calculate total sample frames needed for the recording duration
    frames = int(duration * NATIVE_RATE)
    
    # Record mono 16-bit PCM audio synchronously from microphone
    audio = sd.rec(frames, samplerate=NATIVE_RATE, channels=1, dtype='int16', device=MIC_DEVICE, blocking=True)
    print("Recording finished. Frames captured:", audio.shape[0])

    # Write recorded PCM audio buffer into a standard WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)        # Single audio channel (mono)
        wf.setsampwidth(2)        # 2 bytes per sample (16-bit PCM)
        wf.setframerate(NATIVE_RATE) # Sampling frequency in Hz
        wf.writeframes(audio.tobytes()) # Commit audio byte data to file
    print(f"Saved to {filename} at {NATIVE_RATE} Hz")

if __name__ == "__main__":
    record_audio()