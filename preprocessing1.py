import cv2
import numpy as np
import os
from pdf2image import convert_from_path

def pdf_to_images(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300)
    images = []
    for page in pages:
        # Convert PIL image to numpy array (BGR for OpenCV)
        image_np = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)
        images.append(image_np)
    return images

def preprocess_image(image_path, save_output=False, output_folder="Output"):
    # Load image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Noise removal
    denoised = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    if save_output:
        os.makedirs(output_folder, exist_ok=True)
        base_name = os.path.basename(image_path)
        save_name = f"preprocessed_{base_name}"
        save_path = os.path.join(output_folder, save_name)
        cv2.imwrite(save_path, thresh)
        print(f"Preprocessed image saved to: {save_path}")

    return thresh

def preprocess_numpy_image(image, save_output=False, output_folder="Output", save_name="preprocessed_page.png"):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    if save_output:
        os.makedirs(output_folder, exist_ok=True)
        save_path = os.path.join(output_folder, save_name)
        cv2.imwrite(save_path, thresh)
        print(f"Preprocessed image saved to: {save_path}")

    return thresh