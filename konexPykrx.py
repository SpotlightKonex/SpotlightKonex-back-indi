from pykrx import stock
from datetime import datetime
import schedule
import time

# 시세 조회
# 티커, 시가, 고가, 저가, 종가, 거래량, 거래대금, 등락률

def get_konex_data():

    today = datetime.today().strftime('%Y%m%d')

    konex_df = stock.get_market_ohlcv(today, market="KONEX")
    print(konex_df)

# test
get_konex_data()

# 매일 오전 8시에 getKonexData 함수 등록
schedule.every().day.at("08:00").do(get_konex_data)

while True:
    # 스케줄에 등록된 작업을 확인하고 실행
    schedule.run_pending()
    time.sleep(1)