import os
import re
import cv2
import pytesseract
import pdfplumber
import csv
import json
from PIL import Image
from rotate_image import rotate_image_by_detected_angle  # 회전 모듈 가져오기
from find_objects import detect_table
from data_analysis import calculate_metrics, performance_improvement
import difflib

# Tesseract 설정 (필요한 경우 경로 설정)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows일 경우 Tesseract 경로

# CSV 파일 경로 설정
UPLOAD_FOLDER = 'uploads'
CSV_FILE = 'extracted_data.csv'
# 패턴 정의 (찾고자 하는 항목들)

# 폴더가 없으면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


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

def extract_and_match_keys(json_keys, extracted_text, cutoff=0.8):
    # 공백과 특수문자를 제거하여 데이터를 정리
    def clean_text(text):
        return re.sub(r'\s+', '', text).strip()
    
    # 공백을 줄여주고 데이터 정리
    extracted_text = re.sub(r'\s+', ' ', extracted_text).strip()
    print("extracted")
    print(extracted_text)
    

    # 결과를 저장할 딕셔너리
    result = {key: "" for key in json_keys}
    
    # 각 키에 대해 텍스트에서 매칭되는 부분을 찾음
    for i, key in enumerate(json_keys):
        # 공백을 제거한 상태에서 유사도 분석
        cleaned_key = clean_text(key)
        closest_match = difflib.get_close_matches(cleaned_key, [clean_text(word) for word in extracted_text.split()], n=1, cutoff=cutoff)
        #print(closest_match)
        if closest_match:
            matched_keyword = closest_match[0]
            # 매칭된 키워드 다음에 나오는 값을 추출
            # 남은 키들 중에서 매칭되는 첫 키를 찾음
            next_key_match = None
            remaining_keys = json_keys[i+1:]  # 현재 키 이후의 나머지 키들
            for next_key in remaining_keys:
                next_closest_match = difflib.get_close_matches(clean_text(next_key), [clean_text(word) for word in extracted_text.split()], n=1, cutoff=cutoff)
                if next_closest_match:
                    next_key_match = next_closest_match[0]
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
                # 추출한 텍스트에서 이미 추출한 데이터 삭제 먼가 먼가 결과가 영 별로인데
                #extracted_text = extracted_text.replace(match.group(0), "").strip()
    return result


# def extract_and_match_keys(json_keys, extracted_text, cutoff=0.8):
#     # 1. 공백과 특수문자를 제거하여 데이터를 정리하는 함수
#     def clean_text(text):
#         return re.sub(r'\s+', '', text).strip()
    
#     # 2. 공백을 줄여주고 데이터 정리
#     extracted_text = re.sub(r'\s+', '', extracted_text).strip()
    
#     # 3. 결과를 저장할 딕셔너리 초기화
#     result = {key: "" for key in json_keys}
    
#     # 4. 첫 번째 방법: difflib을 사용하여 유사도 기반 키 매칭 시도
#     unmatched_keys = []  # 첫 번째 방법에서 매칭되지 않은 키들을 저장할 리스트
#     for i, key in enumerate(json_keys):
#         # 키의 공백을 제거하여 유사도 분석
#         cleaned_key = clean_text(key)
        
#         # 5. extracted_text를 공백 단위로 분리하여 각 단어의 유사도 분석
#         closest_match = difflib.get_close_matches(cleaned_key, [clean_text(word) for word in extracted_text.split()], n=1, cutoff=cutoff)
        
#         if closest_match:
#             matched_keyword = closest_match[0]
#             # 다음 키워드를 찾음
#             next_key_match = None
#             remaining_keys = json_keys[i+1:]
#             for next_key in remaining_keys:
#                 next_closest_match = difflib.get_close_matches(clean_text(next_key), [clean_text(word) for word in extracted_text.split()], n=1, cutoff=cutoff)
#                 if next_closest_match:
#                     next_key_match = next_closest_match[0]
#                     break

#             # 다음 키워드가 있는 경우 그 사이의 텍스트를 추출
#             if next_key_match:
#                 pattern = re.escape(matched_keyword) + r"\s*([\S\s]+?)\s+" + re.escape(next_key_match)
#             else:
#                 # 다음 키가 없으면 끝까지 추출
#                 pattern = re.escape(matched_keyword) + r"\s*([\S\s]+?)$"
            
#             match = re.search(pattern, extracted_text)
#             if match:
#                 # 추출된 값을 result에 저장
#                 result[key] = match.group(1).strip()
#                 # 추출한 텍스트에서 이미 추출한 데이터 삭제
#                 extracted_text = extracted_text.replace(match.group(0), "").strip()
#             else:
#                 # 값이 추출되지 않으면 unmatched_keys에 추가
#                 unmatched_keys.append(key)
#         else:
#             # 유사한 키워드를 찾지 못한 경우 unmatched_keys에 추가
#             unmatched_keys.append(key)
    
