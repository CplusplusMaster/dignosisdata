import cv2
import numpy as np
import os
import matplotlib.pyplot as plt


# 1. 이미지 읽기
image_path = "data/src/object_data1.jpg"  # 분석할 이미지 경로
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 2. 이미지 전처리 (노이즈 제거 및 엣지 검출)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 150)

# 3. 윤곽선 검출
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 4. 각 객체의 경계 상자 추출 및 이미지 분리
output_dir = "extracted_objects"  # 추출된 객체 이미지를 저장할 디렉토리
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 5. 각 윤곽선에 대해 이미지 추출 및 저장
object_count = 0
for contour in contours:
    # 윤곽선의 경계 상자 구하기
    x, y, w, h = cv2.boundingRect(contour)
    
    # 너무 작은 사물은 제외 (필요 시 조건 조절)
    if w < 400 or h < 30:
        continue
    
    # 사물의 영역을 자르기
    object_image = image[y:y+h, x:x+w]
    
    # 분리된 사물 이미지를 파일로 저장
    object_path = os.path.join(output_dir, f"object_{object_count}.jpg")
    cv2.imwrite(object_path, object_image)
    
    # 원본 이미지에 경계 상자 그리기
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    object_count += 1

# 6. 결과 이미지와 추출된 사물들 표시
plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title("Detected Objects with Bounding Boxes")
plt.axis("off")
plt.show()

print(f"{object_count} 개의 사물이 분리되었습니다. 각 사물 이미지는 '{output_dir}' 폴더에 저장되었습니다.")

# # # 4. 가장 큰 객체 찾기
# # largest_contour = None
# # max_area = 0
# # for contour in contours:
# #     area = cv2.contourArea(contour)
# #     if area > max_area:  # 현재까지의 최대 면적보다 큰 윤곽선을 찾으면 업데이트
# #         max_area = area
# #         largest_contour = contour

# # # 5. 가장 큰 객체의 경계 상자 구하기
# # if largest_contour is not None:
# #     x, y, w, h = cv2.boundingRect(largest_contour)
# #     largest_object_image = image[y:y+h, x:x+w]  # 객체의 이미지를 자르기

# #     # 6. 분리된 객체 이미지 저장 및 표시
# #     output_path = "largest_object.jpg"
# #     cv2.imwrite(output_path, largest_object_image)

# #     print(f"가장 큰 객체가 저장되었습니다: {output_path}")

# #     # 7. 결과 이미지 출력
# #     plt.figure(figsize=(10, 10))
# #     plt.imshow(cv2.cvtColor(largest_object_image, cv2.COLOR_BGR2RGB))
# #     plt.title("Largest Object Extracted")
# #     plt.axis("off")
# #     plt.show()
# # else:
# #     print("윤곽선이 없습니다. 객체를 찾을 수 없습니다.")