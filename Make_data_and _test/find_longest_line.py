import cv2
import numpy as np
import os
from makefilename import save_image_with_modified_filename


# 이미지를 입력받아 가장 긴 가로선과 세로선을 찾는 함수
def detect_longest_lines(image):
    # 이미지를 그레이스케일로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Gaussian 블러를 적용하여 노이즈 제거
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Canny 엣지 검출
    edges = cv2.Canny(blurred, 50, 150)

    # Hough Line Transform을 사용하여 선 검출
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    # 가장 긴 가로선과 세로선 초기화
    longest_horizontal = None
    longest_vertical = None
    max_horizontal_len = 0
    max_vertical_len = 0

    # 검출된 선들 중에서 가장 긴 가로선과 세로선 찾기
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

            # 가로선: y좌표가 거의 같을 경우
            if abs(y2 - y1) < 10 and length > max_horizontal_len:
                max_horizontal_len = length
                longest_horizontal = (x1, y1, x2, y2)

            # 세로선: x좌표가 거의 같을 경우
            elif abs(x2 - x1) < 10 and length > max_vertical_len:
                max_vertical_len = length
                longest_vertical = (x1, y1, x2, y2)

    # 원본 이미지에 가장 긴 선 그리기
    if longest_horizontal:
        cv2.line(image, (longest_horizontal[0], longest_horizontal[1]), (longest_horizontal[2], longest_horizontal[3]), (0, 255, 0), 3)
    if longest_vertical:
        cv2.line(image, (longest_vertical[0], longest_vertical[1]), (longest_vertical[2], longest_vertical[3]), (255, 0, 0), 3)

    return image

import cv2
import os

image_path = 'base_data.jpg'

# 이미지 불러오기
image = cv2.imread(image_path)

# 가정: detect_longest_lines 함수는 긴 가로선과 세로선을 검출하는 처리된 이미지를 반환
result_image = detect_longest_lines(image)

# 파일 저장 함수 호출
save_image_with_modified_filename(image_path, result_image,"_longest_line")

