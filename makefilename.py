import cv2
import os

def save_image_with_modified_filename(image_path, result_image, prefix, output_dir='data/preprocessed'):
    """
    주어진 이미지 경로에서 원본 파일명 앞에 prefix를 붙여 새로운 이미지를 저장하는 함수.

    :param image_path: 원본 이미지 파일 경로
    :param result_image: 처리된 이미지 (저장할 이미지)
    :param prefix: 파일명 앞에 붙일 접두사 
    :param output_dir: 이미지를 저장할 디렉토리 경로 (기본값은 'data/preprocessed')
    """
    # 파일 경로에서 디렉토리, 파일명, 확장자를 분리
    directory, filename = os.path.split(image_path)
    file_base, file_extension = os.path.splitext(filename)

    # 새 파일명 생성 (원본 파일명 앞에 접두사 추가)
    new_filename = f"{file_base}{prefix}{file_extension}"

    # 새 저장 경로 설정
    output_path = os.path.join(output_dir, new_filename)

    # 출력 디렉토리가 없으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 결과 이미지 저장
    cv2.imwrite(output_path, result_image)
    print(f"이미지 저장 완료: {output_path}")