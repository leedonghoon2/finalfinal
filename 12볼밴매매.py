import time
import ccxt
import telegram ## pip install python-telegram-bot
import asyncio
import datetime
import os
import numpy as np

# 계좌 조회
api_key = ''
api_secret = ''

exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future',
        'adjustForTimeDifference': True,
        'recvWindow': 10000
    }
})

# 설정값
기준갭 = 0.005
추매비율 = 0.7
start = 0.05
leverage = 15 # 레버리지
timesleep = 0.01 # 대기시간
period = 20  # 볼린저밴드 주기
stddev = 1.7  # 표준편차
timeframe = '3m' # 기준봉

symbol = 'LOOM/USDT'
symbol2 = 'LOOMUSDT'
stablecoin = 'USDT'

token = ''
chat_id = ''

count = 0

async def main_시작():
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"기준갭 = {기준갭}\n추매비율 = {추매비율}\n시작비율 = {start}\n레버리지 = {leverage}\n밴드주기 = {period}\n표준편차 = {stddev}\n기준봉 = {timeframe}\n거래코인 = {symbol}")
            break        
        except:
            await asyncio.sleep(timesleep)
            continue

async def main_에러0(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id,'에러0')
            break
        except:
            await asyncio.sleep(timesleep)
            continue

async def main_에러1(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id,'에러_사이클시작')
            break
        except:
            await asyncio.sleep(timesleep)
            continue

async def main_에러2(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id,'에러_사이클중간')
            break
        except:
            await asyncio.sleep(timesleep)
            continue

async def main_에러3(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id,'에러_포지션조회')
            break
        except:
            await asyncio.sleep(timesleep)

async def main_정산_매매(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"청산 {count}")
            break
        except:
            await asyncio.sleep(timesleep)
            continue

asyncio.run(main_시작())

while True:
    while True:
        try:
            # 초기설정 (최소거래수량 확인 필요)
            balance = exchange.fetch_balance({'type':'future'})             # 선물 계좌로 변경
            binance_balance = balance[stablecoin]['free']                          # 계좌 잔고 조회
            symbol_price = exchange.fetch_ticker(symbol)['last']               # 현재가 조회
            amount = (binance_balance * start * leverage) / symbol_price
            count = 0
            break
        except:
            print("에러1")
            asyncio.run(main_에러1()) #봇 실행하는 코드
    
    while True:
        # 밴드 계산
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=period)
        closes = np.array([x[4] for x in ohlcv], dtype=float)
        sma = np.mean(closes)
        std = np.std(closes)
        upper = sma + (stddev * std)
        lower = sma - (stddev * std)

        # 비트코인 현재가 확인
        symbol_price = exchange.fetch_ticker(symbol)['last']
        time.sleep(timesleep)

        if symbol_price >= upper+(upper*기준갭): # 상단밴드 체크
            exchange.create_market_sell_order(symbol, amount)
            while True:
                try:
                    positions = exchange.fapiPrivateV2GetPositionRisk({'symbol': symbol2})
                    amount = abs(float(positions[0]['positionAmt']))
                    reference_price = float(positions[0]['entryPrice'])
                    break
                except:
                    print("에러3")
                    asyncio.run(main_에러3()) #봇 실행하는 코드
                    continue
            while True:
                # 밴드 계산
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=period)
                closes = np.array([x[4] for x in ohlcv], dtype=float)
                sma = np.mean(closes)
                std = np.std(closes)
                upper = sma + (stddev * std)
                lower = sma - (stddev * std)

                # 비트코인 현재가 확인
                symbol_price = exchange.fetch_ticker(symbol)['last']
                time.sleep(timesleep)

                if symbol_price >= reference_price+(reference_price*기준갭): # 추가매매부분
                    exchange.create_market_sell_order(symbol, amount*추매비율) # 추가매매
                    while True:
                        try:
                            positions = exchange.fapiPrivateV2GetPositionRisk({'symbol': symbol2}) # 포지션조회
                            amount = abs(float(positions[0]['positionAmt']))
                            reference_price = float(positions[0]['entryPrice'])
                            break
                        except:
                            print("에러3")
                            asyncio.run(main_에러3()) #봇 실행하는 코드
                            continue

                elif symbol_price <= upper: # 청산부분
                    exchange.create_market_buy_order(symbol, amount) # 청산
                    count += 1
                    asyncio.run(main_정산_매매())
                    break

        elif symbol_price <= lower-(lower*기준갭): # 하단밴드 체크
            exchange.create_market_buy_order(symbol, amount)
            while True:
                try:
                    positions = exchange.fapiPrivateV2GetPositionRisk({'symbol': symbol2})
                    amount = abs(float(positions[0]['positionAmt']))
                    reference_price = float(positions[0]['entryPrice'])
                    break
                except:
                    print("에러3")
                    asyncio.run(main_에러3()) #봇 실행하는 코드
                    continue
            while True:
                # 밴드 계산
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=period)
                closes = np.array([x[4] for x in ohlcv], dtype=float)
                sma = np.mean(closes)
                std = np.std(closes)
                upper = sma + (stddev * std)
                lower = sma - (stddev * std)

                # 비트코인 현재가 확인
                symbol_price = exchange.fetch_ticker(symbol)['last']
                time.sleep(timesleep)

                if symbol_price <= reference_price-(reference_price*기준갭): # 추가매매부분
                    exchange.create_market_buy_order(symbol, amount*추매비율) # 추가매매
                    while True:
                        try:
                            positions = exchange.fapiPrivateV2GetPositionRisk({'symbol': symbol2}) # 포지션조회
                            amount = abs(float(positions[0]['positionAmt']))
                            reference_price = float(positions[0]['entryPrice'])
                            break
                        except:
                            print("에러3")
                            asyncio.run(main_에러3()) #봇 실행하는 코드
                            continue

                elif symbol_price >= lower: # 청산부분
                    exchange.create_market_sell_order(symbol, amount) # 청산
                    count += 1
                    asyncio.run(main_정산_매매())
                    break
