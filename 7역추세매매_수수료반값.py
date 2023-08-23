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

count_익절 = 0
count_롱_보유갯수 = 0
count_숏_보유갯수 = 0

익절갭 = 0.00100
구매갯수 = 100
포지션최대보유가능갯수 = 40
스페어물량 = 5
청산물량 = 5

async def main_시작():
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"거래코인 = {symbol}\n스테이블 코인 = {stablecoin}\n익절갭 = {익절갭}\n코인 구매 단가 = {구매갯수}개\n최대 보유 가능 포지션 수량 = {포지션최대보유가능갯수}\n스페어 물량 = {스페어물량}\n자동 매매를 시작합니다")
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
        
async def main_롱_매수_추적기_정산매매(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"LONG_OPEN = {symbol_price}\n익절 = {count_익절}\n롱 보유 갯수 = {count_롱_보유갯수}\n숏 보유 갯수 = {count_숏_보유갯수}")
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_롱_매도_추적기_정산매매(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"LONG_CLOSE= {symbol_price}\n익절 = {count_익절}\n롱 보유 갯수 = {count_롱_보유갯수}\n숏 보유 갯수 = {count_숏_보유갯수}")
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_숏_매수_추적기_정산매매(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"SHORT_OPEN= {symbol_price}\n익절 = {count_익절}\n롱 보유 갯수 = {count_롱_보유갯수}\n숏 보유 갯수 = {count_숏_보유갯수}")
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_숏_매도_추적기_정산매매(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"SHORT_CLOSE= {symbol_price}\n익절 = {count_익절}\n롱 보유 갯수 = {count_롱_보유갯수}\n숏 보유 갯수 = {count_숏_보유갯수}")
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_숏_한계치도달(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"숏 물량 한계치 도달로 {청산물량_숏_손절}익절 반납\n익절 = {count_익절}")
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_롱_한계치도달(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"롱 물량 한계치 도달로 {청산물량_롱_손절}익절 반납\n익절 = {count_익절}")
            break
        except:
            await asyncio.sleep(timesleep)
            continue        

async def main_정산_매매(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"익절 = {count_익절}\n롱 보유 갯수 = {count_롱_보유갯수}\n숏 보유 갯수 = {count_숏_보유갯수}")
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
            'positionSide': 'SHORT'
        }
        exchange.create_market_sell_order(symbol, 구매갯수, params)
        asyncio.run(main_숏_매수_추적기_정산매매())
        count_숏_보유갯수 += 1
        break
    
    except:
        print("에러1")
        asyncio.run(main_에러1()) #봇 실행하는 코드
        continue


while True : 
    try:
        symbol_price = exchange.fetch_ticker(symbol)['last']
        
        if count_숏_보유갯수 >= 포지션최대보유가능갯수 - 스페어물량:
            청산물량_숏_손절 = (((count_숏_보유갯수 - 1) + (count_숏_보유갯수 - 청산물량)) * 청산물량)/2
            params = {
                        'positionSide': 'SHORT'
                    }
            exchange.create_market_buy_order(symbol, 구매갯수 * 청산물량, params)
        
            count_숏_보유갯수 -= 청산물량
            count_익절 -= 청산물량_숏_손절
            asyncio.run(main_숏_한계치도달)
            
            
        if count_롱_보유갯수 >= 포지션최대보유가능갯수 - 스페어물량:
            청산물량_롱_손절 = (((count_롱_보유갯수 - 1) + (count_롱_보유갯수 - 청산물량)) * 청산물량)/2
            params = {
                        'positionSide': 'LONG'
                        }
            exchange.create_market_sell_order(symbol, 구매갯수 * 청산물량, params)
            
            count_롱_보유갯수 -= 청산물량
            count_익절 -= 청산물량_롱_손절
            asyncio.run(main_롱_한계치도달)
        
        # 본 매매 시작
        
        if symbol_price >= reference_price + 익절갭:
            reference_price = symbol_price
            
            if count_숏_보유갯수 >= count_롱_보유갯수:
                
                params = {
                            'positionSide': 'SHORT'
                            }
                exchange.create_market_sell_order(symbol, 구매갯수, params)
                asyncio.run(main_숏_매수_추적기_정산매매())
                
                count_숏_보유갯수 += 1
                                    
                break
            
            if count_롱_보유갯수 > count_숏_보유갯수:
                
                params = {
                            'positionSide': 'LONG'
                            }
                exchange.create_market_sell_order(symbol, 구매갯수, params)
                asyncio.run(main_롱_매도_추적기_정산매매())
                
                count_롱_보유갯수 -= 1
                
                break
            
        if symbol_price <= reference_price - 익절갭:
            reference_price = symbol_price
            
            if count_숏_보유갯수 > count_롱_보유갯수:
                
                params = {
                            'positionSide': 'SHORT'
                            }
                exchange.create_market_buy_order(symbol, 구매갯수, params)
                
                asyncio.run(main_숏_매도_추적기_정산매매())
                
                count_숏_보유갯수 -= 1
                
                break
            
            if count_롱_보유갯수 >= count_숏_보유갯수:

                params = {
                            'positionSide': 'LONG'
                            }
                exchange.create_market_buy_order(symbol, 구매갯수, params)
                asyncio.run(main_롱_매수_추적기_정산매매())
                
                count_롱_보유갯수 += 1
                
                break
    except:
        asyncio.run(main_에러0())
        continue
