
import re
import difflib
import json

# 추출한 텍스트에서 키와 매칭되는 값을 찾아 저장하는 함수
def extract_and_match_keys(json_keys, extracted_text, cutoff=0.8):
    """
    json_keys: 매칭할 키 목록 (예: ["동물 소유자", "주소", "사육장소"...])
    extracted_text: 사진에서 추출한 텍스트 데이터
    cutoff: 유사도 임계값, 기본 0.8
    """
    # 공백을 줄여주고 데이터 정리
    extracted_text = re.sub(r'\s+', ' ', extracted_text).strip()
    
    # 결과를 저장할 딕셔너리
    result = {key: "" for key in json_keys}
    
    # 각 키에 대해 텍스트에서 매칭되는 부분을 찾음
    for i, key in enumerate(json_keys):
        # 유사도 분석을 통해 추출된 텍스트에서 키워드와 유사한 단어를 찾음
        closest_match = difflib.get_close_matches(key, extracted_text.split(), n=1, cutoff=cutoff)
        
        if closest_match:
            matched_keyword = closest_match[0]
            # 매칭된 키워드 다음에 나오는 값을 추출
            # 다음 키가 나오기 전까지 범위를 설정 (다음 키는 현재 키의 뒤에 있는지 탐색)
            if i + 1 < len(json_keys):
                next_key = json_keys[i + 1]
                next_match = difflib.get_close_matches(next_key, extracted_text.split(), n=1, cutoff=cutoff)
                if next_match:
                    next_keyword = next_match[0]
                    pattern = re.escape(matched_keyword) + r"\s*([\S\s]+?)\s+" + re.escape(next_keyword)
                else:
                    pattern = re.escape(matched_keyword) + r"\s*([\S\s]+?)$"
            else:
                pattern = re.escape(matched_keyword) + r"\s*([\S\s]+?)$"
            
            match = re.search(pattern, extracted_text)
            
            if match:
                # 기존의 키 값들을 추가로 매칭하고 합쳐지는 것을 방지하기 위해 split으로 나누어 처리
                result[key] = match.group(1).strip()

                # 추출한 텍스트에서 이미 추출한 데이터 삭제
                #extracted_text = extracted_text.replace(match.group(0), "").strip()

    return result


# 예시로 사진에서 추출된 텍스트 데이터 
# 사진에서 텍스트가 100% 추출되었다고 가정한 데이터
extracted_text = "광역시 해운대구 해번로 456 사육잠소 부산광역시 해운대구 반려동물 센터 종류 고양이 품종 러시안 블루 동물명(동물등록번호) 미니 성별 암컷 동물의 표시 | 987654321090765) 연령 4세 00 오색 회색 특징 오른쪽 발에 흰 반점 있음 병명 임상적 주정 (7) 최종 진단 () 발병 연월일 ㅣ2024년 6월 15일 (임신 연월일) 진단 연월일 ㅣ2024년 9월 20일 주요 증상 기침, 호흡 곤란 치료명칭 항생제 처방 및 산소 요법 입원*퇴원일 2024년 9월 21일 ~ 2024년 9월 25일 예후  소견 상태 호전 중, 지속적인 경과 관찰 필요 그 밖의 사항 ＊ | 혈액 검사 결과 정상 [수의사법] 제 12조 및 같은 법 시행규칙 제 9조에 따라 위와 같이 중명합니다. 병명"란에는 “임상적 주정"과 최종진단" 중 택밀하여 [ ]에 + 표시를 하고, 질병명은 한글로 적되 명머로 적을 경우 에는 한글을 함께 적습니다. 영상 검사결과는 동물소유자가 다른 동물병원에서 진료를 받은 경우에 해당 동물병원의 개설자(수의샤)에게만 직접 제공할 목적으로 동물병원간 정보통신매 체로 전달할 수 있습니다. 2024년 '09월 14월 동물병원 명칭:부산동물병원 동물병원 주소: 부산광역시 해운대구 해운대로 789 (전화번호: 051-1234-5678)(전화번호 051-1234-5678) 수의사 면허번호: 제67890호 수의사 성명 민강현 (서명 또는 인)"

# JSON 파일 경로 (여기서 파일을 직접 읽지 않고 키 목록을 대입)
json_keys = ["동물 소유자 성명", "주소", "사육장소", "종류", "품종", "동물명(동물등록번호)", "성별", "연령", "모색", "특징", "병명", "발병 연월일", "진단 연월일", "주요 증상", "치료명칭", "입원*퇴원일", "예후 소견", "그 밖의 사항", "동물병원 명칭", "동물병원 주소", "전화번호", "면허번호", "수의사 성명"]

# 함수 실행 및 결과 확인
matched_data = extract_and_match_keys(json_keys, extracted_text, cutoff=0.7)

# 결과 출력
for key, value in matched_data.items():
    print(f"{key}: {value}")

