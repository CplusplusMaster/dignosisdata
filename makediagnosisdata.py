
import random

# 데이터 리스트 정의
owners = ["홍길동", "김영수", "박지현", "이민호", "정수연", "최준호", "김혜리", "한지원", "조윤희", "이수민"]
addresses = ["서울특별시 중구", "서울특별시 강남구", "경기도 수원시", "부산광역시 해운대구", "대구광역시 수성구"]
animals = ["강아지", "고양이"]
breeds_dogs = ["말티즈", "푸들", "비숑프리제", "시츄", "골든리트리버"]
breeds_cats = ["러시안블루", "페르시안", "샴", "스코티쉬폴드"]
colors = ["흰색", "검정색", "갈색", "회색", "황색"]
unique_traits = ["이빨 하나 없음", "꼬리 끝 흰색", "앞다리 절음", "왼쪽 귀 실명", "눈 색깔이 다름", "털 빠짐 심함"]
hospitals = ["행복 동물병원", "희망 동물병원", "건강한 동물병원", "웰빙 동물병원", "사랑 동물병원"]
vet_names = ["민수의", "김수의", "이수의", "박수의", "최수의"]

# 병명, 증상, 치료 간 관계 설정
disease_data = {
    "감기": {
        "증상": ["기침", "콧물", "열"],
        "치료": ["항생제 투여", "감기약 처방"]
    },
    "피부염": {
        "증상": ["가려움", "발진", "붉은 반점"],
        "치료": ["항생제 연고", "알러지 약물"]
    },
    "결막염": {
        "증상": ["눈 붓기", "눈물", "충혈"],
        "치료": ["안약 투여", "소염제"]
    },
    "장염": {
        "증상": ["설사", "구토", "복통"],
        "치료": ["수액 치료", "항생제 투여"]
    },
    "구내염": {
        "증상": ["입 냄새", "침 흘림", "잇몸 출혈"],
        "치료": ["구강 청소", "약물 투여"]
    },
    "알러지": {
        "증상": ["가려움", "발진", "붓기"],
        "치료": ["알러지 약물", "항히스타민제"]
    }
}

# 무작위 데이터 생성 함수
def generate_data():
    animal_type = random.choice(animals)
    breed = random.choice(breeds_dogs if animal_type == "강아지" else breeds_cats)
    disease = random.choice(list(disease_data.keys()))
    symptoms = ", ".join(random.sample(disease_data[disease]["증상"], 2))
    treatment = random.choice(disease_data[disease]["치료"])
    
    return {
        "동물 소유자": random.choice(owners),
        "주소": random.choice(addresses),
        "사육장소": f"{random.choice(addresses)} 사육장",
        "종류": animal_type,
        "품종": breed,
        "동물명": random.choice(["누리", "초코", "보리", "코코", "솜이", "미미", "뭉치", "하늘"]),
        "성별": random.choice(["암컷", "수컷"]),
        "연령": f"{random.randint(1, 10)}세",
        "모색": random.choice(colors),
        "특징": random.choice(unique_traits),
        "병명": disease,
        "발병 연월일": f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
        "진단 연월일": f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
        "주요 증상": symptoms,
        "치료명칭": treatment,
        "입원*퇴원일": f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d} ~ 2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
        "예후 소견": random.choice(["호전 중", "회복 중", "안정적", "증상 완화"]),
        "그 밖의 사항": "특이 사항 없음",
        "년": "2024",
        "월": f"{random.randint(1, 12):02d}",
        "일": f"{random.randint(1, 28):02d}",
        "동물병원 명칭": random.choice(hospitals),
        "동물병원 주소": random.choice(addresses),
        "전화번호": f"010-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
        "면허번호": f"2018{random.randint(100000, 999999)}",
        "수의사 성명": random.choice(vet_names)
    }

# 100개의 데이터 생성
data_list = [generate_data() for _ in range(100)]

# 출력 또는 저장
for idx, data in enumerate(data_list, 1):
    print(f"데이터 {idx}: {data}")



import json

# data_list를 JSON 파일로 저장
with open("data_list.json", "w", encoding="utf-8") as f:
    json.dump(data_list, f, ensure_ascii=False, indent=4)

print("100개의 데이터가 'data_list.json' 파일로 저장되었습니다.")
