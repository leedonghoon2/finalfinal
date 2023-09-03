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
count_손절 = 0
count_추세매매_익절 = 0
count_역추세_롱_보유갯수 = 0
count_역추세_숏_보유갯수 = 0
count_추세_롱_보유갯수 = 0
count_추세_숏_보유갯수 = 0


익절갭 = 0.00100
구매갯수 = 100
포지션최대보유가능갯수 = 200
스페어물량 = 0
청산물량 = 3
추세매매익절발동물량 = 3

async def main_시작():
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"거래코인 = {symbol}\n스테이블 코인 = {stablecoin}\n익절갭 = {익절갭}\n코인 구매 단가 = {구매갯수}개\n최대 보유 가능 포지션 수량 = {포지션최대보유가능갯수}\n스페어 물량 = {스페어물량}\n손절물량 = {청산물량}\n추세 매매 익절 발동 물량 = {추세매매익절발동물량}자동 매매를 시작합니다")
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
            await bot.send_message(chat_id, f"LONG_OPEN = {symbol_price}\n기준가 = {reference_price}\n------------------------\n익절 = {count_익절}\n손절 = {count_손절}\n추세매매 익절 = {count_추세매매_익절}\n------------------------\n(역추세) 롱 보유 갯수 = {count_역추세_롱_보유갯수}\n역추세 숏 보유 갯수 = {count_역추세_숏_보유갯수}\n------------------------\n  (추세)  롱 보유 갯수 = {count_추세_롱_보유갯수}\n  (추세)  숏 보유 갯수 = {count_추세_숏_보유갯수}\n------------------------\n롱 보유 갯수 = {count_추세_롱_보유갯수 + count_역추세_롱_보유갯수}\n숏 보유 갯수 = {count_추세_숏_보유갯수 + count_역추세_숏_보유갯수}\n------------------------\n역추세 매매 기대 익절값 = {count_익절}\n역추세+추세 매매 기대 익절값 = {count_익절 - count_손절 + count_추세매매_익절}\n------------------------")
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_롱_매도_추적기_정산매매(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"LONG_CLOSE= {symbol_price}\n기준가 = {reference_price}\n------------------------\n익절 = {count_익절}\n손절 = {count_손절}\n추세매매 익절 = {count_추세매매_익절}\n------------------------\n(역추세) 롱 보유 갯수 = {count_역추세_롱_보유갯수}\n역추세 숏 보유 갯수 = {count_역추세_숏_보유갯수}\n------------------------\n  (추세)  롱 보유 갯수 = {count_추세_롱_보유갯수}\n  (추세)  숏 보유 갯수 = {count_추세_숏_보유갯수}\n------------------------\n롱 보유 갯수 = {count_추세_롱_보유갯수 + count_역추세_롱_보유갯수}\n숏 보유 갯수 = {count_추세_숏_보유갯수 + count_역추세_숏_보유갯수}\n------------------------\n역추세 매매 기대 익절값 = {count_익절}\n역추세+추세 매매 기대 익절값 = {count_익절 - count_손절 + count_추세매매_익절}\n------------------------")
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_숏_매수_추적기_정산매매(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"SHORT_OPEN= {symbol_price}\n기준가 = {reference_price}\n------------------------\n익절 = {count_익절}\n손절 = {count_손절}\n추세매매 익절 = {count_추세매매_익절}\n------------------------\n(역추세) 롱 보유 갯수 = {count_역추세_롱_보유갯수}\n역추세 숏 보유 갯수 = {count_역추세_숏_보유갯수}\n------------------------\n  (추세)  롱 보유 갯수 = {count_추세_롱_보유갯수}\n  (추세)  숏 보유 갯수 = {count_추세_숏_보유갯수}\n------------------------\n롱 보유 갯수 = {count_추세_롱_보유갯수 + count_역추세_롱_보유갯수}\n숏 보유 갯수 = {count_추세_숏_보유갯수 + count_역추세_숏_보유갯수}\n------------------------\n역추세 매매 기대 익절값 = {count_익절}\n역추세+추세 매매 기대 익절값 = {count_익절 - count_손절 + count_추세매매_익절}\n------------------------")
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_숏_매도_추적기_정산매매(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"SHORT_CLOSE= {symbol_price}\n기준가 = {reference_price}\n------------------------\n익절 = {count_익절}\n손절 = {count_손절}\n추세매매 익절 = {count_추세매매_익절}\n------------------------\n(역추세) 롱 보유 갯수 = {count_역추세_롱_보유갯수}\n역추세 숏 보유 갯수 = {count_역추세_숏_보유갯수}\n------------------------\n  (추세)  롱 보유 갯수 = {count_추세_롱_보유갯수}\n  (추세)  숏 보유 갯수 = {count_추세_숏_보유갯수}\n------------------------\n롱 보유 갯수 = {count_추세_롱_보유갯수 + count_역추세_롱_보유갯수}\n숏 보유 갯수 = {count_추세_숏_보유갯수 + count_역추세_숏_보유갯수}\n------------------------\n역추세 매매 기대 익절값 = {count_익절}\n역추세+추세 매매 기대 익절값 = {count_익절 - count_손절 + count_추세매매_익절}\n------------------------")
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_숏_한계치도달(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"숏 물량 한계치 도달로 {청산물량_숏_손절}개 손절")
            break
        except:
            await asyncio.sleep(timesleep)
            continue
        
