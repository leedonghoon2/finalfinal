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

symbol = 'BLZ/USDT'
stablecoin = 'USDT'

token = ''
chat_id = ''
timesleep = 0

count_손절 = 0
count_추세매매_익절 = 0
count_추세_롱_보유갯수 = 0
count_추세_숏_보유갯수 = 0


익절갭 = 0.00100
구매갯수 = 100
추세매매익절발동물량 = 10

async def main_시작():
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"거래코인 = {symbol}\n스테이블 코인 = {stablecoin}\n갭 = {익절갭}\n코인 구매 단가 = {구매갯수}개\n추세 매매 익절 발동 물량 = {추세매매익절발동물량}개\n자동 매매를 시작합니다")
            break        
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_손절중에러(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id,'손절 에러 발생')
            break
        except:
            await asyncio.sleep(timesleep)
            continue

async def main_익절중에러(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id,'익절 에러 발생')
            break
        except:
            await asyncio.sleep(timesleep)
            continue

        
async def main_에러0(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id,'매매 에러 발생')
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_에러1(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id,'첫 진입 에러 발생')
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_롱_매수_추적기_정산매매(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"LONG_OPEN = {symbol_price}\n기준가 = {reference_price}\n------------------------\n익절 = {count_추세매매_익절}\n손절 = {count_손절}\n------------------------\n  (추세)  롱 보유 갯수 = {count_추세_롱_보유갯수}\n  (추세)  숏 보유 갯수 = {count_추세_숏_보유갯수}\n------------------------")
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_롱_매도_추적기_정산매매(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"LONG_CLOSE= {symbol_price}\n기준가 = {reference_price}\n------------------------\n익절 = {count_추세매매_익절}\n손절 = {count_손절}\n------------------------\n  (추세)  롱 보유 갯수 = {count_추세_롱_보유갯수}\n  (추세)  숏 보유 갯수 = {count_추세_숏_보유갯수}\n------------------------")
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_숏_매수_추적기_정산매매(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"SHORT_OPEN= {symbol_price}\n기준가 = {reference_price}\n------------------------\n익절 = {count_추세매매_익절}\n손절 = {count_손절}\n------------------------\n  (추세)  롱 보유 갯수 = {count_추세_롱_보유갯수}\n  (추세)  숏 보유 갯수 = {count_추세_숏_보유갯수}\n------------------------")
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_숏_매도_추적기_정산매매(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"SHORT_CLOSE= {symbol_price}\n기준가 = {reference_price}\n------------------------\n익절 = {count_추세매매_익절}\n손절 = {count_손절}\n------------------------\n  (추세)  롱 보유 갯수 = {count_추세_롱_보유갯수}\n  (추세)  숏 보유 갯수 = {count_추세_숏_보유갯수}\n------------------------")
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
        
async def main_추세_숏_목표값도달(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"숏 물량 목표치 도달로 {(추세매매익절발동물량 * (추세매매익절발동물량 - 1))/2}개 익절 성공")
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_추세_롱_목표값도달(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"롱 물량 목표치 도달로 {(추세매매익절발동물량 * (추세매매익절발동물량 - 1))/2}개 익절 성공")
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
        reference_price = symbol_price

        params = {
            'positionSide': 'LONG'
        }
        exchange.create_market_buy_order(symbol, 구매갯수, params)
        
        count_추세_롱_보유갯수 += 1
        asyncio.run(main_롱_매수_추적기_정산매매())
        break
    
    except:
        print("에러1")
        asyncio.run(main_에러1())
        continue


while True : 
    try:
        symbol_price = exchange.fetch_ticker(symbol)['last']
                
        if count_추세_숏_보유갯수 >= 추세매매익절발동물량:
            while True:
                try:
                    params = {
                                'positionSide': 'SHORT'
                                }
                    exchange.create_market_buy_order(symbol, 구매갯수 * 추세매매익절발동물량, params)
                    
                    count_추세_숏_보유갯수 -= 추세매매익절발동물량
                    count_추세매매_익절 += (추세매매익절발동물량 * (추세매매익절발동물량 - 1))/2
                    asyncio.run(main_추세_숏_목표값도달())
                    
                    break
                except:
                    asyncio.run(main_익절중에러())
                    continue
                
        if count_추세_롱_보유갯수 >= 추세매매익절발동물량:
            while True:
                try:
                    params = {
                                'positionSide': 'LONG'
                                }
                    exchange.create_market_sell_order(symbol, 구매갯수 * 추세매매익절발동물량, params)
                    
                    count_추세_롱_보유갯수 -= 추세매매익절발동물량
                    count_추세매매_익절 += (추세매매익절발동물량 * (추세매매익절발동물량 - 1))/2
                    asyncio.run(main_추세_롱_목표값도달())
                    
                    break
                except:
                    asyncio.run(main_익절중에러())
                    continue
        
        # 본 매매 시작
        if symbol_price >= reference_price + 익절갭:
            while True:
                try:
                    reference_price = symbol_price
                    
                    #########################################추세매매 방식#########################################    
                    if count_추세_롱_보유갯수 >= count_추세_숏_보유갯수:
                        while True:
                            try:
                                params = {
                                            'positionSide': 'LONG'
                                            }
                                exchange.create_market_buy_order(symbol, 구매갯수, params)
                                
                                count_추세_롱_보유갯수 += 1
                                asyncio.run(main_롱_매수_추적기_정산매매())
                                
                                break
                            except:
                                asyncio.run(main_에러0())
                                continue
                            
                    if count_추세_숏_보유갯수 > count_추세_롱_보유갯수:
                        while True:
                            try:
                                params = {
                                            'positionSide': 'SHORT'
                                            }
                                exchange.create_market_buy_order(symbol, 구매갯수, params)
                                
                                count_추세_숏_보유갯수 -= 1
                                count_손절 += 1
                                asyncio.run(main_숏_매도_추적기_정산매매())
                                
                                break
                            except:
                                asyncio.run(main_에러0())
                                continue
                    ###########################################################################################
                    break
                except:
                    continue
            
        if symbol_price <= reference_price - 익절갭:       
            while True:    
                try:
                    reference_price = symbol_price
                    
                    #########################################추세매매 방식#########################################
                    if count_추세_롱_보유갯수 > count_추세_숏_보유갯수:
                        while True:
                            try:
                                params = {
                                            'positionSide': 'LONG'
                                            }
                                exchange.create_market_sell_order(symbol, 구매갯수, params)
                    
                                count_추세_롱_보유갯수 -= 1
                                count_손절 += 1
                                asyncio.run(main_롱_매도_추적기_정산매매())
                                
                                break
                            except:
                                asyncio.run(main_에러0())
                                continue
                            
                    if count_추세_숏_보유갯수 >= count_추세_롱_보유갯수:
                        while True:
                            try:
                                params = {
                                            'positionSide': 'SHORT'
                                            }
                                exchange.create_market_sell_order(symbol, 구매갯수, params)
                                
                                count_추세_숏_보유갯수 += 1
                                asyncio.run(main_숏_매수_추적기_정산매매())
                                
                                break
                            except:
                                asyncio.run(main_에러0())
                                continue
                    ###########################################################################################
                    
                    break
                except:
                    continue
                
    except:
        asyncio.run(main_에러0())
        continue
