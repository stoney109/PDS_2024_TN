# version_1 파일 결과 입니다
# test_data_decision 파일과 sample_data_decision 파일
# test_data_decision - N / sample_data_decision - Y (종속변수 항목 확인)
import joblib
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier,plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)

# 파일 로드
file = '../../resource/decision_tree_preprocessed_data/merged_data/merged_data_version1.csv'  # CSV 파일 경로
df = pd.read_csv(file)

# 독립변수 종속변수 설정
independent_columns = ['final_견종', 'final_나이', 'final_체중', 'final_성별', 'final_중성화 여부']
dependent_column = 'final_입양여부'

X = df[independent_columns]
y = df[dependent_column]

# 종속변수 값 0, 1 라벨링
if y.dtypes == 'object':  # 종속변수가 문자열인 경우 숫자로 변환
    y = y.map({'N': 0, 'Y': 1})

# 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 모델 학습
# 최대 깊이 제한 (5로 제한)
model = DecisionTreeClassifier(max_depth=5,random_state=42)
model.fit(X_train, y_train)

# 예측
y_pred = model.predict(X_test)

# 성능 지표
# 혼동 행렬
conf_matrix = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = conf_matrix.ravel()

# Accuracy 정확도
accuracy = accuracy_score(y_test, y_pred)

# Precision 정밀도
precision = precision_score(y_test, y_pred, pos_label=1)

# Specificity - 특이도
specificity = tn / (tn + fp)

# Recall / Sensitivity - 민감도 / 재현율
sensitivity = recall_score(y_test, y_pred, pos_label=1)

# Error Rate - 오류율
error_rate = 1 - accuracy

# F1 Score
f1 = f1_score(y_test, y_pred, pos_label=1)

# 피처 중요도 추출
feature_importances = model.feature_importances_

# 피처 중요도를 데이터프레임으로 정리
importance_df = pd.DataFrame({
    'Feature': independent_columns,
    'Importance': feature_importances
}).sort_values(by='Importance', ascending=False)


# 결과 출력
print(f"Confusion Matrix:\n{conf_matrix}")
print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Specificity: {specificity:.2f}")
print(f"Recall / Sensitivity: {sensitivity:.2f}")
print(f"Error Rate: {error_rate:.2f}")
print(f"F1 Score: {f1:.2f}")
print("Feature Importances:")
print(importance_df)

# 모델 저장
model_filename = 'decision_tree1_model.pkl'
joblib.dump(model, model_filename)
print(f"Model saved as: {model_filename}")


# 시각화
matplotlib.rcParams['font.family'] = 'Malgun Gothic'  # 윈도우 한글 폰트 설정
matplotlib.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

plt.figure(figsize=(20, 10))  # 시각화 크기 설정
plot_tree(model,
          feature_names=independent_columns,
          class_names=['N', 'Y'],  # 클래스 이름 (종속변수 값)
          filled=True,
          rounded=True,
          fontsize=10)
plt.title("Decision Tree Visualization")
plt.savefig("decision_tree1.png", dpi=300, bbox_inches='tight')
plt.show()
