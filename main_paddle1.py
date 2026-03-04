import os
from preprocessing import preprocess_image, preprocess_numpy_image, pdf_to_images
from paddle_ocr import run_ocr

INPUT_FOLDER = "Data"
OUTPUT_FOLDER = "Output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Image files 
IMAGE_FILES = {
    "english_sample.png": "eng",
    "arabic_sample.png":  "ara",
    "mixed_sample.png":   "eng+ara",
}

# Process pdf
PDF_FILES = {
    "1.pdf": "eng",
}

# Process image files
for file_name, lang in IMAGE_FILES.items():
    image_path = os.path.join(INPUT_FOLDER, file_name)

    if not os.path.exists(image_path):
        print(f"[SKIP] File not found: {image_path}")
        continue

    print(f"\nProcessing image: {file_name}  (lang={lang})")

    processed_image = preprocess_image(
        image_path, save_output=True, output_folder=OUTPUT_FOLDER
    )

    text = run_ocr(processed_image, language=lang)

    #arabic_sample.png → arabic_sample_PADDLE.txt
    base_name = os.path.splitext(file_name)[0]
    output_file = f"{base_name}_PADDLE.txt"
    output_path = os.path.join(OUTPUT_FOLDER, output_file)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"  ✓ Saved → {output_path}")

# Process PDF files
for file_name, lang in PDF_FILES.items():
    pdf_path = os.path.join(INPUT_FOLDER, file_name)

    if not os.path.exists(pdf_path):
        print(f"[SKIP] File not found: {pdf_path}")
        continue

    print(f"\nProcessing PDF: {file_name}  (lang={lang})")

    pages = pdf_to_images(pdf_path)  # list of numpy arrays, one per page
    all_text = []

    for page_num, page_image in enumerate(pages, start=1):
        print(f"  → Page {page_num}/{len(pages)}")

        save_name = (
            f"preprocessed_{file_name.replace('.pdf', '')}_page{page_num}.png"
        )
        processed_page = preprocess_numpy_image(
            page_image,
            save_output=True,
            output_folder=OUTPUT_FOLDER,
            save_name=save_name,
        )

        page_text = run_ocr(processed_page, language=lang)
        all_text.append(f"--- Page {page_num} ---\n{page_text}")

    # 1.pdf → 1_PADDLE.txt
    base_name = os.path.splitext(file_name)[0]
    output_file = f"{base_name}_PADDLE.txt"
    output_path = os.path.join(OUTPUT_FOLDER, output_file)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_text))

    print(f"  ✓ Saved → {output_path}")