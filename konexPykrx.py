from pykrx import stock

# 시세 조회
# 티커, 시가, 고가, 저가, 종가, 거래량, 거래대금, 등락률
# 티커, 시가, 종가, 거래량, 거래대금, 등락률

def getKonexData():

    konexDataFrame = stock.get_market_ohlcv("20231117", market="KONEX")
    print(konexDataFrame)

# # 순매수 상위종목
# # 티커, 종목명, 매도거래량, 매수거래량, 순매수거래량, 매도거래대금, 매수거래대금, 순매수거래대금

# df = stock.get_market_net_purchases_of_equities("20231117", "20231117", "KONEX", "전체")
# print(df)

