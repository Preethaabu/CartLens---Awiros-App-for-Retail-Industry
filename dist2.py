from ultralytics import YOLO
import cv2

# Load a model
model = YOLO('E:\\Projects\\object_detection\\data\\final_yolo\\best.pt')  # pretrained YOLOv8n model
image_path = 'E:\\Projects\\object_detection\\data\\uploads\\WhatsApp Image 2023-09-09 at 10.55.54.jpg'

# Run batched inference on a list of images
results = model(image_path)  # return a generator of Results objects

# Process results generator
for result in results:
    boxes = result.boxes  # Boxes object for bbox outputs
    labels = result.names  # Labels of detected objects
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs

    # YOLO coordinates [x_center, y_center, width, height]
    yolo_coordinates = boxes.xywh.numpy().tolist()

    image = cv2.imread(image_path)
    image_height, image_width, _ = image.shape

    for i, cord in enumerate(yolo_coordinates):
        label = labels[i]
        # Filter out non-vehicle objects (customize this condition based on your label naming)
        if label not in ["auto", "bike", "bus", "car", "truck"]:
            continue

        # Extract individual values
        x_center, y_center, width, height = cord
        fx = 1000.0

        # Known object size (you should provide the actual size of the object in meters)
        known_object_height = 2.0  # Example: the height of a car in meters
        known_object_width = 1.5   # Example: the width of a car in meters

        # Calculate the distance using the formula: D = (Known Object Height * Focal Length) / Object Height in Pixels
        distance_height = (known_object_height * fx) / height

        # Calculate the distance using the formula: D = (Known Object Width * Focal Length) / Object Width in Pixels
        distance_width = (known_object_width * fx) / width

        # Take the average of the two distance estimates for more robust results
        distance = (distance_height + distance_width) / 2.0

        # Print the label, coordinates, and estimated distance
        print(f"Label: {label}, Coordinates: {cord}, Estimated Distance: {distance:.2f} meters")
