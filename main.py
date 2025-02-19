import os
from utils.pdf_utils import extract_images_from_pdf, extract_text_from_pdf
from utils.yolo_utils import load_yolo_model, detect_objects, draw_detections
from utils.ollama_utils import generate_visual_description

def main(pdf_path, api_url):
    # Extract images from PDF
    print("Extracting images from PDF...")
    images = extract_images_from_pdf(pdf_path)

    # Extract text from PDF
    print("Extracting text from PDF...")
    pdf_text = extract_text_from_pdf(pdf_path)
    
    # Load YOLO model
    print("Loading YOLO model...")
    model = load_yolo_model()
    
    # Create outputs directory if it doesn't exist
    os.makedirs('outputs', exist_ok=True)
    
    # Process each image
    for i, image in enumerate(images, 1):
        print(f"\nProcessing image {i}/{len(images)}")
        
        try:
            # Detect objects in the image
            print("Detecting objects...")
            detections = detect_objects(image, model)
            
            # Draw detections on the image
            annotated_image = draw_detections(image, detections)
            
            # Generate description using multimodal integration (image and text)
            print("Generating description...")
            description = generate_visual_description(image, detections, api_url, pdf_text)
            
            # Save results
            print("Saving results...")
            annotated_image.save(f'outputs/image_{i}_detected.png')
            
            # Save description to file
            with open(f'outputs/image_{i}_description.txt', 'w') as f:
                f.write("Objects detected:\n")
                for det in detections:
                    f.write(f"- {det['class']} (confidence: {det['confidence']:.2f})\n")
                f.write(f"\nOllama description:\n{description}")
            
            print(f"Image {i} processed successfully")
            print(f"Description: {description}")
            
        except Exception as e:
            print(f"Error processing image {i}: {str(e)}")
            continue

if __name__ == "__main__":
    pdf_path = "inputs/boys.pdf"
    api_url = "http://localhost:11434/api/generate"
    
    try:
        main(pdf_path, api_url)
        print("\nProcessing completed successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")