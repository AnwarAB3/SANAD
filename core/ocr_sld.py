import json
from pathlib import Path

import cv2
import numpy as np


def extract_text(
    image_path: str,
    engine: str = "easy",
    lang_mode: str = "en",
    min_conf: float = 0.0,
    save_json: str | None = None,
):
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    img = cv2.imread(str(image_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    results = []

    if engine == "easy":
        import easyocr

        langs = ["en"] if lang_mode == "en" else ["en", "ar"]
        reader = easyocr.Reader(langs, gpu=False)
        ocr_results = reader.readtext(gray, detail=1)

        for bbox, text, conf in ocr_results:
            if conf >= min_conf:
                results.append({"text": text, "confidence": float(conf)})

    else:
        from paddleocr import PaddleOCR

        lang = "arabic" if lang_mode == "ar" else "en"
        ocr = PaddleOCR(use_angle_cls=True, lang=lang, show_log=False)
        ocr_results = ocr.ocr(img, cls=True)

        if ocr_results and ocr_results[0]:
            for line in ocr_results[0]:
                text, conf = line[1]
                if conf >= min_conf:
                    results.append({"text": text, "confidence": float(conf)})

    output = {
        "image": str(image_path),
        "engine": engine,
        "language": lang_mode,
        "count": len(results),
        "texts": results,
    }

    if save_json:
        with open(save_json, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

    return output
