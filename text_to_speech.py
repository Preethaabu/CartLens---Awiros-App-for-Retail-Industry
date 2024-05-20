from gtts import gTTS
from io import BytesIO
import pygame
import tempfile
import time

# Function to convert text to speech
def speak(text, language='en'):
    mp3_fo = BytesIO()
    tts = gTTS(text, lang=language)
    tts.write_to_fp(mp3_fo)
    return mp3_fo

pygame.init()
pygame.mixer.init()

# Read text from a file
with open('input.txt', 'r') as file:
    text_to_speak = file.read()

# Generate speech and save it to a temporary file
sound = speak(text_to_speak, language='ta')

temp_mp3_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
temp_mp3_file.write(sound.getvalue())
temp_mp3_file.close()

# Load and play the temporary MP3 file
pygame.mixer.music.load(temp_mp3_file.name)
pygame.mixer.music.play()

# Wait for the audio to finish playing
while pygame.mixer.music.get_busy():
    pygame.time.delay(100)

# Clean up the temporary file
temp_mp3_file.unlink(temp_mp3_file.name)
