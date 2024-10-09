from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from difflib import SequenceMatcher

# 유사도 계산 함수
def similarity_score(actual, extracted):
    return SequenceMatcher(None, actual, extracted).ratio()

def calculate_metrics(original_data, extracted_data, key_list, weight_dict, similarity_threshold=0.7):
    """
    원본 데이터와 추출된 결과를 비교하여 정확도, 정밀도, 재현율, F1 스코어를 계산하는 함수.
    각 필드에 가중치를 적용하여 평가 점수를 계산.

    Parameters:
    - original_data: dict, 원본 데이터
    - extracted_data: dict, 추출된 데이터
    - key_list: list, 비교할 필드의 키 목록
    - weight_dict: dict, 각 필드별 가중치 (예: {"성명": 2, "병명": 2, "주소": 1})
    - similarity_threshold: float, 유사도 임계값 (기본값 0.7)

    Returns:
    - 정확도, 정밀도, 재현율, F1 스코어 (가중치가 적용된 결과)
    """
    # 1. 키 목록을 정의 (고정된 키 값)
    keys = key_list

    # 2. TP, FP, TN, FN을 위한 리스트 초기화
    y_true = []  # 원본 데이터의 값 (정답)
    y_pred = []  # 추출된 결과 값 (예측)
    y_sim = []   # 유사도 기반 분석 값
    weights = [] # 각 필드에 해당하는 가중치 목록

    # 3. 각 키에 대해 원본 데이터와 추출된 결과를 비교하여 매칭 여부 확인
    for key in keys:
        # 4. 키가 존재하는지 확인하고 원본 데이터와 추출된 데이터의 값을 가져옴
        original_value = original_data.get(key, "").strip() if original_data.get(key) else ""
        extracted_value = extracted_data.get(key, "").strip() if extracted_data.get(key) else ""

        # 5. 해당 필드의 가중치를 가져옴 (기본값 1)
        weight = weight_dict.get(key, 1)
        weights.append(weight)

        # 6. 정답과 예측값 설정
        y_true.append(1 if original_value else 0)  # 원본에 값이 있으면 1, 없으면 0
        y_pred.append(1 if extracted_value == original_value and original_value else 0)  # 값이 일치하면 1, 아니면 0

        # 7. 유사도 점수 계산 (original_value와 extracted_value 비교)
        similarity = similarity_score(original_value, extracted_value)

        # 8. 유사도 점수가 일정 기준 이상일 경우 일치로 간주
        y_sim.append(1 if similarity >= similarity_threshold and original_value else 0)

    # 9. 정확도, 정밀도, 재현율, F1 스코어 계산 (가중치 적용)
    weighted_accuracy = sum(w * (t == p) for w, t, p in zip(weights, y_true, y_pred)) / sum(weights)
    weighted_precision = sum(w * (t & p) for w, t, p in zip(weights, y_true, y_pred)) / (sum(w * p for w, p in zip(weights, y_pred)) + 1e-10)
    weighted_recall = sum(w * (t & p) for w, t, p in zip(weights, y_true, y_pred)) / (sum(w * t for w, t in zip(weights, y_true)) + 1e-10)
    weighted_f1 = 2 * (weighted_precision * weighted_recall) / (weighted_precision + weighted_recall + 1e-10)

    # 10. 유사도 기반 지표 계산 (가중치 적용)
    weighted_sim_accuracy = sum(w * (t == s) for w, t, s in zip(weights, y_true, y_sim)) / sum(weights)
    weighted_sim_precision = sum(w * (t & s) for w, t, s in zip(weights, y_true, y_sim)) / (sum(w * s for w, s in zip(weights, y_sim)) + 1e-10)
    weighted_sim_recall = sum(w * (t & s) for w, t, s in zip(weights, y_true, y_sim)) / (sum(w * t for w, t in zip(weights, y_true)) + 1e-10)
    weighted_sim_f1 = 2 * (weighted_sim_precision * weighted_sim_recall) / (weighted_sim_precision + weighted_sim_recall + 1e-10)

    # 결과 출력
    print(f"정확도(Weighted Accuracy): {weighted_accuracy:.4f}")
    print(f"정밀도(Weighted Precision): {weighted_precision:.4f}")
    print(f"재현율(Weighted Recall): {weighted_recall:.4f}")
    print(f"F1 스코어(Weighted F1 Score): {weighted_f1:.4f}")

    # 유사도 기반 결과 출력
    print("\n유사도 기반 평가 지표 (가중치 적용)")
    print(f"유사도 기반 정확도(Weighted Similarity Accuracy): {weighted_sim_accuracy:.4f}")
    print(f"유사도 기반 정밀도(Weighted Similarity Precision): {weighted_sim_precision:.4f}")
    print(f"유사도 기반 재현율(Weighted Similarity Recall): {weighted_sim_recall:.4f}")
    print(f"유사도 기반 F1 스코어(Weighted Similarity F1 Score): {weighted_sim_f1:.4f}")
    
    return weighted_accuracy, weighted_precision, weighted_recall, weighted_f1, weighted_sim_accuracy, weighted_sim_precision, weighted_sim_recall, weighted_sim_f1


def performance_improvement(before, after):
    print("\n=== 성능 변화 비교 ===")
    metrics = ["정확도", "정밀도", "재현율", "F1 스코어", "유사도 기반 정확도", "유사도 기반 정밀도", "유사도 기반 재현율", "유사도 기반 F1 스코어"]
    for i, metric in enumerate(metrics):
        original_value = before[i]
        modified_value = after[i]
        improvement = modified_value - original_value
        print(f"{metric}: {original_value:.4f} -> {modified_value:.4f} (변화: {improvement:+.4f})")
