from pykrx import stock
from datetime import datetime
import schedule
import time
import pymysql

# RDS 연결 정보
db_host = 'a9b24215-073f-4067-9f2d-9e9677265084.internal.kr1.mysql.rds.nhncloudservice.com'
db_user = 'team2'
db_password = 'team2'
db_name = 'spotlight_konex'

# 데이터베이스 연결 설정
connection = pymysql.connect(host=db_host, port=3306, user=db_user, password=db_password, db=db_name, charset='utf8mb4')
cursor = connection.cursor()

print("RDS 연결 성공")

# 시세 조회
# 티커, 시가, 고가, 저가, 종가, 거래량, 거래대금, 등락률

def get_konex_data():

    today = datetime.today().strftime('%Y%m%d')

    konex_df = stock.get_market_ohlcv(today, market="KONEX")
    print("데이터 불러오기 성공")
    print(konex_df)

    # 데이터베이스에 저장
    for index, row in konex_df.iterrows():
        # konex_df의 열을 konex_detail 테이블의 열에 매핑
        price = row[0]  # 시가
        cmpprevdd_prc = row[6]  # 등락률
        prev_price = row[3]  # 종가
        trading_volume = row[4]  # 거래
        trading_amount = row[5]  # 거래대금
        corp_code = get_corp_code_from_konex_stock(index)  # stock_konex 테이블에서 corp_code 값을 가져옴

        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 현재 날짜와 시간
        modified_at = created_at

        # 오늘의 데이터가 이미 있는지 확인
        check_query = '''
        SELECT * FROM konex_detail 
        WHERE DATE(created_at) = %s AND corp_code = %s
        '''

        cursor.execute(check_query, (today, corp_code))
        existing_data = cursor.fetchone()

        if existing_data:
            # 데이터가 이미 있는 경우 업데이트
            update_query = '''
            UPDATE konex_detail 
            SET 
                price = %s,
                cmpprevdd_prc = %s,
                prev_price = %s,
                trading_volume = %s,
                trading_amount = %s,
                modified_at = %s
            WHERE 
                DATE(created_at) = %s AND corp_code = %s
            '''

            update_values = (
                price,
                cmpprevdd_prc,
                prev_price,
                trading_volume,
                trading_amount,
                modified_at,
                today,
                corp_code
            )

            cursor.execute(update_query, update_values)
            print("RDS에 데이터 업데이트 완료")
        else:
            # 데이터가 없는 경우 새로운 데이터 삽입
            insert_query = '''
            INSERT INTO konex_detail 
            (price, cmpprevdd_prc, prev_price, trading_volume, trading_amount, corp_code, modified_at, created_at)
            VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s)
            '''

            insert_values = (
                price,
                cmpprevdd_prc,
                prev_price,
                trading_volume,
                trading_amount,
                corp_code,
                modified_at,
                created_at
            )

            cursor.execute(insert_query, insert_values)
            print("RDS에 데이터 저장 완료")

    connection.commit()

def get_corp_code_from_konex_stock(stock_code):
    
    select_query = '''
    SELECT corp_code FROM konex_stock WHERE stock_code = %s
    '''

    cursor.execute(select_query, (stock_code,))
    result = cursor.fetchone()
    print(result)
    
    # corp_code 반환
    return result[0] if result else None

# test
get_konex_data()

# 평일 오전 9시 ~ 오후 3시 반에 10분마다 함수 실행
def scheduler():
    current_time = datetime.now().time()
    weekday = datetime.today().weekday()

    # 평일(월요일부터 금요일까지) 오전 9시부터 오후 3시 반까지 10분마다 실행
    if 0 <= weekday <= 4 and datetime.strptime("09:00", "%H:%M").time() <= current_time <= datetime.strptime("15:30", "%H:%M").time():
        get_konex_data()
    else:
        print("스케줄러 동작 시간 아님")

schedule.every(1).minutes.do(scheduler)

while True:
    schedule.run_pending()
    time.sleep(1)