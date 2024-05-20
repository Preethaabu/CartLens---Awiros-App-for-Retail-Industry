from ultralytics import YOLO
import openai
from gtts import gTTS
from io import BytesIO
import pygame
import tempfile
import time

model= YOLO('E:\\Projects\\object_detection\\data\\final_yolo\\best.pt')
model.predict(source='E:\\Projects\\object_detection\\data\\uploads', save=True)

# Run inference on the source
all_coords = []  # Initialize an empty list to store coordinates

results = model(source='E:\\Projects\\object_detection\\data\\uploads')
for result in results:
    boxes = result.boxes.xyxy
    coord = boxes.tolist()

    # Convert the tensor to a Python list
    all_coords.append(coord)  # Append coord to the list

# Now, 'all_coords' contains all the coordinates as Python lists from each iteration
print(all_coords)

# Set your OpenAI API key

openai.api_key = "your-secret-api-key"


messages = [{"role": "system", "content": "You are an intelligent assistant."}]

message = """
explain this output that i provided in all coords variable to alert the blind person
tell them where the vehicle is with the help of coordinates i provided
do not mention the  coordinates value but just the position , tell them the location like it is located
like left or right in two or three lines and the name of vehcile, guide them in friendly way to navigate.be polite and dont mention blind people 
Don't put bulletins:  320x640 1 auto, 1 bike, 4 cars, 1481.7ms
Speed: 3.5ms preprocess, 1481.7ms inference, 1.9ms postprocess per image at shape (1, 3, 320, 640)
[[[36.718605041503906, 132.61044311523438, 349.3322448730469, 340.6586608886719], [646.794921875, 150.05615234375, 894.1738891601562, 343.1234130859375], [458.9913635253906, 178.7517852783203, 533.2379760742188, 319.06744384765625], [552.6607666015625, 119.29246520996094, 657.2623291015625, 262.0163269042969], [316.53515625, 123.6947250366211, 468.6447448730469, 262.4700622558594], [840.9850463867188, 136.7136688232422, 900.0, 276.72198486328125]]]
"""

if message:
    messages.append({"role": "user", "content": message})

    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )

    reply = chat.choices[0].message.content

    # Save the ChatGPT response to a text file
    with open("chatgpt_response.txt", "w") as file:
        file.write(reply)

    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})

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
sound = speak(text_to_speak)

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





