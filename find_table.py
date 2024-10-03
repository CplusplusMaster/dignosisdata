
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt


def preprocess_image(image_path, blur_kernel=(5, 5), canny_threshold1=50, canny_threshold2=150):
    """
    이미지를 읽고 전처리 (그레이스케일 변환, 가우시안 블러링, 엣지 검출)
    
    :param image_path: 입력 이미지 경로
    :param blur_kernel: 가우시안 블러 커널 크기
    :param canny_threshold1: Canny 엣지 검출의 첫 번째 임계값
    :param canny_threshold2: Canny 엣지 검출의 두 번째 임계값
    :return: 원본 이미지, 그레이스케일 이미지, 엣지 이미지
    """
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, blur_kernel, 0)
    edges = cv2.Canny(blurred, canny_threshold1, canny_threshold2)
    return image, gray, edges


def extract_objects(image, edges, min_width=400, min_height=30, output_dir="extracted_objects"):
    """
    윤곽선을 검출하여 각 객체를 분리하고 이미지를 저장합니다.
    
    :param image: 원본 이미지
    :param edges: 엣지 이미지
    :param min_width: 최소 객체 너비 (너무 작은 사물 제외)
    :param min_height: 최소 객체 높이 (너무 작은 사물 제외)
    :param output_dir: 추출된 객체 이미지를 저장할 디렉토리 경로
    :return: 경계 상자가 그려진 이미지, 분리된 객체 수
    """
    # 윤곽선 검출
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 결과 저장을 위한 디렉토리 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    object_count = 0
    for contour in contours:
        # 윤곽선의 경계 상자 구하기
        x, y, w, h = cv2.boundingRect(contour)

        # 너무 작은 사물은 제외
        if w < min_width or h < min_height:
            continue

        # 사물의 영역을 자르기
        object_image = image[y:y+h, x:x+w]

        # 분리된 사물 이미지를 파일로 저장
        object_path = os.path.join(output_dir, f"object_{object_count}.jpg")
        cv2.imwrite(object_path, object_image)

        # 원본 이미지에 경계 상자 그리기
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        object_count += 1

    return image, object_count


def display_image(image, title="Image with Detected Objects"):
    """
    이미지를 matplotlib을 이용하여 표시
    
    :param image: 표시할 이미지
    :param title: 이미지 제목
    """
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis("off")
    plt.show()


def detect_table(image_path, output_dir="extracted_objects", blur_kernel=(5, 5), canny_threshold1=50, canny_threshold2=150, min_width=400, min_height=30):
    """
    객체 추출 파이프라인을 실행합니다.
    
    :param image_path: 분석할 이미지 경로
    :param output_dir: 추출된 객체 이미지를 저장할 디렉토리 경로
    :param blur_kernel: 가우시안 블러 커널 크기
    :param canny_threshold1: Canny 엣지 검출의 첫 번째 임계값
    :param canny_threshold2: Canny 엣지 검출의 두 번째 임계값
    :param min_width: 최소 객체 너비 (너무 작은 사물 제외)
    :param min_height: 최소 객체 높이 (너무 작은 사물 제외)
    """
    # 1. 이미지 전처리
    image, gray, edges = preprocess_image(image_path, blur_kernel, canny_threshold1, canny_threshold2)

    # 2. 객체 추출 및 이미지 분리
    processed_image, object_count = extract_objects(image, edges, min_width, min_height, output_dir)

    # 3. 결과 이미지 표시
#    display_image(processed_image, title="Detected Objects with Bounding Boxes")
    
    # 4. 결과 출력
#    print(f"{object_count} 개의 사물이 분리되었습니다. 각 사물 이미지는 '{output_dir}' 폴더에 저장되었습니다.")


if __name__ == "__main__":
    # 사용자 지정 입력 파일 경로
    image_path = "data/src/object_data1.jpg"
    detect_table(image_path)
