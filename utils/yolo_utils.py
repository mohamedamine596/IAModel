import torch
from ultralytics import YOLO
import numpy as np
from PIL import Image, ImageDraw

def load_yolo_model(model_path="yolov8s.pt"):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading YOLO model on {device}")
    model = YOLO(model_path)
    model.to(device)
    return model

def detect_objects(image, model):
    image_np = np.array(image)
    results = model.predict(image_np)
    
    detections = []
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())
            # Get class name if available; otherwise, fallback to numeric class
            class_name = result.names.get(cls, str(cls)) if hasattr(result, "names") else str(cls)
            detections.append({
                "bbox": [x1, y1, x2, y2],
                "confidence": conf,
                "class": class_name
            })
    return detections

def draw_detections(image, detections):
    draw_image = image.copy()
    draw = ImageDraw.Draw(draw_image)

    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        label = f"{det['class']} {det['confidence']:.2f}"
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
        draw.text((x1, y1 - 10), label, fill="red")
    
    return draw_image