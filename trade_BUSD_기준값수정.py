import time
import ccxt
import telegram ## pip install python-telegram-bot
import asyncio
import datetime
import os
from binance.client import Client
import pandas as pd


# 현재 시간
now = datetime.datetime.now()

# 계좌 조회
api_key = 'RyrXLKBeTj4o5qQPXVelszy4x0KmuA4GLLEjf9fTG3xI5qvKSOQPEYoROtsVVq7V'
api_secret = 'iLmSAkbZaUKNJKRiIuIZtNxNSauJvKuQTlQRR8noefs3M1urBXkQYbqgLozcIRKR'

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

client = Client(api_key, api_secret)  # 포지션 조회용

# 카운팅
count_마틴 = 0
count1_0 = 0
count1_1 = 0
count1_2 = 0
count1_3 = 0
count1_4 = 0
count1_5 = 0
count1_6 = 0

count2_1 = 0

count3 = 0
count4 = 0

error1 = 0
error2 = 0

# 설정값
target_point =  0.01      # 익절 지점
switching_point =  0.007   # 스위칭 지점
switching_ratio =  3     # 스위칭 배율
switching_count =  4       # 스위칭 횟수
leverage = 3              # 레버리지
symbol = '/BUSD'        # 거래 코인
start = 0.06
token = ''
chat_id = ''
거래토큰 = ''
symbol_포지션조회용 = 'SOLBUSD'   #'BTCUSDT' 형식 # 포지션 조회용

#포지션 조회용 함수
def get_position_entry_price(symbol_포지션조회용):
    """
    입력한 심볼에 해당하는 포지션의 진입 가격을 조회하여 반환하는 함수
    :param symbol: 조회할 코인의 심볼, 예: 'BTCUSDT'
    :return: 조회된 포지션의 진입 가격
    """
    position = client.futures_position_information(symbol=symbol_포지션조회용)

    # 진입 가격 출력
    for pos in position:
        if pos['symbol'] == symbol_포지션조회용:
            entry_price = float(pos['entryPrice'])
            print(f"{symbol_포지션조회용} 포지션 진입 가격: {entry_price}")
            return entry_price

entry_price = get_position_entry_price(symbol_포지션조회용)  #포지션 조회용
###########################################################################################        
# 텔레 봇 함수 정의

async def main_시작(): #실행시킬 함수명 임의지정 
    bot = telegram.Bot(token)
    await bot.send_message(chat_id, f"수익실현 지점 = {target_point}\n스위칭 지점 = {switching_point}\n스위칭 배율 = {switching_ratio}\n스위칭 한도 = {switching_count}\n레버리지 = {leverage}\n거래코인 = {symbol}\n첫 매수물량 = {start}\n자동 매매를 시작합니다")

async def main_롱진입():
    bot = telegram.Bot(token)
    message = "롱 진입 \n margin : {} BUSD"
    await bot.send_message(chat_id, message.format(long_amount * XRP_price))

async def main_숏진입():
    bot = telegram.Bot(token)
    message = "숏 진입 \n margin : {} BUSD"
    await bot.send_message(chat_id, message.format(short_amount * XRP_price))

async def main_에러1(): #실행시킬 함수명 임의지정
    bot = telegram.Bot(token)
    await bot.send_message(chat_id,'에러1')

async def main_에러2(): #실행시킬 함수명 임의지정
    bot = telegram.Bot(token)
    await bot.send_message(chat_id,'에러2')

async def main_숏스위칭(): #실행시킬 함수명 임의지정
    bot = telegram.Bot(token)
    message = "숏 스위칭 \n margin : {} BUSD"
    await bot.send_message(chat_id, message.format(short_amount * XRP_price))

async def main_롱스위칭(): #실행시킬 함수명 임의지정
    bot = telegram.Bot(token)
    message = "롱 스위칭 \n margin : {} BUSD"
    await bot.send_message(chat_id, message.format(long_amount * XRP_price))

async def main_n번스위칭후익절(): #실행시킬 함수명 임의지정
    bot = telegram.Bot(token)
    await bot.send_message(chat_id,"%d번 스위칭 후 익절"%(count))

