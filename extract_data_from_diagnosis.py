import os
import re
import cv2
import pytesseract
import pdfplumber
import csv
import json
import difflib
from PIL import Image
from fuzzywuzzy import fuzz

from rotate_image import rotate_image_by_detected_angle 
from find_objects import detect_table
from data_analysis import calculate_metrics, performance_improvement
from input_data import input_data,extract_text_from_image,extract_text_from_pdf,write_to_csv

# Tesseract 설정 (필요한 경우 경로 설정)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows일 경우 Tesseract 경로

# CSV 파일 경로 설정
UPLOAD_FOLDER = 'uploads'
CSV_FILE = 'extracted_data.csv'
# 패턴 정의 (찾고자 하는 항목들)

# 폴더가 없으면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Levenshtein Distance를 이용한 유사도 계산 함수
def calculate_similarity(text1, text2):
    """
    두 텍스트 간의 Levenshtein 유사도를 계산하여 반환.
    """
    return fuzz.ratio(text1, text2)

# 음운적 유사도 비교를 위한 자모 분해 함수
def jamo_split(text):
    """
    한글 자모 분해를 통해 초성, 중성, 종성 단위로 분리하여 반환.
    """
    CHOSUNG_START = 4352
    JAMO_START = 44032

    def split_char(char):
        if ord(char) < JAMO_START or ord(char) > 55203:
            return char  # 한글이 아닌 경우 그대로 반환
        base = ord(char) - JAMO_START
        chosung = base // 588
        jung = (base - chosung * 588) // 28
        jong = base % 28
        return (chr(4352 + chosung), chr(4449 + jung), chr(4519 + jong) if jong > 0 else '')

    return ''.join([elem for char in text for elem in split_char(char)])

# 두 텍스트의 자모 기반 유사도 측정 함수
def phonetic_similarity(text1, text2):
    """
    자모 분해 후 두 문자열을 자모 단위로 비교하여 유사도를 계산.
    """
    jamo1, jamo2 = jamo_split(text1), jamo_split(text2)
    return difflib.SequenceMatcher(None, jamo1, jamo2).ratio()

# 텍스트와 키워드의 유사도를 기반으로 최적의 키워드를 찾는 함수
def find_best_match(keyword, candidates, similarity_threshold=70, phonetic_threshold=0.7):
    """
    주어진 후보군 중에서 keyword와 가장 유사한 단어를 찾음.
    두 가지 기준 (텍스트 유사도와 음운적 유사도)을 모두 사용하여 가장 유사한 단어를 반환.
    """
    best_match = None
    best_score = 0  # 초기화된 최적 유사도 점수

    # 키워드가 여러 단어로 구성된 경우 처리
    keyword_tokens = keyword.split()
    keyword_length = len(keyword_tokens)

    for i in range(len(candidates) - keyword_length + 1):
        # 후보군에서 keyword와 동일한 길이의 연속된 단어 조합을 만듦
        candidate_phrase = " ".join(candidates[i:i + keyword_length])

        # Levenshtein Distance와 자모 기반 유사도 계산
        text_similarity = calculate_similarity(keyword, candidate_phrase)
        phonetic_score = phonetic_similarity(keyword, candidate_phrase)

        # 두 유사도의 평균을 최종 유사도로 사용
        combined_score = (text_similarity / 100 + phonetic_score) / 2

        # 특정 유사도 기준을 넘는 경우 최적 후보로 설정
        if combined_score > best_score and (text_similarity >= similarity_threshold or phonetic_score >= phonetic_threshold):
            best_score = combined_score
            best_match = candidate_phrase

    return best_match

# JSON 키와 추출한 텍스트 간 매칭을 수행하는 함수
def extract_and_match_keys(json_keys, extracted_text, cutoff=0.8):
    # 공백과 특수문자를 제거하여 데이터를 정리하는 함수 띄어쓰기로 구분되는 key 존재 '치료 명칭, 주요 증상 등' 오히려 인식 방해
    # def clean_text(text):
    #     return re.sub(r'\s+', '', text).strip()

    # 공백을 줄여주고 데이터 정리
    extracted_text = re.sub(r'\s+', ' ', extracted_text).strip()
    # print("정리된 추출 텍스트:")
    # print(extracted_text)

    # 결과를 저장할 딕셔너리 키: 값 구조 세팅
    result = {key: "" for key in json_keys}
 
    # 각 키에 대해 텍스트에서 매칭되는 부분을 찾음
    for i, key in enumerate(json_keys):
        # 유사도 분석을 위해 공백 제거 후 정리된 키 텍스트
        #cleaned_key = clean_text(key)
        cleaned_key = key
        # print("cleaned")
        # print(cleaned_key)
        # 가장 유사한 텍스트 찾기
        #closest_match = find_best_match(cleaned_key, [word for word in extracted_text.split()])

        # 텍스트에서 단어들을 리스트로 나눔 두 단어 이상으로 구성된 키를 찾기 위해
        candidate_words = extracted_text.split()

        # cleaned_key가 두 단어 이상이면 연속된 단어로 찾도록 수정
        if len(cleaned_key.split()) > 1:
            # 가장 유사한 텍스트 찾기 (연속된 단어 조합을 찾아 매칭)
            closest_match = find_best_match(cleaned_key, candidate_words)
        else:
            # 단일 단어의 경우 기존 방식 유지
            closest_match = find_best_match(cleaned_key, candidate_words)
        
        # print("closest")
        # print(closest_match)
        if closest_match:
            matched_keyword = closest_match
            # 매칭된 키워드 다음에 나오는 값을 추출
            next_key_match = None
            remaining_keys = json_keys[i + 1:]  # 현재 키 이후의 나머지 키들
            for next_key in remaining_keys:
                #next_key_clean = clean_text(next_key)
                #print("next_key_clean")
                #print(next_key_clean)
                #####
                # 텍스트에서 단어들을 리스트로 나눔
                candidate_words = extracted_text.split()

                # cleaned_key가 두 단어 이상이면 연속된 단어로 찾도록 수정
                if len(next_key.split()) > 1:
                    # 가장 유사한 텍스트 찾기 (연속된 단어 조합을 찾아 매칭)
                    next_closest_match = find_best_match(next_key, candidate_words)
                else:
                    # 단일 단어의 경우 기존 방식 유지
                    next_closest_match = find_best_match(next_key, candidate_words)
                ###
               #next_closest_match = find_best_match(next_key_clean, [clean_text(word) for word in extracted_text.split()])
                # print("nextclosestmatch")
                # print(next_closest_match)
                if next_closest_match:
                    next_key_match = next_closest_match
                    break  # 매칭되는 첫 키를 찾으면 중단

            # 다음 키워드가 있는 경우 그 사이의 텍스트를 추출
            if next_key_match:
                pattern = re.escape(matched_keyword) + r"\s*([\S\s]+?)\s+" + re.escape(next_key_match)
            else:
                # 다음 키가 없으면 끝까지 추출
                pattern = re.escape(matched_keyword) + r"\s*([\S\s]+?)$"

            match = re.search(pattern, extracted_text)

            if match:
                # 추출된 값을 result에 저장
                result[key] = match.group(1).strip()

    return result



