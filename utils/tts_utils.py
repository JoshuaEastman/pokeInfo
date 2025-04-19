import io
import openai
from config.config import config

openai.api_key = config.openai_api_key

def generate_tts_audio(text: str, voice: str = "echo") -> io.BytesIO:
    response = openai.audio.speech.create(
        model="tts-1-hd",
        voice=voice,
        input=text
    )
    return io.BytesIO(response.content)