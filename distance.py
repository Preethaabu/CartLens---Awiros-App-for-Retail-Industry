from ultralytics import YOLO
import cv2
import imageio

# Load the YOLO model
model = YOLO('best.pt', task='detect')

media_path = 'rightvid.mp4'
video_file_path = 'leftpredicted.mp4'
# Perform object detection on a video


confidence_threshold = 0.1
iou= 0.2
# Define a dictionary to map class IDs to labels
class_labels = {3: "Person"}

# Open the video file
cap = cv2.VideoCapture(media_path)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
# output_writer = imageio.get_writer(video_file_path, fps=30, codec='vp9')
# Define the output text file path
output_file_path = 'output_boxes.txt'

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_width = frame.shape[1]
    frame_height = frame.shape[0]

    # Perform object detection on the frame
    results = model(frame, conf=confidence_threshold,iou=iou)

    for result in results:
        boxes = result.boxes.xywh.cpu().numpy()
        scores = result.boxes.conf.cpu().numpy()
        labels = result.boxes.cls.cpu().numpy()
        for i in range(len(labels)):
            if((labels[i]) == 3):
                x, y, w, h = boxes.tolist()[i]
                threshold = frame_width // 2  # Assuming frame_width is the width of your image
                bbox_center_x = x + (w / 2)

                # Determine the position
                if bbox_center_x < threshold:
                    position = "left"
                else:
                    position = "right"

                print(f"The person is walking to the {position}.")

    # output_writer.append_data(frame)


    # Release video capture and writer
cap.release()
# output_writer.close()

cv2.destroyAllWindows()