import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust path

def read_timer(frame: np.ndarray) -> int | None:
    # ROI for timer (top center, assuming 1920x1080)
    timer_roi = frame[30:80, 860:1060]
    gray = cv2.cvtColor(timer_roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    text = pytesseract.image_to_string(thresh, config='--psm 7 digits')
    try:
        if ':' in text:
            mins, secs = map(int, text.strip().split(':'))
            return mins * 60 + secs
        return int(text)
    except ValueError:
        return None