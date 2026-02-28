# Python-OCR-App-Tesseract-Paddle-integration

<div align="center">
  <img height="200" src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZW8yaHMydjhvMXFkcmF3bGUxZnJib3g5a2I2dDNoZHlkM282aGhydyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/fZoKDBwdbILBjhtXZD/giphy.gif" />
</div>

<h1 align="center">🚀 OCR Studio</h1>

<p align="center">
  <strong>نظام متقدم لاستخراج النصوص يدعم اللغتين العربية والإنجليزية مع معالجة صور ذكية باستخدام محركات Tesseract و PaddleOCR</strong>
</p>

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/GUI-CustomTkinter-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/OCR-Tesseract%20%26%20Paddle-red?style=for-the-badge" />
</div>

---

## 📝 وصف المشروع
[cite_start]يوفر **OCR Studio** منصة متكاملة لتحويل الصور وملفات PDF إلى نصوص قابلة للتعديل[cite: 1]. تم بناء النظام ليعمل بمرونة عالية، حيث يتيح للمستخدم المقارنة بين أداء محركين عالميين، مع واجهة رسومية عصرية تدعم الوضع الليلي ومعاينة النتائج فورياً.

---

## 🏗️ كيف يعمل النظام (Core Logic)
يمر كل مستند يتم رفعه بسلسلة من العمليات التقنية لضمان دقة الاستخراج:

* **تحويل الرمادي (Grayscale):** لتبسيط البيانات الصورية.
* **إزالة الضوضاء (Gaussian Blur):** للتخلص من الشوائب التي تعيق التعرف.
* **العتبة التكيفية (Adaptive Thresholding):** لفصل الحروف عن الخلفية بوضوح تام.



---

## 📊 مقارنة الأداء (Performance Insights)
بناءً على الاختبارات المكثفة للمشروع، تم التوصل للخلاصات التالية:

* [cite_start]**اللغة الإنجليزية:** قدم Tesseract نتائج نظيفة ودقيقة جداً مع حد أدنى من الأخطاء[cite: 2].
* [cite_start]**اللغة العربية:** أداء Tesseract كان مقبولاً وجيداً لمعظم الحالات [cite: 3][cite_start]، بينما واجه PaddleOCR صعوبات كبيرة أنتجت مخرجات ضعيفة[cite: 4].
* [cite_start]**المحتوى المختلط:** تعامل Tesseract مع اللغتين معاً بمستوى متوسط [cite: 5][cite_start]، في حين فشل PaddleOCR في إنتاج نتائج متماسكة للأجزاء العربية[cite: 5].

---

## 🛠️ الأدوات والتقنيات (I code with)

<div align="left">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="40" alt="python logo" />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg" height="40" alt="numpy logo" />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/opencv/opencv-original.svg" height="40" alt="opencv logo" />
  <img width="12" />
  <img src="https://raw.githubusercontent.com/otter-ai/tesseract-python/master/logo.png" height="40" alt="tesseract logo" />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" height="40" alt="github logo" />
</div>

---

## 🚀 تعليمات التشغيل

1. **إعداد البيئة:** تأكد من استخدام **Python 3.11** لضمان استقرار المكتبات.
2. **تثبيت المكتبات:**
   ```bash
   pip install -r requirements.txt
