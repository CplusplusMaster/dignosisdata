import os
import pdfplumber
from PIL import Image
import pytesseract
import csv
import json

# 이미지에서 텍스트를 추출하는 함수
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='kor')
    #print(f"Extracted text: {text}")  # 텍스트 확인
    return text

# PDF에서 텍스트를 추출하는 함수
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    #print(f"Extracted text from PDF: {text}")  # 텍스트 확인
    return text

# 파싱된 데이터를 CSV 파일에 저장하는 함수
def write_to_csv(data, csv_file):
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)


def input_data():
    # 파일 경로 입력받기
    file_path = input("사진 파일 경로를 입력하세요 (이미지 또는 PDF): ").strip()
    file_text_path = input("사진 텍스트 데이터 파일 경로를 입력하세요 (JSON): ").strip()
    json_file_path = 'key_for_diagnosis_data.json'
    json_key_weights = 'weight_key.json'

    # 데이터 분석을 위해 실제 진단서 사진에서 추출 가능한 텍스트를 정리해둔 json 파일에서 텍스트 추출
    with open(file_text_path,'r',encoding="utf-8") as text_file:
        text_data =json.load(text_file)

    # json형식의 파일에서 키 추출
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        keys_data = json.load(json_file)
    json_keys = list(keys_data.keys())

    # 각 키마다 가중치 부여(특히 중요한 키에 대한 데이터가 well match한지 확인하기 위해)
    with open(json_key_weights,'r',encoding="utf-8") as text_file:
        keys_weights =json.load(text_file)

    if not os.path.isfile(file_path):
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return

    # 파일 확장자에 따라 텍스트 추출
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        extracted_text = extract_text_from_image(file_path)
    elif file_path.lower().endswith('.pdf'):
        extracted_text = extract_text_from_pdf(file_path)
    else:
        print(f"지원되지 않는 파일 형식입니다: {file_path}")
        return
    return file_path, text_data, json_keys, keys_weights, extracted_text