# 1. 표준 라이브러리
import os
import sys
import urllib.request
import time
from collections import Counter

# 2. 외부 라이브러리
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from konlpy.tag import Okt
from wordcloud import WordCloud
import json

# 3. 로컬 라이브러리
from PIL import Image

# 발급받은 naver API id / secret
client_id = "********************"
client_secret = "***********"

quote = input("검색어를 입력해주세요.: ") # 검색어 입력받기
print("[INFO] 입력받은 검색어: {}".format(quote))
encText = urllib.parse.quote(quote)

display="50"  # 표시할 검색 결과 개수 설정
sort="sim"  # 관련성순
url = "https://openapi.naver.com/v1/search/news?query=" + encText + "&display="+ display + "&sort="+sort # JSON 결과
print("[INFO] 네이버 API 요청 URL 생성 완료.")

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()

if rescode == 200:
    response_body = response.read()
    body = response_body.decode('utf-8')
    print("[INFO] 네이버 API 요청 성공.")
    
    # JSON 데이터 파싱
    data = json.loads(body)
    total_results = data.get('total', 0)  # 'total' 키에서 값 가져오기
    print(f"[INFO] 총 검색 결과 개수: {total_results}")
else:
    print("[ERROR] 네이버 API 요청 실패. Error Code:", rescode)

# body 나누기
list1 = body.split('\n\t\t{\n\t\t\t')
print("[INFO] 검색 결과 JSON 데이터 분리 완료.")

# 제목, 링크 뽑기
import re
titles = []
links = []
for i in list1:
    title = re.findall('"title":"(.*?)",\n\t\t\t"originallink"', i)
    link = re.findall('"link":"(.*?)",\n\t\t\t"description"', i)
    titles.append(title)
    links.append(link)

# 2차원 리스트를 1차원으로 변환
titles = [r for i in titles for r in i]
links = [r for i in links for r in i]
print("[INFO] 뉴스 제목과 링크 추출 완료. 총 {}개 제목 수집.".format(len(titles)))

# 링크 다듬기 (필요없는 부분 제거 및 수정)
news_links = []
for i in links:
    a = i.replace('\\', '')
    b = a.replace('?Redirect=Log&logNo=', '/')
    news_links.append(b)
print("[INFO] 뉴스 링크 정리 완료.")

# 다양한 뉴스 본문 CSS 선택자 리스트
content_selectors = [
    'div.viewer',
    'div._article_content',
    'div.article_content',
    'div.news_contents',
    'div.cont_view',
    'div.article-body',
    'div.article_body',
    'div.arti-txt', 
    'div.art_body',
    'article.story-news',
    'div.article-view-content-div',
    'article'  # 가장 일반적인 article 태그
]

# 현재 실행 중인 파일의 절대 경로 가져오기
current_dir = os.path.dirname(os.path.abspath(__file__))

# chromedriver 경로 설정 
chromedriver_name = 'chromedriver.exe' 
chromedriver_path = os.path.join(current_dir, chromedriver_name)
service = Service(chromedriver_path) 

# WebDriver 초기화 
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 3)
print("[INFO] Selenium WebDriver 초기화 완료.")

# 뉴스 링크 하나씩 불러서 크롤링 
contents = [] 
for idx, i in enumerate(news_links): 
    print("\r[INFO] {}번째 뉴스 링크 크롤링 중...".format(idx + 1), end="")
    driver.get(i)  # 뉴스 링크 하나씩 불러오기 
    time.sleep(1) 

    # 다양한 선택자로 본문 찾기
    content = None
    for selector in content_selectors:
        try:
            content = driver.find_element(By.CSS_SELECTOR, selector).text
            if content and len(content.strip()) > 0:
                contents.append(content)
                break  # 성공적으로 본문을 찾았다면 반복 중단
        except NoSuchElementException:
            continue

    # 본문을 찾지 못한 경우 처리
    if not content:
        contents.append("")

print("[INFO] 뉴스 본문 크롤링 완료.")
driver.quit()  # 창닫기 

# 제목 및 본문 txt에 저장
total_contents = titles + contents
print("[INFO] 뉴스 제목 및 본문 저장 중...")
text = open("news_text.txt", 'w', encoding='utf-8') 
for i in total_contents:
    text.write(i)
text.close()
print("[INFO] 뉴스 제목 및 본문 저장 완료.")

# 제목, 블로그링크, 본문내용 Dataframe으로 만들기
df = pd.DataFrame({'제목': titles, '링크': news_links, '내용': contents})
print("[INFO] DataFrame 생성 완료.")

news_text = open('news_text.txt', 'rt', encoding='UTF-8').read()

# Okt 함수를 이용해 형태소 분석
okt = Okt()
print("[INFO] 형태소 분석 시작...")
line = []

line = okt.pos(news_text)

n_adj = []
# 명사 또는 형용사인 단어만 n_adj에 넣어주기
for word, tag in line:
    if tag in ['Noun', 'Adjective']:
        n_adj.append(word)

# 명사 또는 형용사만 필터링 + 불용어 제거 + 최소 길이 조건
stopwords = {'라며', '그리고', '그러나', '하지만', '에서', '에게', '중에', '위해', '조차', '까지', '어디', '무엇', '누구', '어느', '있다', '있는', '있습니다', '최근', '이번', '시간', '지난', '소식', '통해', '사진', '무단', '재', '및', '배포', '금지'}
n_adj = [word for word, tag in line if tag in ['Noun', 'Adjective'] and len(word) > 1 and word not in stopwords]

# 단어 빈도수 계산
word_count = Counter(n_adj)
print("[INFO] 단어 빈도수 계산 완료.")

# 상위 50개 단어 출력
tags = word_count.most_common(50)
print("[INFO] 상위 50개 단어 추출 완료.")

# 워드 클라우드 모양 이미지 경로 설정
img_name = 'cloud.png'
img_path = os.path.join(current_dir, img_name)

# 이미지 추가(워드클라우드 모양 설정) - cloud
mask = Image.new("RGBA", (500, 300), (255, 255, 255)) #(2555,2575)는 사진 크기, (255,255,255)는 색을의미
image = Image.open(img_path).convert("RGBA")
x, y = image.size
mask.paste(image, (0, 0, x, y), image)
mask = np.array(mask)

print("[INFO] 워드클라우드 생성 중...")

# font 경로 설정
font_name = 'NanumGothicBold.ttf'
font_path = os.path.join(current_dir, font_name)

wordcloud = WordCloud(
    font_path=font_path,  # 한글 폰트 파일 경로
    width=800, 
    height=400, 
    mask=mask,
    background_color='white'
).generate_from_frequencies(dict(tags))

# WordCloud 표시
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")  # 축 제거

# cloud 이미지 저장경로 설정
output_image_name = '{}_cloud.png'.format(quote)
output_image_path = os.path.join(current_dir, output_image_name)

# cloud 이미지 저장
plt.savefig(output_image_path, bbox_inches='tight')
print("[INFO] 워드클라우드 저장 완료. 파일 경로: {}".format(output_image_path))
plt.show()