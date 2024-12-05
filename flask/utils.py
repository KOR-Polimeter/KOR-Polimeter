from models import fetch_name, fetch_votes, insert_chart
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os
import boto3
from dotenv import load_dotenv
from io import BytesIO

# S3 연결
def s3_connect():
    load_dotenv()
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('S3_SECRET_KEY'),
        region_name='ap-northeast-2'
    )
    return s3


# 차트 생성
def create_chart(pol_id):
    name = fetch_name(pol_id)
    if not name:
        return None, f"Politician with ID {pol_id} not found."

    data = fetch_votes(pol_id)
    if data.empty:
        return None, f"No vote data for {name} (id: {pol_id})."

    # 차트 생성
    plt.plot(data['date'], data['votes'], marker='o', label=name)
    plt.title(f"Vote Trend for {name}")
    plt.xlabel("Date")
    plt.ylabel("Votes")
    plt.legend()

    # 메모리에 차트 저장
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)  # 버퍼의 시작으로 포인터 이동
    plt.close()

    return img_buffer, None


# S3 업로드
def upload_s3(buffer, file_name):
    s3 = s3_connect()
    bucket_name = 'kortest'
    try:
        s3.upload_fileobj(buffer, bucket_name, file_name)
        print(f"Uploaded chart to s3://{bucket_name}/{file_name}")
    except Exception as e:
        return None, f"Failed to upload chart to S3: {str(e)}"

    # S3 파일 경로 반환
    return f"s3://{bucket_name}/{file_name}", None


# 통합 함수
def process_chart(pol_id):
    try:
        # 차트 생성
        chart_buffer, error = create_chart(pol_id)
        if error:
            return None, error

        # S3 업로드
        fname = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_pol-{pol_id}"
        s3_file_path = f"charts/{fname}.png"
        file_url, error = upload_s3(chart_buffer, s3_file_path)
        if error:
            return None, error

        # DB 저장
        insert_chart(pol_id, s3_file_path)  # 필요한 매개변수 전달
        return file_url, None

    except Exception as e:
        # 모든 예외를 처리
        return None, f"Unexpected error: {str(e)}"