async def main_n번스위칭후손절(): #실행시킬 함수명 임의지정
    bot = telegram.Bot(token)
    await bot.send_message(chat_id,"%d번 스위칭 후 손절"%(count))





asyncio.run(main_시작()) #봇 실행하는 코드

while True:

    # 현재 시간
    now = datetime.datetime.now()

    if now.hour != 25:

        if count3 > count4:

                try:
                    # 초기설정 (최소거래수량 확인 필요)
                    balance = exchange.fetch_balance({'type':'future'})             # 선물 계좌로 변경
                    USDT_balance = balance[거래토큰]['free']                          # 계좌 잔고 조회
                    XRP_price = exchange.fetch_ticker(symbol)['last']               # 리플 현재가 조회
                    long_amount = (USDT_balance * start * leverage) / XRP_price    # 초기 롱 물량(거래코인 최소거래수량 이상)
                    short_amount = 0                                                # 초기 숏 물량
                    count = 0
                    count3 = 0      
                    count4 = 0                                                 # 카운팅
                    reference_price = entry_price                                     # 기준값 설정
                    exchange.create_market_buy_order(symbol, long_amount)  
                   
                    asyncio.run(main_롱진입())         # 초기 롱 물량 매수
                
                except:

                    asyncio.run(main_에러1()) #봇 실행하는 코드
                    
                    continue
                while True:
                    try:
                        # 비트코인 현재가 확인
                        XRP_price = exchange.fetch_ticker(symbol)['last']

                        # 숏 포지션 물량이 없고 비트코인의 현재가가 기준값의 -1%일 경우 숏 포지션 생성(롱 포지션 3배 물량)
                        if short_amount == 0 and XRP_price <= reference_price * (1 - switching_point) and count < switching_count:
                            short_amount = long_amount * switching_ratio
                            exchange.create_market_sell_order(symbol, short_amount)
                            short_amount = short_amount - long_amount
                            long_amount = 0
                            count += 1
                            

                            asyncio.run(main_숏스위칭()) #봇 실행하는 코드

                        # 롱 포지션 물량이 없고 비트코인의 현재가가 기준값과 동일할 경우 롱 포지션 생성(숏 포지션 3배 물량)
                        elif long_amount == 0 and XRP_price >= reference_price and count < switching_count:
                            long_amount = short_amount * switching_ratio
                            exchange.create_market_buy_order(symbol, long_amount)
                            long_amount = long_amount - short_amount
                            short_amount = 0
                            count += 1
                            

                            asyncio.run(main_롱스위칭()) #봇 실행하는 코드

                        # 숏 포지션만 존재할 경우 묙표가 지점에서 모든 포지션 정리
                        elif long_amount == 0 and short_amount > 0 and XRP_price <= reference_price * (1 - (switching_point + target_point)):
                            exchange.create_market_buy_order(symbol, short_amount)
                            

                            count4 += 1

                            asyncio.run(main_n번스위칭후익절()) #봇 실행하는 코드

                            count_마틴 = 0

                            break

                        # 롱 포지션만 존재할 경우 목표가 지점에서 모든 포지션 정리
                        elif short_amount == 0 and long_amount > 0 and XRP_price >= reference_price * (1 + target_point): 
                            exchange.create_market_sell_order(symbol, long_amount)
                            

                            count3 += 1

                            asyncio.run(main_n번스위칭후익절()) #봇 실행하는 코드

                            count_마틴 = 0
              
                            break
                            
                        # 숏 보유중 - 마지막 스위칭 후 기준값 지점에서 모든 포지션 정리
                        elif long_amount == 0 and XRP_price >= reference_price and count >= switching_count:
                            exchange.create_market_buy_order(symbol, short_amount)
                            

                            asyncio.run(main_n번스위칭후손절()) #봇 실행하는 코드

                            
                            count3 += 1

                            count_마틴 += 1

                            break

                        # 롱 보유중 - 마지막 스위칭 후 스위칭 지점에서 모든 포지션 정리
                        elif short_amount == 0 and XRP_price <= reference_price * (1 - switching_point) and count >= switching_count:
                            exchange.create_market_sell_order(symbol, long_amount)
                            

                            
                            asyncio.run(main_n번스위칭후손절()) #봇 실행하는 코드

                            count_마틴 += 1

                            count4 += 1
                            break

                    except:

                        asyncio.run(main_에러2()) #봇 실행하는 코드

                        continue

        elif count3 <= count4:

                try:
                    # 초기설정 (최소거래수량 확인 필요)
                    balance = exchange.fetch_balance({'type':'future'})             # 선물 계좌로 변경
                    USDT_balance = balance[거래토큰]['free']                          # 계좌 잔고 조회
                    XRP_price = exchange.fetch_ticker(symbol)['last']               # 리플 현재가 조회
                    long_amount = 0                                                 # 초기 롱 물량(거래코인 최소거래수량 이상)
                    short_amount = (USDT_balance * start * leverage) / XRP_price    # 초기 숏 물량
                    count = 0 
                    count3 = 0
                    count4 = 0                                                       # 카운팅
                    reference_price = entry_price                                     # 기준값 설정
                    exchange.create_market_sell_order(symbol, short_amount)

                    asyncio.run(main_숏진입())           # 초기 숏 물량 매수
                
                except:
                    asyncio.run(main_에러1()) #봇 실행하는 코드
                    
                    continue
                while True:
                    try:
                        # 비트코인 현재가 확인
                        XRP_price = exchange.fetch_ticker(symbol)['last']

                        # 롱 포지션 물량이 없고 비트코인의 현재가가 기준값의 +1%일 경우 롱 포지션 생성(숏 포지션 3배 물량)
                        if long_amount == 0 and XRP_price >= reference_price * (1 + switching_point) and count < switching_count:
                            long_amount = short_amount * switching_ratio
                            exchange.create_market_buy_order(symbol, long_amount)
                            long_amount = long_amount - short_amount
                            short_amount = 0
                            count += 1
                            

                            asyncio.run(main_롱스위칭()) #봇 실행하는 코드

                        # 숏 포지션 물량이 없고 비트코인의 현재가가 기준값과 동일할 경우 숏 포지션 생성(롱 포지션 3배 물량)
                        elif short_amount == 0 and XRP_price <= reference_price and count < switching_count:
                            short_amount = long_amount * switching_ratio
                            exchange.create_market_sell_order(symbol, short_amount)
                            short_amount = short_amount - long_amount
                            long_amount = 0
                            count += 1
                           

                            asyncio.run(main_숏스위칭()) #봇 실행하는 코드

                        # 롱 포지션만 존재할 경우 묙표가 지점에서 모든 포지션 정리
                        elif short_amount == 0 and long_amount > 0 and XRP_price >= reference_price * (1 + (switching_point + target_point)):
                            exchange.create_market_sell_order(symbol, long_amount)
                            

                            count3 += 1

                            
                            asyncio.run(main_n번스위칭후익절()) #봇 실행하는 코드

                            
                            break

                        # 숏 포지션만 존재할 경우 목표가 지점에서 모든 포지션 정리
                        elif long_amount == 0 and short_amount > 0 and XRP_price <= reference_price * (1 - target_point): 
                            exchange.create_market_buy_order(symbol, short_amount)
                            

                            count4 += 1

                            
                            asyncio.run(main_n번스위칭후익절()) #봇 실행하는 코드

                            
                            break
                            
                        # 숏 보유중 - 마지막 스위칭 후 기준값 지점에서 모든 포지션 정리
                        elif long_amount == 0 and XRP_price >= reference_price * (1 + switching_point) and count >= switching_count:
                            exchange.create_market_buy_order(symbol, short_amount)
                            
                            
                            count3 += 1

                            

                            asyncio.run(main_n번스위칭후손절()) #봇 실행하는 코드

                            count2_1 += 1
                            break

                        # 롱 보유중 - 마지막 스위칭 후 스위칭 지점에서 모든 포지션 정리
                        elif short_amount == 0 and XRP_price <= reference_price and count >= switching_count:
                            exchange.create_market_sell_order(symbol, long_amount)
                            

                            count4 += 1

                            
                            asyncio.run(main_n번스위칭후손절()) #봇 실행하는 코드

                            count2_1 += 1
                            break

                    except:
                        asyncio.run(main_에러2()) #봇 실행하는 코드

                        continue


    else:
        os.system('cls')
        time.sleep(60)
