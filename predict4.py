from super_gradients.training import models
import os

dataset_params = {
    'classes': ['car', 'bike', 'auto', 'truck']
}

best_model = models.get('yolo_nas_l',
                        num_classes=len(dataset_params['classes']),
                        checkpoint_path="E:\\Projects\\object_detection\\data\\yolonas\\average_model.pth")

class_names = {
    0: "car",
    1: "bike",
    2: "auto",
    3: "truck"
    # Add more class names as needed
}

test_image = "E:\\Projects\\object_detection\\data\\uploads"

results = best_model.predict(test_image, conf=0.5)

# Iterate through all the results
for i, result in enumerate(results):
    print(f"Object {i + 1} predictions:")
    
    # Prepare detection annotations for the image
    det_bboxes = result.prediction.bboxes_xyxy
    det_scores = result.prediction.confidence
    det_labels = result.prediction.labels.astype(int)

    # Convert integer labels to class names
    det_class_names = [class_names[label] for label in det_labels]

    all_coords = []
    for box, label, score in zip(det_bboxes, det_labels, det_scores):
        x1, y1, x2, y2 = box.tolist()
        class_name = class_names[label]
        print(f"Class: {class_name}, Confidence: {score:.2f}")
        print(f"Bounding Box Coordinates: ({x1}, {y1}, {x2}, {y2})")

    print("\n")

# If you want to store the results in a variable for further processing, you can append them to a list or dictionary.
