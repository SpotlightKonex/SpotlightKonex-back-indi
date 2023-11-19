from pykrx import stock
from datetime import datetime
import schedule
import time
import pymysql

# RDS 연결 정보
db_host = '8387448b-ff4e-41ea-874f-130b33bfd64d.external.kr1.mysql.rds.nhncloudservice.com'
db_user = 'team2'
db_password = 'team2'
db_name = 'spotlight_konex'

# 데이터베이스 연결 설정
connection = pymysql.connect(host=db_host, port=13306, user=db_user, password=db_password, db=db_name, charset='utf8mb4')
cursor = connection.cursor()

print("RDS 연결 성공")

# 테이블 생성 쿼리
create_table_query = '''
CREATE TABLE IF NOT EXISTS konex_detail (
    price BIGINT,
    cmpprevdd_prc BIGINT,
    prev_price BIGINT,
    trading_volume VARCHAR(255),
    transaction_amount BIGINT,
    crop_code VARCHAR(50),
    modified_at TIMESTAMP,
    created_at TIMESTAMP
);
'''

# 테이블 생성
cursor.execute(create_table_query)
connection.commit()

print("테이블 생성 성공")

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
        transaction_amount = row[5]  # 거래대금
        crop_code = get_crop_code_from_konex_stock(index)  # stock_konex 테이블에서 crop_code 값을 가져옴

        modified_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 현재 날짜와 시간
        created_at = modified_at  # 생성일은 수정일과 동일하게 설정

        insert_query = '''
        INSERT INTO konex_detail 
        (price, cmpprevdd_prc, prev_price, trading_volume, transaction_amount, crop_code, modified_at, created_at)
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        
        values = (
            price,
            cmpprevdd_prc,
            prev_price,
            trading_volume,
            transaction_amount,
            crop_code,
            modified_at,
            created_at
        )

        cursor.execute(insert_query, values)

    connection.commit()
    print("RDS에 데이터 저장 완료")

def get_crop_code_from_konex_stock(stock_code):

    select_query = '''
    SELECT crop_code FROM konex_stock WHERE stock_code = %s
    '''
    
    # 쿼리 실행
    cursor.execute(select_query, (stock_code,))
    
    # 결과 가져오기
    result = cursor.fetchone()
    print(result)
    
    # crop_code 반환
    return result[0] if result else None

# test
get_konex_data()

# # 매일 오전 8시에 getKonexData 함수 등록
# schedule.every().day.at("08:00").do(get_konex_data)

# while True:
#     # 스케줄에 등록된 작업을 확인하고 실행
#     schedule.run_pending()
#     time.sleep(1)