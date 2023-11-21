from pykrx import stock

konex_df_1115 = stock.get_market_ohlcv("20231115", market="KONEX")
konex_df_1116 = stock.get_market_ohlcv("20231116", market="KONEX")
konex_df_1117 = stock.get_market_ohlcv("20231117", market="KONEX")

# CSV 파일로 저장
konex_df_1115.to_csv("konex_df_1115.csv", index=True, encoding='utf-8')
konex_df_1116.to_csv("konex_df_1116.csv", index=True, encoding='utf-8')
konex_df_1117.to_csv("konex_df_1117.csv", index=True, encoding='utf-8')