#     # 6. 두 번째 방법: 첫 번째 방법에서 값을 찾지 못한 키들에 대해 연속적인 문자열 매칭
#     if unmatched_keys:
#         result = sequential_string_matching(unmatched_keys, extracted_text, result)
    
#     return result


# # 두 번째 함수 (연속적인 문자열로 키를 찾는 함수)
# def sequential_string_matching(json_keys, extracted_text, result):
#     # 1. 공백을 모두 제거하여 하나의 연속된 문자열로 변환
#     extracted_text = re.sub(r'\s+', '', extracted_text).strip()
    
#     # 2. 문자열 내에서 키워드를 순차적으로 탐색
#     for i, key in enumerate(json_keys):
#         # 키워드도 공백을 제거하여 검색할 수 있도록 정리
#         cleaned_key = re.sub(r'\s+', '', key).strip()
        
#         # 3. 현재 키워드를 텍스트에서 검색
#         key_start = extracted_text.find(cleaned_key)
        
#         if key_start != -1:
#             # 4. 현재 키의 끝 위치를 구함 (찾은 위치 + 키의 길이)
#             key_end = key_start + len(cleaned_key)

#             # 5. 다음 키워드를 찾음
#             next_key_match = None
#             for next_key in json_keys[i+1:]:
#                 cleaned_next_key = re.sub(r'\s+', '', next_key).strip()
#                 next_key_start = extracted_text.find(cleaned_next_key, key_end)
                
#                 if next_key_start != -1:
#                     next_key_match = (cleaned_next_key, next_key_start)
#                     break  # 가장 가까운 다음 키를 찾으면 중단

#             # 6. 다음 키워드를 찾은 경우 그 사이의 텍스트를 값으로 추출
#             if next_key_match:
#                 next_key, next_key_start = next_key_match
#                 result[key] = extracted_text[key_end:next_key_start].strip()
#             else:
#                 # 다음 키워드를 못 찾으면 해당 키 뒤의 모든 텍스트를 값으로 저장
#                 result[key] = extracted_text[key_end:].strip()

#             # 7. 처리한 부분을 제거하여 텍스트 업데이트
#             extracted_text = extracted_text[:key_start] + extracted_text[key_end:]
#         else:
#             # 키워드를 찾지 못한 경우 비워둠
#             result[key] = ""

#     return result




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


def main():
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
    
    # 초기 데이터    
    parsed_data = extract_and_match_keys(json_keys, extracted_text, cutoff=0.7)
    #print(f"초기 추출된 데이터: {json.dumps(parsed_data, ensure_ascii=False, indent=4)}")

    print("실제 데이터와(검증을 위해 직접 입력한 데이터)와 Raw 사진에서 추출한 텍스트 데이터 비교 분석 결과 ")
    raw_image_results = calculate_metrics(text_data, parsed_data, json_keys,keys_weights, 0.7)
    
    # 누락된 데이터가 있는 경우 이미지 회전 후 재시도
    rotated_data = image_process_rotate(json_keys, file_path, parsed_data)
    #print(f"회전 후 추출된 데이터: {json.dumps(rotated_data, ensure_ascii=False, indent=4)}")

    print("실제 데이터와 이미지 회전을 통한 데이터 비교 분석 결과")
    rotated_image_results = calculate_metrics(text_data, rotated_data, json_keys,keys_weights, 0.7)

    # 퍼포먼스 상향 정도 확인
    performance_improvement(raw_image_results, rotated_image_results)

    # # CSV 파일에 데이터 저장
    # write_to_csv(rotated_data, CSV_FILE)
    # print(f"데이터가 {CSV_FILE}에 저장되었습니다.")


    # # 누락된 데이터가 있는 경우 이미지에서 객체를 탐지하여 해당 부분을 오려낸 후 재시도 //이부분 수정할 것
    # objected_data = image_process_with_object_detection(json_keys, file_path, parsed_data)
    # #print(f"객체 탐지 후 추출된 데이터: {json.dumps(objected_data, ensure_ascii=False, indent=4)}")

    # print("실제 데이터와 객체 탐지를 진행한 후 데이터 비교 분석 결과")
    # objected_image_results = calculate_metrics(text_data, objected_data, json_keys,keys_weights, 0.7)

    # # 퍼포먼스 상향 정도 확인
    # performance_improvement(raw_image_results, objected_image_results)

    # # CSV 파일에 데이터 저장
    # write_to_csv(objected_data, CSV_FILE)
    # print(f"데이터가 {CSV_FILE}에 저장되었습니다.")




if __name__ == "__main__":
    main()
