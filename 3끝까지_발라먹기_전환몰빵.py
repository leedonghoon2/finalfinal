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

symbol = 'HBAR/USDT'
stablecoin = 'USDT'

token = ''
chat_id = ''
timesleep = 0.1 

count3 = 0
count4 = 0
count_익절 = 0
count_익절유무 = 1
count_롱_물림갯수 = 0
count_숏_물림갯수 = 0
count_수량차이 = 0

익절갭 = 0.0001
구매갯수 = 100


async def main_시작():
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"거래코인 = {symbol}\n스테이블 코인 = {stablecoin}\n익절갭 = {익절갭}\n코인 구매 단가 = {구매갯수}개\n자동 매매를 시작합니다")
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
        
async def main_롱_매수_추적기(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"LONG_OPEN = {symbol_price}")
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_롱_매도_추적기(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"LONG_CLOSE= {symbol_price}")
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_숏_매수_추적기(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"SHORT_OPEN= {symbol_price}")
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_숏_매도_추적기(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"SHORT_CLOSE= {symbol_price}")
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        

async def main_정산_매매(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"익절 = {count_익절}\n롱 물림 갯수 = {count_롱_물림갯수}\n숏 물림 갯수 = {count_숏_물림갯수}")
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
        reference_price = symbol_price            # 기준값 설정
        reference_price_long = symbol_price
        reference_price_short = reference_price_long
        count_수량차이 += 1
        asyncio.run(main_롱_매수_추적기())
        count3 += 1
        break
    except:
        print("에러1")
        asyncio.run(main_에러1()) #봇 실행하는 코드
        continue

# print("첫 매수 무한루프 탈출완료")
# print(f"기준가 = {reference_price}")

while True : 
    if count_수량차이 == 10:
        params = {
                    'positionSide': 'LONG'
                    }
        exchange.create_market_sell_order(symbol, params)
        
        params = {
                    'positionSide': 'SHORT'
                    }
        exchange.create_market_sell_order(symbol, params)
    
    if count3 >= count4:
        count3 = 0
        count4 = 0
        while True :
            try:
                        symbol_price = exchange.fetch_ticker(symbol)['last']
                
                        if symbol_price >= reference_price + 익절갭:
                                # print("매수조건 충족")
                                params = {
                                            'positionSide': 'LONG'
                                        }
                                
                                
                                exchange.create_market_buy_order(symbol, 구매갯수, params)
                                asyncio.run(main_롱_매수_추적기())
                                # print("롱 매수 완료")
                                    
                                reference_price = symbol_price
                                # print("기준가 갱신")
                                # print(f"기준가 = {reference_price}")
                                count3 += 1
                                count_익절 += 1
                                count_수량차이 += 1
                                # print("익절")
                                
                                asyncio.run(main_정산_매매())
                                
                                break
                            
                        if symbol_price <= reference_price - 익절갭:
                                # print("매도조건 충족")
                                params = {
                                            'positionSide': 'SHORT'
                                        }
                                if count_수량차이 == 0:
                                    count_수량차이 = 1
                                exchange.create_market_sell_order(symbol, 구매갯수 * count_수량차이, params)
                                asyncio.run(main_숏_매수_추적기())
                                # print("숏 오픈")
                                reference_price = symbol_price
                        
                                # print("기준가 갱신")
                                # print(f"기준가 = {reference_price}")
                                count4 += 1
                                count_롱_물림갯수 += 1
                                count_수량차이 = 0
                                print("방향 전환")

                                asyncio.run(main_정산_매매())
                                
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
                            # print("매도조건 충족")
                            params = {
                                        'positionSide': 'SHORT'
                                    }
                            
                            exchange.create_market_sell_order(symbol, 구매갯수, params)
                            asyncio.run(main_숏_매수_추적기())
                            
                            # print("숏 매도 완료")
                            
                            reference_price = symbol_price
                
                            # print("기준가 갱신")
                            # print(f"기준가 = {reference_price}")
                            count4 += 1
                            count_익절 += 1
                            count_수량차이 += 1
                            # print("익절")
                            
                            asyncio.run(main_정산_매매())
                            
                            break
                        
                        if symbol_price >= reference_price + 익절갭:
                            # print("매수조건 충족")
                            
                            params = {
                                        'positionSide': 'LONG'
                                    }
                            if count_수량차이 == 0:
                                count_수량차이 = 1
                            exchange.create_market_buy_order(symbol, 구매갯수 * count_수량차이, params)
                            asyncio.run(main_롱_매수_추적기())
                            # print("롱 오픈")
                            
                            reference_price = symbol_price
                            
                            # print("기준가 갱신")
                            # print(f"기준가 = {reference_price}")
                            count3 += 1
                            count_숏_물림갯수 += 1
                            count_수량차이 = 0
                            # print("방향 전환")
                            
                            asyncio.run(main_정산_매매())
                            
                            break
            except:
                asyncio.run(main_에러0())
                continue
            
