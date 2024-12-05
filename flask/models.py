#models.py
import utils as u
import pymysql
import pandas as pd

# 데이터베이스 연결
def db_connect():
    return pymysql.connect(
                    host='127.0.0.1',
                    user='root', 
                    password='1234', 
                    db='kor-polimeter', 
                    charset='utf8')

# 특정 정치인의 투표 데이터를 가져오는 함수
def fetch_votes(pol_id):
    conn = db_connect()
    query = """
        SELECT
            DATE_FORMAT(vt.created_at,'%%Y-%%m-%%d') AS date,
            SUM(vr.count) AS votes
        FROM
            Votes_result vr
        JOIN
            Votes_topic vt ON vr.votes_topic_id = vt.id
        WHERE
            vr.politician_id = %s
        GROUP BY 
            date
        ORDER BY 
            date ASC;
    """
    data = pd.read_sql(query,conn,params=(pol_id,))
    conn.close()

    return data

# 정치인 이름 가져오기 함수
def fetch_name(pol_id):
    conn = db_connect()
    query = "SELECT name FROM Politicians WHERE id = %s;"
    with conn.cursor() as cursor:
        cursor.execute(query, (pol_id,))
        result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

#s3 파일 경로 DB 저장
def insert_chart(pol_id,img_url):
    conn = db_connect()
    cursor = conn.cursor()
    try:
        query = """
                INSERT INTO ChartImg (politician_id,img_path,uploaded_at)
                VALUES (%s, %s, NOW());
                """
        cursor.execute(query,(pol_id,img_url))
        conn.commit()
        print("Chart data inserted successfully.")
    
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

    finally:
        # 연결 종료
        cursor.close()
        conn.close()




