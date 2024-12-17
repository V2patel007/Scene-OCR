import io
from utils import performTTS, play_audio

def text_to_speech(text, filename=None):
    try:
        response = performTTS(text)
        bytes_audio = response.content

        play_audio(bytes=bytes_audio)

        if filename:
            with open(filename, 'wb') as f:
                f.write(bytes_audio)
    except Exception as e:
        print(f"Error in text to speech: {str(e)}")

if __name__ == "__main__":
    greeting_text = "Hey There! [pause] I'm Akshi! [pause] Your Personal Assistant!"
    processing_text = "Processing [pause] Please wait."
    sd_text = """
    Performing scene detection! ... [pause] [pause]
    Please start speaking after two beeps.
    """
    ocr_text = """
    Performing Optical Character Recognition! ... 
    Please align the document or the scene containing text in front of you. [pause] [pause]
    I will take a photo in 2 seconds.
    """

    text_to_speech(sd_text, filename="sd_openai.mp3")