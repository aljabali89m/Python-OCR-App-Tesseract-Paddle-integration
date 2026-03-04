import os
from paddleocr import PaddleOCR
import numpy as np
import cv2
import tempfile

# language codes
LANG_MAP = {
    "eng":     "en",
    "ara":     "ar",
    "eng+ara": "ar",   # ar handles both
}

_ocr_instances: dict[str, PaddleOCR] = {}


def _get_ocr(language: str) -> PaddleOCR:
    if language not in _ocr_instances:
        _ocr_instances[language] = PaddleOCR(
            use_angle_cls=True,
            lang=language,
            use_gpu=False,
            enable_mkldnn=False,
            show_log=False,   
        )
    return _ocr_instances[language]


def run_ocr(image: np.ndarray, language: str = "eng") -> str:

    paddle_lang = LANG_MAP.get(language, "en")
    ocr = _get_ocr(paddle_lang)

    # PaddleOCR needs BGR input
    if image.ndim == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".png")
    os.close(tmp_fd)

    try:
        cv2.imwrite(tmp_path, image)
        result = ocr.ocr(tmp_path, cls=True)   
    finally:
        os.remove(tmp_path)

    lines = []

    if result is None:
        return ""

    for page in result:
        if page is None:
            continue

        if isinstance(page, list):
            for line in page:
                if line and len(line) >= 2:
                    text_info = line[1]
                    if isinstance(text_info, (list, tuple)) and len(text_info) >= 1:
                        text = text_info[0]
                        if text and text.strip():
                            lines.append(text.strip())

        elif isinstance(page, dict):
            for text in page.get("rec_texts", []):
                if text and text.strip():
                    lines.append(text.strip())

    return "\n".join(lines)