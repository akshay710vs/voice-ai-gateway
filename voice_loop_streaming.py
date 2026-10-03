from record import record_audio
from transcribe import transcribe
from ask import ask_llm_stream
from stream_utils import sentence_chunks
from speak import speak
import sounddevice as sd
import soundfile as sf
import time

def play_file(filename):
    data, samplerate = sf.read(filename)
    sd.play(data, samplerate)
    sd.wait()

def run_once():
    record_audio("input.wav", duration=5)

    t0 = time.time()
    user_text = transcribe("input.wav")
    t1 = time.time()
    print("You said: {user_text} [STT: {t1-t0:.2f}s]")

    print("AI replying (streaming)...")
    token_stream = ask_llm_stream(user_text)

    first_sentence_time = None

    sentence_num=0

    for sentence in sentence_chunks(token_stream):
        sentence_num += 1
        now = time.time()
        if first_sentence_time is None:
            first_sentence_time = now
            print(f"[Time to first sentence: {now - t1:2f}s]")

        print(f"Sentence {sentence_num}: {sentence}")
        out_file = f"output_{sentence_num}.wav"
        speak(sentence, out_file)
        play_file(out_file)

    total = time.time() - t0
    print(f"[Total: {total:2f}s]")

if __name__ == "__main__":
    run_once()

