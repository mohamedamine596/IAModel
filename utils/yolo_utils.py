from ultralytics import YOLO
import numpy as np
from PIL import Image, ImageDraw

def load_yolo_model():
    model = YOLO('yolov5su.pt')
    return model

def detect_objects(image, model):
    # Convert PIL Image to numpy array
    image_np = np.array(image)
    results = model.predict(image_np)
    
    # Process the results
    detections = []
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = box.conf[0].item()
            cls = box.cls[0].item()
            class_name = result.names[int(cls)]
            
            detections.append({
                'bbox': [x1, y1, x2, y2],
                'confidence': conf,
                'class': class_name
            })
    
    return detections

def draw_detections(image, detections):
    # Create a copy of the image to draw on
    draw_image = image.copy()
    draw = ImageDraw.Draw(draw_image)
    
    # Draw each detection
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        label = f"{det['class']} {det['confidence']:.2f}"
        
        # Draw rectangle
        draw.rectangle([x1, y1, x2, y2], outline='red', width=2)
        
        # Draw label
        draw.text((x1, y1-10), label, fill='red')
    
    return draw_image