
from PIL import Image, ImageOps
import os
import cv2
import pytesseract
import numpy as np
import re
import tempfile
import openai
openai.api_key = "your-secret-api-key"



def set_image_dpi(file_path):
    im = Image.open(file_path)
    length_x, width_y = im.size
    factor = max(1, int(IMAGE_SIZE / length_x))
    size = (1800, 1800)
    im_resized = im.resize(size, Image.Resampling.LANCZOS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(600, 600))
    return temp_filename

def process_image(input_image_path):
    img1 = set_image_dpi(input_image_path)
    img = cv2.imread(img1)
    norm_img = np.zeros((img.shape[0], img.shape[1]))
    img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)

    def get_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # noise removal
    def remove_noise(image):
        return cv2.medianBlur(image, 1)

    # thresholding
    def thresholding(image, threshold_value=140):
        return cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)[1]

    # dilation
    def dilate(image):
        kernel = np.ones((1, 1), np.uint8)
        return cv2.dilate(image, kernel, iterations=1)

    # erosion
    def erode(image):
        kernel = np.ones((1, 1), np.uint8)
        return cv2.erode(image, kernel, iterations=1)

    # opening - erosion followed by dilation
    def opening(image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    # canny edge detection
    def canny(image):
        return cv2.Canny(image, 100, 200)

    # skew correction
    def deskew(image):
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    # template matching
    def match_template(image, template):
        return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

    gray = get_grayscale(img)
    thresh = thresholding(gray, threshold_value=140)  # Use a threshold value of 150
    opening = opening(gray)
    canny = canny(gray)
    dilate = dilate(thresh)
    erode = erode(thresh)
    rem = remove_noise(thresh)

    text = pytesseract.image_to_string(thresh, config='--psm 6 --oem 3 -l eng')
    text = text.upper()

    return text

def rotate_and_mirror(input_image_path, output_folder):
    # Check if the output folder exists, create it if not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the input image
    image = Image.open(input_image_path)

    # Define rotation angles
    rotation_angles = [0, 90, 180, 270]

    for angle in rotation_angles:
        # Rotate the image
        rotated_image = image.rotate(angle, expand=True)

        # Generate the output file name
        output_file_name = f"rotated_{angle}.jpg"
        output_file_path = os.path.join(output_folder, output_file_name)

        # Save the rotated image to the output folder
        rotated_image.save(output_file_path)

        print(f"Saved {output_file_path}")

        # Mirror the rotated image horizontally (left-right flip)
        mirrored_image = ImageOps.mirror(rotated_image)

        # Generate the output file name for the mirrored image
        mirrored_output_file_name = f"mirrored_rotated_{angle}.jpg"
        mirrored_output_file_path = os.path.join(output_folder, mirrored_output_file_name)

        # Save the mirrored image to the output folder
        mirrored_image.save(mirrored_output_file_path)

        print(f"Saved {mirrored_output_file_path}")

if __name__ == "__main__":
    IMAGE_SIZE = 1800
    input_image_path = r"E:\Projects\object_detection\data\reverse_ocr.jpg"  # Replace with your input image path
    rotation_output_folder = r"E:\Projects\object_detection\data\output"  # Replace with your desired output folder for rotation

    # Perform rotation
    rotate_and_mirror(input_image_path, rotation_output_folder)

    # Extract text from rotated images
    extracted_texts = []  # List to store extracted texts

    for filename in os.listdir(rotation_output_folder):
        if filename.endswith(".jpg"):
            image_path = os.path.join(rotation_output_folder, filename)
            extracted_text = process_image(image_path)
            extracted_texts.append(extracted_text)
    text1, text2, text3, text4, text5, text6, text7, text8 = extracted_texts
    # Print or manipulate the extracted text as needed
    for i, text in enumerate(extracted_texts):
        print(f"Extracted Text from Image {i + 1}:\n{text}\n")


def enhance_text(text):
    prompt = f"Improve the following text:\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Specify the model
        messages=[{"role": "system", "content": prompt}]
    )
    enhanced_text =response.choices[0].message.content.strip()
    return enhanced_text
def post_process_text(ocr_text):
    # Apply any necessary post-processing steps to the text
    processed_text = ocr_text.strip()  # Remove leading and trailing spaces
    processed_text = re.sub(r'\s+', ' ', processed_text)  # Replace multiple spaces with a single space
    processed_text = processed_text.replace('’', "'")  # Replace special characters

    return processed_text


def evaluate_text_quality(text):
    # You can define your own criteria to evaluate the quality of the text
    # For example, you can calculate the length of the text, presence of keywords, etc.
    text_length = len(text)
    # Add more evaluation criteria as needed
    return text_length

# Define a function to enhance and process text
def enhance_and_process_text(text):
    # Enhance the text using your existing code or any other method
    enhanced_text = enhance_text(text)  # Use your enhancement function here
    # Perform post-processing on the enhanced text
    processed_text = post_process_text(enhanced_text)  # Use your post-processing function here
    return processed_text

# Compare the extracted texts and choose the best one
extracted_texts = [
    text1,
    text2,
    text3,
    text4,
     text5,
    text6,
    text7,
    text8
]

best_text = None
best_quality = 0

for extracted_text in extracted_texts:
    text_quality = evaluate_text_quality(extracted_text)
    if text_quality > best_quality:
        best_quality = text_quality
        best_text = extracted_text

# Enhance and process the best text
if best_text is not None:
    best_processed_text = enhance_and_process_text(best_text)
    print("Best Extracted, Enhanced, and Processed Text:")
    print(best_processed_text)
else:
    print("No text found in any orientation.")



openai.api_key = "your-secret-api-key"


messages = [{"role": "system", "content": "You are an intelligent assistant."}]

message = """
You are assisting a blind person by conveying information about their medication. Please provide a clear and detailed explanation of the drug details extracted from a tablet strip so that the blind person can easily understand their medications donot mention any bulletins .

Tablet Strip Information:
- Tablets in the strip: DICLOFENAC SODIUM, CHLORZOXAZONE & PARACETAMOL
- Each Uncoated Tablet Contains:
  - Diclofenac Sodium IP: 50mg
  - Paracetamol IP: 325mg
  - Chlorzoxazone USP: 250mg
- Dose: The tablets should be taken as directed by the Physician.
- Not for Veterinary Use


Please provide a detailed and clear explanation of the above information, and then give some usage but dont mention the ingredients and then explain them as a normal person
 do not mention blind give the content in short way do not summarize anything i do not need any greetings do not mention any points and then do not give any extra content 
 only give only the mentioned content
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