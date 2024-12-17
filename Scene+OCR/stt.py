# Speech to text
import io
import speech_recognition as sr

from utils import play_audio, performSTT


class MicrophoneStream:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust microphone energy threshold
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

def speech_to_text():
    rec = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise ...")
            rec.adjust_for_ambient_noise(source, duration=1)
            
            print("Starting To Record ... ")
            play_audio("beep.mp3", bg=False)
            
            print("Listening...")
            audio = rec.listen(source, timeout=5, phrase_time_limit=5)
            wav_audio = audio.get_wav_data()
            
            text = performSTT(wav_audio)
            return text
            
    except sr.WaitTimeoutError:
        print("No speech detected within timeout period")
        return "No speech detected"
    except Exception as e:
        print(f"Error during speech recognition: {str(e)}")
        return "Error during speech recognition"