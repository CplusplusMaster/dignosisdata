# # import cv2
# # import numpy as np
# # import matplotlib.pyplot as plt
# # from scipy.ndimage import rotate

# # # 이미지 회전 함수 (중심 기준으로 지정된 각도만큼 회전)
# # def rotate_image(image, angle):
# #     (h, w) = image.shape[:2]
# #     center = (w // 2, h // 2)
# #     rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
# #     rotated = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
# #     return rotated

# # # 1. 이미지 읽기
# # image_path = "data/src/rotate_data1.jpg"  # 예시 이미지 경로 (업로드된 이미지 사용)
# # image = cv2.imread(image_path)



# # # 여기에 find_line_and_calculate_angle

# # angle = 


# # # 4. 이미지 회전 (필요시 회전 각도를 변경 가능)
# # rotated_image = rotate_image(image, angle)  # 회전 각도는 테스트 후 필요에 따라 조절

# # # 6. 최종 이미지 저장
# # output_path = "enhanced_image.jpg"
# # cv2.imwrite(output_path, rotated_image)

# # # 7. 최종 결과 시각화
# # plt.figure(figsize=(10, 10))
# # plt.subplot(1, 3, 1)
# # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
# # plt.title("Original Image")
# # plt.axis("off")

# # plt.subplot(1, 3, 3)
# # plt.imshow(rotated_image, cmap='gray')
# # plt.title("Enhanced & Rotated Image")
# # plt.axis("off")

# # plt.show()

# # print(f"최종 이미지가 저장되었습니다: {output_path}")

# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# from find_line_and_calculate_angle import find_average_angle  # 모듈에서 함수 가져오기

# # 이미지 회전 함수 (중심 기준으로 지정된 각도만큼 회전)
# def rotate_image(image, angle):
#     (h, w) = image.shape[:2]
#     center = (w // 2, h // 2)
#     rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
#     rotated = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
#     return rotated

# # 1. 이미지 읽기
# image_path = "data/src/rotate_data1.jpg"  # 예시 이미지 경로
# image = cv2.imread(image_path)

# # 2. 각도 계산 함수 호출
# angle = find_average_angle(image_path)

# # 4. 이미지 회전 (필요시 회전 각도를 변경 가능)
# rotated_image = rotate_image(image, angle)  # 회전 각도는 계산된 각도를 사용

# # 6. 최종 이미지 저장
# output_path = "enhanced_image.jpg"
# cv2.imwrite(output_path, rotated_image)

# # # 7. 최종 결과 시각화
# # plt.figure(figsize=(10, 10))
# # plt.subplot(1, 3, 1)
# # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
# # plt.title("Original Image")
# # plt.axis("off")

# # plt.subplot(1, 3, 3)
# # plt.imshow(rotated_image, cmap='gray')
# # plt.title("Enhanced & Rotated Image")
# # plt.axis("off")

# # plt.show()

# # print(f"최종 이미지가 저장되었습니다: {output_path}")
import cv2
import numpy as np
from find_line_and_calculate_angle import find_average_angle  # 각도 계산 함수 가져오기

# 이미지 회전 함수 (중심 기준으로 지정된 각도만큼 회전)
def rotate_image(image, angle):
    """
    주어진 이미지와 각도를 사용하여 이미지를 회전합니다.
    
    :param image: 회전할 이미지 (OpenCV 형식)
    :param angle: 회전할 각도
    :return: 회전된 이미지
    """
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

# 각도를 계산하고 이미지를 회전하는 함수
def rotate_image_by_detected_angle(image_path):
    """
    주어진 이미지 경로에서 선의 각도를 계산한 후 이미지 회전을 수행합니다.
    
    :param image_path: 이미지 파일 경로
    :return: 회전된 이미지와 계산된 각도
    """
    # 이미지 읽기
    image = cv2.imread(image_path)

    # 각도 계산
    angle = find_average_angle(image_path)

    # 이미지 회전
    rotated_image = rotate_image(image, angle)

        # 6. 최종 이미지 저장
    output_path = "enhanced_image.jpg"
    cv2.imwrite(output_path, rotated_image)

    print(f"최종 이미지가 저장되었습니다: {output_path}")
    return rotated_image, angle
