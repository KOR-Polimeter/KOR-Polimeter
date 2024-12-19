# 1. 표준 라이브러리
import os
import time
import json
import urllib.request
from collections import Counter
import re

# 2. 외부 라이브러리
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from konlpy.tag import Okt
from wordcloud import WordCloud

# 3. 로컬 라이브러리
from PIL import Image

# 발급받은 naver API id / secret
client_id = "xYeaPBhyekbsWj9WtCq3"
client_secret = "YFZcqd9ZrQ"

# 검색할 이름 목록
names = '''
강경숙,강대식,강득구,강명구,강민국,강선영,강선우,강승규,강유정,강준현,강훈식,고동진,고민정,곽규택,곽상언,구자근,권성동,권영세,권영진,권칠승,권향엽,김건,김교흥,
김기웅,김기표,김기현,김남근,김남희,김대식,김도읍,김동아,김문수,김미애,김민석,김민전,김병기,김병주,김상욱,김상훈,김석기,김선교,김선민,김성원,김성환,김성회,김소희,
김승수,김승원,김영배,김영진,김영호,김영환,김예지,김용만,김용민,김용태,김우영,김원이,김위상,김윤,김윤덕,김은혜,김장겸,김재섭,김재원,김정재,김정호,김종민,김종양,
김주영,김준혁,김준형,김태년,김태선,김태호,김한규,김현,김현정,김형동,김희정,나경원,남인순,노종면,맹성규,모경종,문금주,문대림,문정복,문진석,민병덕,민형배,민홍철,
박균택,박대출,박덕흠,박민규,박범계,박상웅,박상혁,박선원,박성민,박성준,박성훈,박수민,박수영,박수현,박용갑,박은정,박정,박정하,박정현,박정훈,박주민,박준태,박지원,
박지혜,박찬대,박충권,박해철,박형수,박홍근,박홍배,박희승,배준영,배현진,백선희,백승아,백종헌,백혜련,복기왕,부승찬,서명옥,서미화,서범수,서삼석,서영교,서영석,서왕진,
서일준,서지영,서천호,성일종,소병훈,손명수,송기헌,송석준,송언석,송옥주,송재봉,신동욱,신성범,신영대,신장식,신정훈,안규백,안도걸,안상훈,안철수,안태준,안호영,양문석,
양부남,어기구,엄태영,염태영,오기형,오세희,용혜인,우원식,우재준,위성곤,위성락,유동수,유상범,유영하,유용원,윤건영,윤상현,윤영석,윤재옥,윤종군,윤종오,윤준병,윤한홍,
윤호중,윤후덕,이강일,이개호,이건태,이광희,이기헌,이달희,이만희,이병진,이상식,이상휘,이성권,이성윤,이소영,이수진,이양수,이언주,이연희,이용선,이용우,이원택,이인선,
이인영,이재강,이재관,이재명,이재정,이정문,이정헌,이종배,이종욱,이주영,이준석,이철규,이춘석,이학영,이해민,이해식,이헌승,이훈기,인요한,임광현,임미애,임오경,임이자,
임종득,임호선,장경태,장동혁,장종태,장철민,전용기,전재수,전종덕,전진숙,전현희,정동만,정동영,정성국,정성호,정연욱,정을호,정일영,정점식,정준호,정진욱,정청래,정춘생,
정태호,정혜경,정희용,조경태,조계원,조배숙,조승래,조승환,조은희,조인철,조정식,조정훈,조지연,주진우,주철현,주호영,진선미,진성준,진종오,차규근,차지호,채현일,천준호,
천하람,최기상,최민희,최보윤,최수진,최은석,최형두,추경호,추미애,한기호,한민수,한병도,한정애,한준호,한지아,한창민,허성무,허영,허종식,홍기원,황명선,황운하,황정아,황희
'''

# 이름 목록을 콤마로 분리하여 리스트로 변환
names = [name.strip() for name in names.split(',')]

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

# 크롬 드라이버 설정 (현재 실행 중인 파일의 절대 경로 가져오기)
current_dir = os.path.dirname(os.path.abspath(__file__))
chromedriver_name = 'chromedriver.exe' 
chromedriver_path = os.path.join(current_dir, chromedriver_name)
service = Service(chromedriver_path)

