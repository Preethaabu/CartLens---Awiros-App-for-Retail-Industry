from ultralytics import YOLO
import cv2

# Load a model
model = YOLO('E:\\Projects\\object_detection\\data\\final_yolo\\best.pt')  # pretrained YOLOv8n model

# Open the video file
video_path = 'E:\\visioaid\\yolo\\output_limit.mp4'
cap = cv2.VideoCapture(video_path)

# Get the focal length (fx) of your camera. You should provide the correct value.
fx = 1000.0  # Example focal length in pixels (adjust as needed)

# Known object size (you should provide the actual size of the object in meters)
known_object_height = 2.0  # Example: the height of a car in meters
known_object_width = 1.5   # Example: the width of a car in meters

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    # Check if the frame was read successfully
    if not ret:
        break

    # Run inference on the current frame
    results = model(frame)

    for result in results:
        boxes = result.boxes  # Boxes object for bbox outputs

        # YOLO coordinates [x_center, y_center, width, height]
        yolo_coordinates = boxes.xywh.numpy().tolist()

        for cord in yolo_coordinates:
            # Extract individual values
            x_center, y_center, width, height = cord

            # Calculate the distance using the formula: D = (Known Object Height * Focal Length) / Object Height in Pixels
            distance_height = (known_object_height * fx) / height

            # Calculate the distance using the formula: D = (Known Object Width * Focal Length) / Object Width in Pixels
            distance_width = (known_object_width * fx) / width

            # Take the average of the two distance estimates for more robust results
            distance = (distance_height + distance_width) / 2.0

            # Print the estimated distance
            print(f"Estimated Distance: {distance:.2f} meters")

# Release the video capture object
cap.release()
import openai


openai.api_key = "your-secret-api-key"


messages = [{"role": "system", "content": "You are an intelligent assistant."}]

message = f"""output coordinates and distance are mentioned below using these coordinates to act as an assistive system for a visually impaired person. 
Assist the visually impaired by explaining the output coordinates to the user without mentioning the coordinate point and bulletin point. 
Explain the output coordinate, like the name of the object detected like person, and then where the person is positioned, like to the left or to the right. 
and the distance of the object Then insist the visually impaired person to navigate in such a way based on the position of the object detected so that they move safely mention the visually impaired people to navigate in such a 
way that they move away from the object dtected
{yolo_coordinates}{distance} """

max_tokens=70


# Add temperature to the API call with a low value (0.2)
temperature = 0.1  # Low temperature for more deterministic responses

if message:
    messages.append({"role": "user", "content": message})

    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, temperature=temperature
    )

    reply = chat.choices[0].message.content

    # Save the ChatGPT response to a text file
    with open("chatgpt_response.txt", "w") as file:
        file.write(reply)

    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})

    from gtts import gTTS
    from io import BytesIO
    import pygame
    import tempfile
    import time


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