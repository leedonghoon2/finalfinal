import time
import ccxt
import talib

while true :
    exchange = ccxt.binance()  # 사용할 거래소 선택
    symbol = 'BTC/USD'  # 사용할 티커 선택
    timeframe = '1m'  # 사용할 시간프레임 선택

    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)  # 시세 데이터 가져오기
    close_price = [ohlcv[i][4] for i in range(len(ohlcv))]  # 종가 데이터 추출

    rsi = talib.RSI(close_price, timeperiod=14)  # RSI 지표 계산
    print(rsi)  # 계산된 RSI 지표 출력

     time.sleep(60)