async def main_롱_한계치도달(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"롱 물량 한계치 도달로 {청산물량_롱_손절}개 손절")
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

async def main_정산_매매(): #실행시킬 함수명 임의지정   #현재 사용 안하고 있음
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"익절 = {count_익절}\n역추세 롱 보유 갯수 = {count_역추세_롱_보유갯수}\n역추세 숏 보유 갯수 = {count_역추세_숏_보유갯수}")
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
        
        count_역추세_숏_보유갯수 += 1
        asyncio.run(main_숏_매수_추적기_정산매매())
        
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
        
        if count_역추세_숏_보유갯수 >= 포지션최대보유가능갯수 - 스페어물량:
            while True :
                try:
                    청산물량_숏_손절 = (((count_역추세_숏_보유갯수 - 1) + (count_역추세_숏_보유갯수 - 청산물량)) * 청산물량)/2
                    params = {
                                'positionSide': 'SHORT'
                            }
                    exchange.create_market_buy_order(symbol, 구매갯수 * 청산물량, params)
                
                    count_역추세_숏_보유갯수 -= 청산물량
                    count_손절 += 청산물량_숏_손절
                    asyncio.run(main_숏_한계치도달)
                    
                    break
                except:
                    asyncio.run(main_손절중에러())
                    continue
      
        if count_역추세_롱_보유갯수 >= 포지션최대보유가능갯수 - 스페어물량:
            while True:
                try:
                    청산물량_롱_손절 = (((count_역추세_롱_보유갯수 - 1) + (count_역추세_롱_보유갯수 - 청산물량)) * 청산물량)/2
                    params = {
                                'positionSide': 'LONG'
                                }
                    exchange.create_market_sell_order(symbol, 구매갯수 * 청산물량, params)
                    
                    count_역추세_롱_보유갯수 -= 청산물량
                    count_손절 += 청산물량_롱_손절
                    asyncio.run(main_롱_한계치도달)
                    
                    break
                except:
                    asyncio.run(main_손절중에러())
                    continue
                
        if count_추세_숏_보유갯수 >= 추세매매익절발동물량:
            while True:
                try:
                    params = {
                                'positionSide': 'SHORT'
                                }
                    exchange.create_market_buy_order(symbol, 구매갯수 * 추세매매익절발동물량, params)
                    
                    count_추세_숏_보유갯수 -= 추세매매익절발동물량
                    count_익절 += (추세매매익절발동물량 * (추세매매익절발동물량 - 1))/2
                    asyncio.run(main_추세_숏_목표값도달)
                    
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
                    count_익절 += (추세매매익절발동물량 * (추세매매익절발동물량 - 1))/2
                    asyncio.run(main_추세_롱_목표값도달)
                    
                    break
                except:
                    asyncio.run(main_익절중에러())
                    continue
        
        # 본 매매 시작
        if symbol_price >= reference_price + 익절갭:
            while True:
                try:
                    reference_price = symbol_price
                    
                    #########################################역추세매매 방식#########################################
                    if count_역추세_숏_보유갯수 >= count_역추세_롱_보유갯수:
                        while True:
                            try:
                                params = {
                                            'positionSide': 'SHORT'
                                            }
                                exchange.create_market_sell_order(symbol, 구매갯수, params)
                                
                                count_역추세_숏_보유갯수 += 1
                                asyncio.run(main_숏_매수_추적기_정산매매())
                                                    
                                break
                            except:
                                asyncio.run(main_에러0())
                                continue
                            
                    if count_역추세_롱_보유갯수 > count_역추세_숏_보유갯수:
                        while True:
                            try:
                                params = {
                                            'positionSide': 'LONG'
                                            }
                                exchange.create_market_sell_order(symbol, 구매갯수, params)
                                
                                count_역추세_롱_보유갯수 -= 1
                                count_익절 += 1
                                asyncio.run(main_롱_매도_추적기_정산매매())
                                
                                break
                            except:
                                asyncio.run(main_에러0())
                                continue
                    ###########################################################################################
                    
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
                    
                    #########################################역추세매매 방식#########################################
                    if count_역추세_숏_보유갯수 > count_역추세_롱_보유갯수:   
                        while True:
                            try:
                                params = {
                                            'positionSide': 'SHORT'
                                            }
                                exchange.create_market_buy_order(symbol, 구매갯수, params)
                                
                                count_역추세_숏_보유갯수 -= 1
                                count_익절 += 1
                                asyncio.run(main_숏_매도_추적기_정산매매())
                                
                                break
                            except:
                                asyncio.run(main_에러0())
                                continue
                    
                    if count_역추세_롱_보유갯수 >= count_역추세_숏_보유갯수:   
                        while True:
                            try:
                                params = {
                                            'positionSide': 'LONG'
                                            }
                                exchange.create_market_buy_order(symbol, 구매갯수, params)
                                
                                count_역추세_롱_보유갯수 += 1
                                asyncio.run(main_롱_매수_추적기_정산매매())
                                
                                break
                            except:
                                asyncio.run(main_에러0())
                                continue
                    ###########################################################################################
                    
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
