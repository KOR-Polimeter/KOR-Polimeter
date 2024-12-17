import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.dates import DateFormatter

sns.set_theme(style="dark")  # Seaborn 스타일 설정

# Seaborn 스타일 설정
sns.set_theme(style="dark")

# 예제 데이터
data = pd.DataFrame({
    'date': ['2024-12-01', '2024-12-08', '2024-12-15', '2024-12-22'],
    'votes': [55, 60, 57, 62]
})

# 'date' 컬럼을 datetime 타입으로 변환
data['date'] = pd.to_datetime(data['date'])

# 그래프 크기 조정
plt.figure(figsize=(8, 5))

# 데이터 그래프
plt.plot(data['date'], data['votes'], color='black', marker='o', markersize=8, label='Popularity')

# y축 범위를 0에서 100으로 설정
plt.ylim(0, 100)

# 날짜 포맷 설정
plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

# x, y축 폰트 크기
plt.xticks(data['date'], fontsize=8, fontweight='bold')
plt.yticks(range(0, 101, 10), fontsize=10, fontweight='bold')

# 범례
plt.legend(loc='upper left', fontsize=10, frameon=True, fancybox=True, shadow=True)

# 그래프 여백 조정
plt.tight_layout()

# 현재 실행 중인 파일의 절대 경로 가져오기
current_dir = os.path.dirname(os.path.abspath(__file__))

img_name = 'chart.png'
img_path = os.path.join(current_dir, img_name)

# 그래프 저장 (dpi는 해상도)
plt.savefig(img_path, dpi=300)

plt.show()