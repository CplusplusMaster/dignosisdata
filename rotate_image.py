import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import rotate

# # 이미지 선명도를 높이는 함수 (가우시안 블러 사용)
# def increase_sharpness(image):
#     blurred = cv2.GaussianBlur(image, (0, 0), 3)
#     sharp = cv2.addWeighted(image, 1.5, blurred, -0.5, 0)
#     return sharp

# 이미지 회전 함수 (중심 기준으로 지정된 각도만큼 회전)
def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

# 1. 이미지 읽기
image_path = "data/src/rotate1.jpg"  # 예시 이미지 경로 (업로드된 이미지 사용)
image = cv2.imread(image_path)

# # 2. 이미지를 그레이스케일로 변환
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # 3. 이미지 선명도 향상 (샤프닝)
# sharp_image = increase_sharpness(gray)

# 4. 이미지 회전 (필요시 회전 각도를 변경 가능)
rotated_image = rotate_image(image, angle=-12)  # 회전 각도는 테스트 후 필요에 따라 조절

# 5. 선명도 및 대비 조정
# 히스토그램 평활화를 통한 대비 향상
#enhanced_image = cv2.equalizeHist(rotated_image)

# 6. 최종 이미지 저장
output_path = "enhanced_image.jpg"
cv2.imwrite(output_path, rotated_image)

# 7. 최종 결과 시각화
plt.figure(figsize=(10, 10))
plt.subplot(1, 3, 1)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(rotated_image, cmap='gray')
plt.title("Enhanced & Rotated Image")
plt.axis("off")

plt.show()

print(f"최종 이미지가 저장되었습니다: {output_path}")