import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (r"C:\Program Files\Tesseract-OCR\tesseract.exe")

def run_ocr(image, language="eng"):
 text = pytesseract.image_to_string(
 Image.fromarray(image),lang=language)
 return text