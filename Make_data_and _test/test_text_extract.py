import cv2
import numpy as np
import pytesseract
from PIL import Image
import re

# Tesseract 경로 설정 (윈도우의 경우 필요)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# 텍스트 추출 함수
def extract_text_from_image(image_path):
    # 이미지 읽기
    image = cv2.imread(image_path)
    
    text = pytesseract.image_to_string(image, lang='kor')
    
    return text


# 이미지 경로
#image_path = 'data/src/object_data1.jpg'
#image_path = 'image.png'
image_path = 'enhanced_image.jpg'


# 텍스트 추출
extracted_text = extract_text_from_image(image_path)

print(extracted_text)
