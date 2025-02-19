from pdf2image import convert_from_path
import PyPDF2

def extract_images_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    return images

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()
