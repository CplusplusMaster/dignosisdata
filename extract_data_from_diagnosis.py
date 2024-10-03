

import os
import re
import cv2
import pytesseract
import pdfplumber
import csv
import json
from PIL import Image
from rotate_image import rotate_image_by_detected_angle  # 회전 모듈 가져오기
from find_table import detect_table

# Tesseract 설정 (필요한 경우 경로 설정)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows일 경우 Tesseract 경로

# CSV 파일 경로 설정
UPLOAD_FOLDER = 'uploads'
CSV_FILE = 'extracted_data.csv'
# 패턴 정의 (찾고자 하는 항목들)
patterns = {
    "소유자명": r"동물 소유자 성명\s?([가-힣]+)",
    "주소": r"주소\s?:\s?(.+?(?:도|시|구|동|로|길))",
    "사육장소": r"사육장소\s?:\s?(.+?(?:도|시|구|동|로|길))",
    "연락처": r"전화번호\s?:\s?([\d\-]+)",
    "동물명": r"동물명\(동물등록번호\)\s(.+?)\s",
    "품종": r"품종\s(.+?)\s",
    "성별": r"성별\s(암컷|수컷)",
    "연령": r"연령\s(\d+세)",
    "모색": r"모색\s(.+?)\s",
    "특징": r"특징\s(.+?)(?:\n|병명|주요\s증상)",
    "병명": r"병명\s*(?:임상적 추정\s*\(\s*\)|최종 진단\s*\(\s*\))\s*(.+?)(?=\s|발병 연월일)",
    "발병 연월일": r"발병 연월일\s([0-9]{4}-[0-9]{2}-[0-9]{2})",
    "진단 연월일": r"진단 연월일\s([0-9]{4}-[0-9]{2}-[0-9]{2})",
    "주요 증상": r"주요 증상\s?(.+?)(?=\s치료명칭)",
    "치료명칭": r"치료명칭\s?(.+?)(?=\s입원\*퇴원일)",
    "입원*퇴원일": r"입원\*퇴원일\s([0-9]{4}-[0-9]{2}-[0-9]{2}\s~\s[0-9]{4}-[0-9]{2}-[0-9]{2})",
    "예후 소견": r"예후 소견\s(.+?)(?:\n|그 밖의 사항|\d)",
    "그 밖의 사항": r"그 밖의 사항\s(.+?)\s1\.",
    "동물병원 명칭": r"동물병원 명칭:\s?(.+?)\s동물병원 주소",
    "동물병원 주소": r"동물병원 주소:\s?(.+?(?:도|시|구|동|로|길))",
    "수의사 성명": r"수의사 성명\s(.+?)\(",
    "수의사 면허번호": r"수의사 면허번호:\s?제?\s?(\d+)\s?(\d+)",
}



# 폴더가 없으면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def extract_text_from_image(image_path):
    """
    이미지에서 텍스트를 추출하는 함수
    """
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='kor')
    #print(f"Extracted text: {text}")  # 텍스트 확인
    return text


def extract_text_from_pdf(pdf_path):
    """
    PDF에서 텍스트를 추출하는 함수
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    #print(f"Extracted text from PDF: {text}")  # 텍스트 확인
    return text


def parse_text(text):
    """
    텍스트에서 정규 표현식을 사용해 패턴에 맞는 정보를 추출하는 함수
    """
    text = re.sub(r'\s+', ' ', text).strip()  # 공백 제거 및 여러 개의 공백을 하나로
    parsed_data = {}

    # 각 패턴을 탐색하여 값 추출
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            parsed_data[key] = match.group(1).strip() if key != "수의사 면허번호" else match.group(1).strip() + match.group(2).strip()

    return parsed_data


def write_to_csv(data, csv_file):
    """
    파싱된 데이터를 CSV 파일에 저장하는 함수
    """
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)


def image_process_rotate(image_path):
    """
    이미지가 제대로 정렬되지 않은 경우 회전하여 텍스트를 다시 추출하고 패턴에 맞게 값을 추출
    """
    # 이미지 정렬
    rotated_image, _ = rotate_image_by_detected_angle(image_path)

    # 회전된 이미지를 임시 파일로 저장
    temp_image_path = "rotated_temp.jpg"
    cv2.imwrite(temp_image_path, rotated_image)

    # 회전된 이미지에서 텍스트 추출
    rotated_text = extract_text_from_image(temp_image_path)

    # 임시 파일 삭제
    os.remove(temp_image_path)

    return rotated_text


def main():
    # 파일 경로 입력받기
    file_path = input("파일 경로를 입력하세요 (이미지 또는 PDF): ").strip()
    
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

    # 텍스트에서 정보 파싱
    parsed_data = parse_text(extracted_text)
    #print(f"초기 추출된 데이터: {json.dumps(parsed_data, ensure_ascii=False, indent=4)}")

    # 누락된 데이터가 있는 경우 이미지 회전 후 재시도
    if len(parsed_data) < len(patterns):
        print("일부 데이터가 누락되었습니다. 이미지 회전 후 재시도 중...")
        rotated_text = image_process_rotate(file_path)
        additional_data = parse_text(rotated_text)
        parsed_data.update({k: v for k, v in additional_data.items() if k not in parsed_data})

    # 누락된 데이터가 있는 경우 이미지에서 객체를 탐지하여
    # 해당 부분을 오려낸 후 재시도 이부분 수정 
    if len(parsed_data) < len(patterns):
        print("일부 데이터가 누락되었습니다. 객체 탐지 후 재시도 중...")
        detect_table(file_path)  # 객체 탐지 및 저장 함수 호출

        # 저장된 객체 이미지에서 텍스트 추출
        for i in range(len(os.listdir("extracted_objects"))):
            object_image_path = f"extracted_objects/object_{i}.jpg"
            if os.path.exists(object_image_path):
                extracted_text = extract_text_from_image(object_image_path)
                additional_data = parse_text(extracted_text)
                parsed_data.update({k: v for k, v in additional_data.items() if k not in parsed_data})


    #print(f"최종 추출된 데이터: {json.dumps(parsed_data, ensure_ascii=False, indent=4)}")

    # CSV 파일에 데이터 저장
    write_to_csv(parsed_data, CSV_FILE)
    print(f"데이터가 {CSV_FILE}에 저장되었습니다.")

if __name__ == "__main__":
    main()

