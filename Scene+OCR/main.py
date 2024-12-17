import subprocess
import time
from pynput import keyboard
from utils import setup_camera, sceneDetection
from stt import speech_to_text
from tts import text_to_speech
import os

# Directory to store audio files
AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# FFmpeg playback function
def play_audio_ffmpeg(file_path):
    """Play audio using FFmpeg."""
    try:
        command = ["ffplay", "-nodisp", "-autoexit", file_path]
        subprocess.run(command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except Exception as e:
        print(f"Error playing audio {file_path}: {str(e)}")

# Ensure audio files exist
def ensure_audio_files_exist():
    """Check if required audio files exist."""
    required_files = {
        "greeting_openai.mp3": "Welcome message",
        "sd_openai.mp3": "Scene detection prompt",
        "ocr_openai.mp3": "OCR prompt",
        "processing_openai.mp3": "Processing message"
    }

    missing_files = []
    for file, description in required_files.items():
        if not os.path.exists(os.path.join(AUDIO_DIR, file)):
            missing_files.append(f"- {file} ({description})")

    if missing_files:
        print("\nMissing audio files:")
        print("\n".join(missing_files))
        print(f"\nPlease ensure these files are present in the {AUDIO_DIR} directory")
        return False
    return True

# Global execution counter
TIMES_EXEC = 0

# Key event handlers
def on_press(key):
    global TIMES_EXEC
    try:
        if key.char == 'q':
            print("\nExiting program...")
            return False  # Stops listener

        if key.char == 's':
            print("\nScene Detection triggered")
            time.sleep(0.5)  # Debounce delay
            play_audio_ffmpeg(os.path.join(AUDIO_DIR, "sd_openai.mp3"))
            cap = setup_camera()

            # Warm up camera
            for _ in range(10):
                ret, frame = cap.read()

            _, frame = cap.read()
            text = speech_to_text()
            print(text)

            play_audio_ffmpeg(os.path.join(AUDIO_DIR, "processing_openai.mp3"))
            response = sceneDetection(frame, text)
            print(f"\nResponse - {response}\n")
            print(type(response))

            text_to_speech(response)
            cap.release()

        if key.char == 'o':
            print("\nOCR triggered")
            time.sleep(0.5)  # Debounce delay
            play_audio_ffmpeg(os.path.join(AUDIO_DIR, "ocr_openai.mp3"))
            cap = setup_camera()

            # Warm up camera
            for _ in range(10):
                ret, frame = cap.read()

            time.sleep(2)
            _, frame = cap.read()
            text = "Please perform OCR on this image. Only return exactly what is written in the image and nothing else."
            response = sceneDetection(frame, text)
            print(f"\nResponse - {response}\n")
            print(type(response))

            text_to_speech(response)
            cap.release()

    except AttributeError:
        pass

def main():
    global TIMES_EXEC

    if not ensure_audio_files_exist():
        print("\nWarning: Some audio files are missing. The program will continue but audio features may not work.")

    if TIMES_EXEC == 0:
        play_audio_ffmpeg(os.path.join(AUDIO_DIR, "greeting_openai.mp3"))
        TIMES_EXEC += 1

    print("Press 's' for Scene Detection")
    print("Press 'o' for OCR")
    print("Press 'q' to quit")

    # Start listening to key presses
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
