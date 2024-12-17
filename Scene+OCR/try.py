
import subprocess
import pyaudio

# Path to the audio file
audio_file = "C:\\Users\\Viraj\\Downloads\\final-20241213T181551Z-001\\Scene+OCR\\audio\\beep.mp3"

# FFmpeg command to decode the audio into raw PCM format
ffmpeg_command = [
    "ffmpeg",
    "-i", audio_file,          # Input file
    "-f", "s16le",             # Output format: PCM 16-bit little-endian
    "-ac", "2",                # Number of audio channels
    "-ar", "44100",            # Sample rate (Hz)
    "pipe:1"                   # Output to stdout (pipe)
]

# Start the FFmpeg subprocess
ffmpeg_process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

# Initialize PyAudio
audio_player = pyaudio.PyAudio()

# Open a PyAudio stream
stream = audio_player.open(format=pyaudio.paInt16,  # 16-bit audio format
                           channels=2,             # Stereo
                           rate=44100,             # Sample rate
                           output=True)            # Output stream

# Read and play the audio data from FFmpeg
try:
    while True:
        audio_data = ffmpeg_process.stdout.read(4096)  # Read raw audio data
        if not audio_data:
            break
        stream.write(audio_data)  # Play audio
finally:
    # Cleanup
    stream.stop_stream()
    stream.close()
    audio_player.terminate()
    ffmpeg_process.terminate()
