from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from transcribe import transcribe
from ask import ask_llm_stream
from stream_utils import sentence_chunks
from speak import speak

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.post("/call")
async def call(audio: UploadFile = File(...)):
    input_path = "web_input.webm"
    with open(input_path, "wb") as f:
        f.write(await audio.read())


    user_text = transcribe(input_path)
    print ("You said:", user_text)

    full_reply = ""
    for sentence in sentence_chunks(ask_llm_stream(user_text)):
        full_reply += sentence + " "
    
    print("AI replied:", full_reply)

    speak(full_reply, "web_reply.wav")

    return FileResponse("web_reply.wav", media_type="audio/wav")