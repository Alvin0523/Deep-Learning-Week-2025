import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO(r"C:\Users\alvin\OneDrive - Nanyang Technological University\Files\03_Work\05_Hackathon\Deep Learning Week 2025\model\best.pt")

# Confidence threshold
CONFIDENCE_THRESHOLD = 0.7

def get_frame(cap):
    """Captures a frame from the webcam, performs YOLOv8 detection, and returns the processed frame as an RGB numpy array."""

    ret, frame = cap.read()
    if not ret:
        return None

    # Resize for faster processing (reduce detection time)
    frame_resized = cv2.resize(frame, (640, 480))  # Adjust resolution for speed

    # Perform YOLOv8 detection
    results = model(frame_resized)[0]

    for box in results.boxes:
        conf = box.conf[0].item()
        if conf < CONFIDENCE_THRESHOLD:
            continue  # Skip detections below confidence threshold

        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
        cls = int(box.cls[0])
        label = f"{model.names[cls]}: {conf:.2f}"

        # Draw bounding box (thicker)
        cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (0, 255, 0), thickness=3)

        # Draw label
        cv2.putText(frame_resized, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Convert frame to RGB (Streamlit requires RGB format)
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

    return frame_rgb

def is_object_detected(frame_resized):
    """Runs YOLOv8 detection on a frame and returns True if an object is detected, otherwise False."""

    results = model(frame_resized)[0]

    for box in results.boxes:
        conf = box.conf[0].item()
        if conf >= CONFIDENCE_THRESHOLD:
            return True  # Object detected

    return False  # No object detected
