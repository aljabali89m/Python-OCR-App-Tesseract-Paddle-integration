<div align="center">
  <img height="200" src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZW8yaHMydjhvMXFkcmF3bGUxZnJib3g5a2I2dDNoZHlkM282aGhydyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/fZoKDBwdbILBjhtXZD/giphy.gif"  />
</div>

<h1 align="center">🚀 OCR Studio</h1>

<p align="center">
  <strong>An advanced Optical Character Recognition system supporting English & Arabic with intelligent image preprocessing</strong>
</p>

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/GUI-CustomTkinter-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/OCR-Tesseract%20%26%20Paddle-red?style=for-the-badge" />
</div>

---

## 📝 Project Overview
**OCR Studio** is a comprehensive platform designed to convert images and PDF documents into editable text. Built with **Python 3.11**, the system allows users to toggle between two powerful OCR engines (**Tesseract** and **PaddleOCR**) while providing a modern GUI for real-time preview and result management.

---

## 🏗️ Core Logic & Pipeline
To ensure maximum accuracy, every document undergoes a specific image processing pipeline before text extraction:

* **Grayscale Conversion**: Reduces data complexity for faster processing.
* **Noise Removal (Gaussian Blur)**: Eliminates artifacts and "salt-and-pepper" noise.
* **Adaptive Thresholding**: Dynamically separates text from the background based on local pixel intensity.



---

## 📊 Performance Insights & Benchmarking
Based on rigorous testing within the application:

* **English Content**: Tesseract delivered exceptionally clean and accurate results with minimal errors.
* **Arabic Content**: Tesseract performed reasonably well and is suitable for most use cases, whereas PaddleOCR struggled significantly, producing poor output.
* **Mixed Content**: Tesseract handled dual languages at a moderate level, while PaddleOCR failed to produce coherent results for Arabic portions.

---

## 🛠️ Tech Stack (I code with)

<div align="left">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="40" alt="python logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg" height="40" alt="numpy logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/opencv/opencv-original.svg" height="40" alt="opencv logo"  />
  <img width="12" />
  <img src="https://raw.githubusercontent.com/otter-ai/tesseract-python/master/logo.png" height="40" alt="tesseract logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" height="40" alt="github logo"  />
</div>

---

## 🚀 Getting Started

### 1. Prerequisites
* **Python 3.11** is highly recommended for library stability.
* **Tesseract OCR**: Must be installed on your OS. Update the path in `tesseract_ocr.py`.
* **Poppler**: Required for the `pdf2image` library to handle PDF files.

### 2. Installation
```bash
pip install -r requirements.txt

3. Usage
Run the main GUI application:

Bash
python gui.py
<p align="center">
Developed by <strong>Mohammad Aljabali</strong> - AI Scientist & Flutter Developer
</p>


-----

Would you like me to generate a **setup.sh** or **install.bat** script to automate the environment configuration f
