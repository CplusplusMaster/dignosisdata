from extract_data_from_diagnosis import *


def main():
    
    #테스트에 필요한 데이터 입력
    file_path, text_data, json_keys, keys_weights, extracted_text = input_data()

    # Raw Picture (촬영한 사진) 데이터    
    parsed_data = extract_and_match_keys(json_keys, extracted_text, cutoff=0.7)
    print(f"초기 추출된 데이터: {json.dumps(parsed_data, ensure_ascii=False, indent=4)}")

    print("실제 데이터와(검증을 위해 직접 입력한 데이터)와 Raw 사진에서 추출한 텍스트 데이터 비교 분석 결과 ")
    raw_image_results = calculate_metrics(text_data, parsed_data, json_keys,keys_weights, 0.7)
    
    # JSON 파일로 저장
    with open('parsed_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(parsed_data, json_file, ensure_ascii=False, indent=4)  # ensure_ascii=False로 한글 처리

    print("데이터가 parsed_data.json 파일로 저장되었습니다.")
    
    # 아래부분 삭제 절대 네버
    # # 누락된 데이터가 있는 경우 이미지 회전 후 재시도
    # rotated_data = image_process_rotate(json_keys, file_path, parsed_data)
    # #print(f"회전 후 추출된 데이터: {json.dumps(rotated_data, ensure_ascii=False, indent=4)}")

    # print("실제 데이터와 이미지 회전을 통한 데이터 비교 분석 결과")
    # rotated_image_results = calculate_metrics(text_data, rotated_data, json_keys,keys_weights, 0.7)

    # # 퍼포먼스 상향 정도 확인
    # performance_improvement(raw_image_results, rotated_image_results)

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
