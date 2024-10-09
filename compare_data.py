import pandas as pd
import json

# CSV 파일 읽기
csv_file_path = 'extracted_data.csv'
csv_data = pd.read_csv(csv_file_path)

# JSON 파일 읽기
json_file_path = 'src_data.json'
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

# 데이터 비교를 위한 함수
def compare_data(csv_row, json_data):
    for key, value in json_data.items():
        # CSV의 해당 열 이름과 JSON의 키 비교
        if key in csv_row and csv_row[key] != value:
            print(f"Mismatch found: {key} (CSV: {csv_row[key]}, JSON: {value})")

# CSV 데이터와 JSON 데이터 비교
for index, row in csv_data.iterrows():
    compare_data(row, json_data)