# WebDriver 초기화
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 3)
print("[INFO] Selenium WebDriver 초기화 완료.")

# 각 이름마다 워드 클라우드 생성
for name in names:
    if not name.strip():
        continue

    quote = name + " 의원"  # 의원 이름에 "의원" 추가
    print(f"[INFO] 검색어: {quote}")
    encText = urllib.parse.quote(quote)

    display = "20"  # 표시할 검색 결과 개수 설정
    sort = "sim"  # 관련성순
    url = f"https://openapi.naver.com/v1/search/news?query={encText}&display={display}&sort={sort}"  # JSON 결과
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
        continue  # 오류가 나면 다음 이름으로 넘어가기

    # body 나누기
    list1 = body.split('\n\t\t{\n\t\t\t')
    print("[INFO] 검색 결과 JSON 데이터 분리 완료.")

    # 제목, 링크 뽑기
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
    print(f"[INFO] 뉴스 제목과 링크 추출 완료. 총 {len(titles)}개 제목 수집.")

    # 링크 다듬기 (필요없는 부분 제거 및 수정)
    news_links = []
    for i in links:
        a = i.replace('\\', '')
        b = a.replace('?Redirect=Log&logNo=', '/')
        news_links.append(b)
    print("[INFO] 뉴스 링크 정리 완료.")

    # 뉴스 링크 하나씩 불러서 뉴스 본문 크롤링
    contents = []
    for idx, i in enumerate(news_links):
        try:
            print(f"\r[INFO] {idx + 1}번째 뉴스 링크 크롤링 중...", end="")
            driver.get(i)  # 뉴스 링크 하나씩 불러오기

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

        except TimeoutException as e:
            contents.append("")  # 빈 내용 추가하고 다음으로 넘어감
        except WebDriverException as e:
            contents.append("")  # 빈 내용 추가하고 다음으로 넘어감
        except Exception as e:
            contents.append("")  # 빈 내용 추가하고 다음으로 넘어감

    print("[INFO] 뉴스 본문 크롤링 완료.")

    # 뉴스 제목과 본문을 결합하여 형태소 분석에 사용할 텍스트 생성
    news_text = ' '.join(titles + contents)
    print("[INFO] 뉴스 제목 및 본문 결합 완료.")

    # Okt 함수를 이용해 형태소 분석
    okt = Okt()
    print("[INFO] 형태소 분석 시작...")
    line = okt.pos(news_text)

    # 명사 또는 형용사만 필터링 + 불용어 제거 + 최소 길이 조건
    stopwords = {'라며', '그리고', '그러나', '하지만', '에서', '에게', '중에', '위해', '조차', '까지', '어디', '무엇', '무슨', '모두', '누구', '생각', '대해', '때문', '사실', '당시', '만약', '이제', '지금', '말씀', '그것', '이것', '저것', '어떤',
                 '부분', '그런', '그거', '그날', '계속', '만날', '얘기', '이런',  '우리', '어느', '있다', '있는', '입니다', '경우', '있습니다', '최근', '이번', '시간', '지난', '소식', '통해', '사진', '무단', '재', '및', '배포', '금지'}
    n_adj = [word for word, tag in line if tag in ['Noun', 'Adjective'] and len(word) > 1 and word not in stopwords]

    # 단어 빈도수 계산
    word_count = Counter(n_adj)
    print("[INFO] 단어 빈도수 계산 완료.")

    # 상위 50개 단어 추출
    tags = word_count.most_common(20)
    print(f"[INFO] 상위 20개 단어 추출 완료 for {name}.")

    # 워드 클라우드 모양 이미지 경로 설정
    img_name = 'cloud.png'
    img_path = os.path.join(current_dir, img_name)

    # 이미지 추가(워드클라우드 모양 설정) - cloud
    mask = Image.new("RGBA", (500, 300), (255, 255, 255))
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
    output_image_name = f'{name}_cloud.png'
    output_image_path = os.path.join(current_dir, output_image_name)

    # cloud 이미지 저장
    plt.savefig(output_image_path, bbox_inches='tight')
    print(f"[INFO] 워드클라우드 저장 완료 for {name}. 파일 경로: {output_image_path}")
    print('-' * 100)

# WebDriver 종료
driver.quit()
print("[INFO] 모든 작업 완료.")
