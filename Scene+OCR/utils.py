import os
import io
import base64
import threading

# First import pydub
from pydub import AudioSegment
from pydub.playback import play

import cv2
from dotenv import load_dotenv
from openai import OpenAI

if os.name == "nt":
    FFMPEG_PATH = r"C:\ffmpeg\ffmpeg.exe"
else:
    FFMPEG_PATH = "/opt/homebrew/bin/ffmpeg"
AudioSegment.converter = FFMPEG_PATH

load_dotenv()

# OS_BASE_PATH = r"/home/gsfc-pi/Desktop/final/audio/"
# OS_BASE_PATH = r"C:/Users/Viraj/Downloads/final-20241213T181551Z-001/final/audio/"
OS_BASE_PATH = os.path.join(os.path.dirname(__file__), "audio")

client = OpenAI()


def setup_camera():
    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    return cap


def play_audio(filename=None, bytes=None, bg=True):
    try:
        if filename:
            print(f"Loading {filename}")
            audio_path = os.path.join(OS_BASE_PATH, filename)

            # Create directory if it doesn't exist
            os.makedirs(OS_BASE_PATH, exist_ok=True)

            audio = AudioSegment.from_file(audio_path)
            print(f"Playing {filename}")

            if not bg:
                play(audio)
            else:
                t = threading.Thread(target=play, args=(audio,))
                t.start()

        if bytes:
            print(f"Loading audio from bytes ...")
            audio = AudioSegment.from_file(io.BytesIO(bytes), format="mp3")
            print(f"Playing audio ...")
            t = threading.Thread(target=play, args=(audio,))
            t.start()
    except Exception as e:
        print(f"Error playing audio: {str(e)}")


def performSTT(wav_audio):
    audio_bytes = io.BytesIO(wav_audio)
    audio_bytes.name = "myfile.wav"

    text = client.audio.transcriptions.create(
        model="whisper-1",
        language="en",
        response_format="text",
        file=audio_bytes
    )

    return text


def performVision(img_b64, prompt):
    messages = [{
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": prompt
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{img_b64}"
                }
            }
        ]
    }]

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        max_tokens=300,
        n=1

    )

    return response.choices[0].message.content


def performTTS(text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="shimmer",
        input=text,
        response_format="mp3",
    )

    return response


def sceneDetection(frame, text):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    _, buffer = cv2.imencode(".jpg", frame)
    img_b64 = base64.b64encode(buffer).decode('utf-8')

    model_response = performVision(img_b64, text)

    return model_response
