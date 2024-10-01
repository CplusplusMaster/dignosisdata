import cv2
import numpy as np
import pytesseract
from PIL import Image

# Tesseract 경로 설정 (윈도우의 경우 필요)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 이미지 자르기 함수 (가장 큰 사각형 영역 검출)
def crop_to_document(image):
    # 이미지를 그레이스케일로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 이미지 이진화 (테두리 강조)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # 윤곽선 검출
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 가장 큰 사각형 영역 찾기
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    # 사각형 영역으로 이미지 자르기
    cropped_image = image[y:y+h, x:x+w]
    return cropped_image

# 텍스트 추출 함수
def extract_text_from_image(image_path):
    # 이미지 읽기
    image = cv2.imread(image_path)
    
    text = pytesseract.image_to_string(image, lang='kor')
    
    return text

# 이미지 경로
#image_path = 'data/src/original.jpg'
image_path = 'data/preprocessed/2_edged.jpg'

# 텍스트 추출
extracted_text = extract_text_from_image(image_path)

# 결과 출력
print(extracted_text)


