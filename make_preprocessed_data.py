import cv2
import numpy as np
import os
from makefilename import save_image_with_modified_filename

# 가로로 가장 긴 윤곽선과 세로로 가장 긴 윤곽선을 찾아 사각형을 만드는 함수
def crop_to_document(image,image_path):
    # 이미지를 그레이스케일로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imwrite('data/preprocessed/step1_gray.jpg', gray)  # Step 1: 그레이스케일 이미지 저장
    save_image_with_modified_filename(image_path, gray,"_gray")

    # 엣지 검출 (Canny 사용)
    edged = cv2.Canny(gray, 50, 150)
    #cv2.imwrite('data/preprocessed/step2_edged.jpg', edged)  # Step 2: 엣지 검출된 이미지 저장
    save_image_with_modified_filename(image_path, edged,"_edged")

    # 윤곽선 검출
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 가로로 가장 긴 윤곽선, 세로로 가장 긴 윤곽선 초기화
    longest_horizontal = None
    longest_vertical = None
    max_width = 0
    max_height = 0

    for contour in contours:
        # 윤곽선의 경계 상자를 계산
        x, y, w, h = cv2.boundingRect(contour)

        # 가로로 가장 긴 윤곽선 찾기
        if w > max_width:
            max_width = w
            longest_horizontal = (x, y, w, h)

        # 세로로 가장 긴 윤곽선 찾기
        if h > max_height:
            max_height = h
            longest_vertical = (x, y, w, h)

    print("윤곽선: ", longest_horizontal, longest_vertical);

    if longest_horizontal is not None and longest_vertical is not None:
        # 각 윤곽선의 좌표를 사용하여 사각형 만들기
        x1, y1, w1, h1 = longest_horizontal
        x2, y2, w2, h2 = longest_vertical

        # 가로로 긴 윤곽선과 세로로 긴 윤곽선의 범위를 합쳐서 사각형 좌표 만들기
        x_start = min(x1, x2)
        y_start = min(y1, y2)
        x_end = max(x1 + w1, x2 + w2)
        y_end = max(y1 + h1, y2 + h2)

        # 이미지를 해당 사각형 범위로 자르기
        cropped_image = image[y_start:y_end, x_start:x_end]
        
        # 결과 이미지 저장 및 출력
        cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (0, 255, 0), 3)
        #cv2.imwrite('data/preprocessed/step3_draw_rectangle.jpg', image)  # Step 3: 사각형 그린 이미지 저장
        save_image_with_modified_filename(image_path, image,"_draw_rectangle")

        print("가장 긴 가로와 세로 윤곽선을 사용한 사각형 찾음")
        return cropped_image
    else:
        print("적절한 윤곽선 없음")
        return image  # 윤곽선을 찾지 못하면 원본 이미지 반환

# 이미지 읽기
image_path = 'data/src/2.jpg'
image = cv2.imread(image_path)

# 이미지 자르기
cropped_image = crop_to_document(image,image_path)

# 최종 결과 저장
save_image_with_modified_filename(image_path, cropped_image,"_cropped")

# output_path = 'data/preprocessed/step4_cropped_image.jpg'
# cv2.imwrite(output_path, cropped_image)

# print(f"최종 이미지 저장 경로: {output_path}")
