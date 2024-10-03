import cv2
import numpy as np
import math

def merge_similar_lines(lines, threshold=10):
    """
    비슷한 y값을 가지는 선분들을 하나의 선으로 합치는 함수
    :param lines: HoughLinesP로 검출된 선분들
    :param threshold: y값의 차이를 기준으로 비슷한 선분을 합침
    :return: 합쳐진 선분 리스트
    """
    if lines is None:
        return []

    merged_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]

        # 이미 존재하는 선들과 비교하여 합칠 수 있는지 확인
        merged = False
        for merged_line in merged_lines:
            mx1, my1, mx2, my2 = merged_line

            # y값이 비슷한지 비교
            if abs(y1 - my1) < threshold and abs(y2 - my2) < threshold:
                # 두 선분을 평균 값으로 합침
                new_line = [
                    (x1 + mx1) // 2, (y1 + my1) // 2,
                    (x2 + mx2) // 2, (y2 + my2) // 2
                ]
                merged_line[:] = new_line
                merged = True
                break
        
        # 새로운 선분 추가
        if not merged:
            merged_lines.append([x1, y1, x2, y2])
    
    return merged_lines

def calculate_angle(x1, y1, x2, y2):
    """
    두 점의 좌표를 사용하여 각도를 계산하는 함수
    :param x1, y1: 첫 번째 점의 좌표
    :param x2, y2: 두 번째 점의 좌표
    :return: 선의 각도 (도 단위)
    """
    # 수직선일 때의 각도 처리
    if x1 == x2:
        return 90.0

    # 기울기를 이용해 각도 계산 (라디안 단위 -> 도 단위 변환)
    angle_rad = math.atan2(y2 - y1, x2 - x1)
    angle_deg = math.degrees(angle_rad)
    
    # 각도를 양수로 조정
    if angle_deg < 0:
        angle_deg += 180
    
    return angle_deg


def main():
        
    # 이미지 읽기
    image_path = 'data/src/rotate_data1.jpg'  # 사용자가 제공한 이미지 경로
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 엣지 검출 (Canny 사용)
    edges = cv2.Canny(gray, 50, 150)

    # Hough Line Transform을 사용해 선 검출
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 180, threshold=200, minLineLength=700, maxLineGap=40)

    # 비슷한 선분 합치기
    merged_lines = merge_similar_lines(lines)

    # 결과를 이미지에 그리기 및 각도 계산
    print("검출된 선들의 각도:")

    sum = 0 
    line_counts = 0
    average = 0
    for line in merged_lines:
        x1, y1, x2, y2 = line
        # 선분을 이미지에 그림
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # 각도 계산
        angle = calculate_angle(x1, y1, x2, y2)
        print(f"({x1}, {y1}) -> ({x2}, {y2}): {angle:.2f}도")
        sum += angle - 180
        line_counts += 1

    # 기울어진 평균 각도 계산
    average = sum/line_counts
    print("average: ", int(average))

    return average

    # # 결과 이미지 저장
    # output_path = 'output_with_angles.jpg'
    # cv2.imwrite(output_path, image)

    # # 결과 출력
    # cv2.imshow("Result", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # print(f"최종 이미지 저장 경로: {output_path}")


if __name__ == "__main__":
    main()
