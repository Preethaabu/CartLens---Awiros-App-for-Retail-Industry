from ultralytics import YOLO
import openai
from gtts import gTTS
from io import BytesIO
import pygame
import tempfile
import time

# Load the first YOLO model
model1 = YOLO('E:\\Projects\\object_detection\\data\\first_yolo\\best (1).pt')

# Load the second YOLO model
model2 = YOLO('E:\\Projects\\object_detection\\data\\first_yolo\\best (1).pt')  # Replace 'path_to_second_model.pt' with the path to your second model

# Make predictions using both models on the same source image
results1 = model1.predict(source='E:\\Projects\\object_detection\\data\\uploads')
results2 = model2.predict(source='E:\\Projects\\object_detection\\data\\uploads')

# Combine the predictions from both models
results = results1 + results2

# Save the combined predictions
#combined_results.save()

# You can also access the combined prediction data like bounding boxes, labels, and scores as needed
#print(combined_results)

all_coords=[]
for result in results:
    boxes = result.boxes.xyxy
    coord = boxes.tolist()

    # Convert the tensor to a Python list
    all_coords.append(coord)  # Append coord to the list

# Now, 'all_coords' contains all the coordinates as Python lists from each iteration
print(all_coords)

#chatgpt



# Set your OpenAI API key

openai.api_key = "your-secret-api-key"


messages = [{"role": "system", "content": "You are an intelligent assistant."}]

message = """
explain this yolo object detection output to alert the blind person
tell them where the vehicle is with the help of coordinates
do not tell them coordinates, tell them the location like it is located
like left or right in two or three lines, guide them.
Don't put bulletins: {all_coords}
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
with open('chatgpt_response.txt', 'r') as file:
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






