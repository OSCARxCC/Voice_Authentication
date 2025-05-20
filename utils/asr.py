# import whisper

# def transcribe(audio_path):
#     model = whisper.load_model("base")
#     result = model.transcribe(audio_path, language="zh")
#     return result["text"]


# utils/asr.py
import whisper

model = whisper.load_model("base")

def transcribe(audio_path):
    result = model.transcribe(audio_path, language="zh")
    return result["text"]
