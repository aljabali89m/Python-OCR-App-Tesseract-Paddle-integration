## 🚀 Getting Started

### 1. Prerequisites
* **Python 3.11**: Recommended for library stability and compatibility.
* **Tesseract OCR**: Must be installed on your system with the path updated in `tesseract_ocr.py`.
* **Poppler**: Required for the `pdf2image` library to process PDF documents.

### 2. Installation
* **Clone the Repository**: `git clone https://github.com/aljabali89m/OCR-Studio.git`
* **Install Dependencies**: Run `pip install -r requirements.txt` to install all necessary packages.

### 3. Usage
* **Launch the App**: Run `python gui.py` to open the main graphical interface.
* **Select Engine**: Choose between **Tesseract** (recommended for Arabic) or **PaddleOCR** from the sidebar.
* **Upload File**: Select an image or PDF to begin the automated preprocessing pipeline.
* **Extract & Save**: View the results in the preview panel and save the output as a `.txt` file.

---

## 🔍 Engine Comparison & Technical Insights

This project integrates two distinct OCR architectures to provide a comprehensive benchmarking environment. Below is a breakdown of their technical nature and real-world performance within this application.

### 🧩 Tesseract OCR
Tesseract is a mature, open-source OCR engine currently maintained by Google.
* **Architecture**: It utilizes a deep learning-based system powered by **LSTM** (Long Short-Term Memory) networks to recognize character sequences.
* **Integration**: Accessed via the `pytesseract` wrapper, it requires a local engine installation on the host OS.
* **Strengths**: It is highly reliable for standard Latin-based scripts and provides solid, multi-language support through trained data files.

### 🌊 PaddleOCR
PaddleOCR is a modern, high-performance OCR toolkit based on the **PaddlePaddle** deep learning framework.
* **Architecture**: It employs the **PP-OCR** system, which uses a modular approach involving text detection, direction classification, and text recognition.
* **Optimization**: Designed for speed and efficiency, it can leverage GPU acceleration for high-volume document processing.
* **Implementation**: Managed entirely through Python packages, making it highly portable across different development environments.

---

### 📊 Comparative Analysis
Based on testing results recorded in `conclusion.txt`, here is the comparative performance breakdown:

| Feature | Tesseract | PaddleOCR |
| :--- | :--- | :--- |
| **English Accuracy** | Delivered clean, highly accurate results with minimal errors. | Performed well but was not the primary standout for Latin text. |
| **Arabic Support** | Performed reasonably well and is acceptable for most use cases. | Struggled significantly, producing poor and largely unusable output. |
| **Mixed Content** | Handled English + Arabic at a moderate level with decent accuracy. | Failed to produce coherent results for the Arabic portions of mixed documents. |
| **Setup Type** | Requires local OS engine installation and path configuration. | Managed via Python package managers (`pip`). |



---

<h2 align="left">Contributor</h2>

<p align="left">
  <strong>Mohammad Aljabali</strong>
  <br> AI Engineer | LLMs & RAG Specialist <br>
</p>

<div align="center">
  <a href="https://www.linkedin.com/in/aljabali89m/" target="_blank">
    <img src="https://raw.githubusercontent.com/maurodesouza/profile-readme-generator/master/src/assets/icons/social/linkedin/default.svg" width="40" height="30" alt="linkedin logo" />
  </a>
  <a href="mailto:aljabali89m@gmail.com" target="_blank">
    <img src="https://raw.githubusercontent.com/maurodesouza/profile-readme-generator/master/src/assets/icons/social/gmail/default.svg" width="40" height="30" alt="gmail logo" />
  </a>
</div>
