import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.dates import DateFormatter

sns.set_theme(style="dark")  # Seaborn 스타일 설정

# 예제 데이터
data = {
    'date': ['2024-12-01', '2024-12-02', '2024-12-03', '2024-12-04', '2024-12-05', '2024-12-06', '2024-12-07', 
             '2024-12-08', '2024-12-09', '2024-12-10', '2024-12-11', '2024-12-12', '2024-12-13', '2024-12-14',
             '2024-12-15', '2024-12-16', '2024-12-17', '2024-12-18', '2024-12-19', '2024-12-20', '2024-12-21',
             '2024-12-22', '2024-12-23', '2024-12-24', '2024-12-25', '2024-12-26', '2024-12-27', '2024-12-28'
             ],
    'votes': [55, 60, 57, 62, 59, 65, 63, 70, 60, 57, 62, 52, 65, 68, 54, 60, 57, 62, 59, 65, 63, 50, 60, 57, 62, 42, 45, 53]
}

# 리스트를 DataFrame으로 변환
data = pd.DataFrame(data)

# 'date' 컬럼을 datetime 타입으로 변환
data['date'] = pd.to_datetime(data['date'])

# 매주(7일 간격) 데이터, 마지막 데이터 추출
selected_data = data.iloc[list(range(0, len(data), 7)) + [len(data) - 1]]

# 그래프 크기 조정
plt.figure(figsize=(8, 5))

# 데이터 그래프
plt.plot(selected_data['date'], selected_data['votes'], color='black', marker='o', markersize=8, label='Popularity')

# y축 범위를 0에서 100으로 설정
plt.ylim(0, 100)

# x축 눈금을 마커 위치에 해당하는 날짜로 설정
plt.gca().set_xticks(selected_data['date'])  # 마커 위치의 날짜만 눈금으로 설정
plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))  # 날짜 포맷 설정

# x, Y축 폰트 크기
plt.xticks(fontsize=8, fontweight='bold')
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