# 기울어진 사진을 0'와 최대한 가깝게 회전시키는 함수
def image_process_rotate(json_keys, image_path, parsed_data):
    # 누락된 값이 있는지 확인
    empty_keys = find_empty_values(parsed_data)
    if empty_keys:
        print(f"누락된 데이터가 발견되었습니다: {empty_keys}")
        
        # 이미지 정렬
        rotated_image, _ = rotate_image_by_detected_angle(image_path)

        # 회전된 이미지를 임시 파일로 저장
        temp_image_path = "rotated_temp.jpg"
        cv2.imwrite(temp_image_path, rotated_image)

        # 회전된 이미지에서 텍스트 추출
        rotated_text = extract_text_from_image(temp_image_path)
        rotated_data = extract_and_match_keys(json_keys, rotated_text, cutoff=0.7)

        # 누락된 키만 업데이트 (기존 값이 없는 키만 교체)
        for key in empty_keys:
            if key in rotated_data and rotated_data[key]:  # 회전 후 데이터가 있으면
                parsed_data[key] = rotated_data[key]

        # 임시 파일 삭제
        os.remove(temp_image_path)
        
        print(f"회전 후 누락된 데이터가 채워졌습니다: {json.dumps(parsed_data, ensure_ascii=False, indent=4)}")
    else:
        print("누락된 데이터가 없습니다. 회전이 필요하지 않습니다.")

    return parsed_data

# 테이블 탐지를 통해 사진에서 진단서의 텍스트 부분만 추출
def image_process_with_object_detection(json_keys, image_path, parsed_data):
    # 누락된 값이 있는지 확인
    empty_keys = find_empty_values(parsed_data)
    
    if empty_keys:
        print(f"누락된 데이터가 발견되었습니다: {empty_keys}")
        print("객체 탐지 후 텍스트 추출을 시도합니다...")

        # 객체 탐지 및 이미지 분리
        detect_table(image_path)  # detect_table 함수를 통해 객체 추출

        # 저장된 객체 이미지에서 텍스트 추출
        extracted_dir = "extracted_objects"
        for i in range(len(os.listdir(extracted_dir))):
            object_image_path = os.path.join(extracted_dir, f"object_{i}.jpg")
            if os.path.exists(object_image_path):
                # 각 객체 이미지에서 텍스트 추출
                object_extracted_text = extract_text_from_image(object_image_path)
                # 추출한 텍스트에서 필요한 키 매칭
                additional_data = extract_and_match_keys(json_keys, object_extracted_text, cutoff=0.7)

                # 누락된 키 값만 업데이트
                for key in empty_keys:
                    if key in additional_data and additional_data[key]:
                        parsed_data[key] = additional_data[key]
        
        # 최종 업데이트된 데이터 출력
        print(f"객체 탐지 후 추출된 데이터: {json.dumps(parsed_data, ensure_ascii=False, indent=4)}")
    else:
        print("누락된 데이터가 없습니다. 객체 탐지가 필요하지 않습니다.")
    
    return parsed_data

# 설정한 키 패러미터들에 빈 값이 들어가는 경우(특정 키에 해당하는 값을 못 찾는 경우) 확인
def find_empty_values(data, parent_key=''):
    empty_keys = []  # 빈 값을 가진 키 목록 저장
    
    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{parent_key}.{key}" if parent_key else key  # 중첩된 경우 키 경로 저장
            if value == "":  # 값이 빈 문자열이면
                empty_keys.append(full_key)
            elif isinstance(value, (dict, list)):  # 딕셔너리나 리스트일 경우 재귀적으로 탐색
                empty_keys.extend(find_empty_values(value, full_key))
    
    elif isinstance(data, list):
        for index, item in enumerate(data):
            full_key = f"{parent_key}[{index}]"  # 리스트의 경우 인덱스를 경로로 사용
            if item == "":  # 리스트 항목이 빈 문자열이면
                empty_keys.append(full_key)
            elif isinstance(item, (dict, list)):  # 리스트 항목이 딕셔너리나 리스트일 경우 재귀적으로 탐색
                empty_keys.extend(find_empty_values(item, full_key))

    return empty_keys


