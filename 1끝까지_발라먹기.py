import time
import ccxt
import telegram ## pip install python-telegram-bot
import asyncio
import datetime
import os

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

symbol = 'LQTY/USDT'
stablecoin = 'USDT'

token = ''
chat_id = ''
timesleep = 0.1 

count3 = 0
count4 = 0
count_익절 = 0
count_롱_물림갯수 = 0
count_숏_물림갯수 = 0

익절갭 = 10
구매갯수 = 10


async def main_시작():
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"거래코인 = {symbol}\n스테이블 코인 = {stablecoin}\n익절갭 = {익절갭}\n코인 구매 단가 = {20}개\n자동 매매를 시작합니다")
            break        
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_에러0(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id,'매매중 에러')
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_에러1(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id,'첫 진입 에러')
            break
        except:
            await asyncio.sleep(timesleep)
            continue

asyncio.run(main_시작())

while True:
    try:
        # 초기설정 (최소거래수량 확인 필요)
        balance = exchange.fetch_balance({'type':'future'})             # 선물 계좌로 변경                       
        symbol_price = exchange.fetch_ticker(symbol)['last']               # 코인 현재가 조회
        params = {
            'positionSide': 'LONG'
        }
        exchange.create_market_buy_order(symbol, 구매갯수, params)
        reference_price = symbol_price                                     # 기준값 설정
        count3 += 1
        break
    except:
        print("에러1")
        asyncio.run(main_에러1()) #봇 실행하는 코드
        continue

while True : 
    if count3 >= count4:
        count3 = 0
        count4 = 0
        while True :
            try:
                symbol_price = exchange.fetch_ticker(symbol)['last'] 
                if symbol_price >= reference_price + 익절갭:
                    
                    params = {
                                'positionSide': 'LONG'
                            }
                    exchange.create_market_sell_order(symbol, 구매갯수, params)
                    exchange.create_market_buy_order(symbol, 구매갯수, params)
                    
                    symbol_price = exchange.fetch_ticker(symbol)['last']    
                    reference_price = symbol_price
                    count3 += 1
                    count_익절 += 1
                    break
                    
                if symbol_price <= reference_price - 익절갭:
                    
                    params = {
                                'positionSide': 'SHORT'
                            }
                    exchange.create_market_sell_order(symbol, 구매갯수, params)
                    
                    symbol_price = exchange.fetch_ticker(symbol)['last']
                    reference_price = symbol_price
                    count4 += 1
                    count_롱_물림갯수 += 1
                    break
            except:
                asyncio.run(main_에러0())
                continue
                
    if count3 < count4:
        count3 = 0
        count4 = 0
        while True :
            try:
                symbol_price = exchange.fetch_ticker(symbol)['last']
                if symbol_price <= reference_price - 익절갭:
                    
                    params = {
                                'positionSide': 'SHORT'
                            }
                    exchange.create_market_buy_order(symbol, 구매갯수, params)
                    exchange.create_market_sell_order(symbol, 구매갯수, params)
                    
                    symbol_price = exchange.fetch_ticker(symbol)['last']
                    reference_price = symbol_price
                    count4 += 1
                    count_익절 += 1
                    break
                    
                if symbol_price <= reference_price + 익절갭:
                    
                    params = {
                                'positionSide': 'LONG'
                            }
                    exchange.create_market_buy_order(symbol, 구매갯수, params)
                    
                    symbol_price = exchange.fetch_ticker(symbol)['last']
                    reference_price = symbol_price
                    count3 += 1
                    break
                    
            except:
                asyncio.run(main_에러0())
                continue
            
