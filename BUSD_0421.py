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

# 카운팅
count1_0 = 0
count1_1 = 0

count2_1 = 0

count3 = 0
count4 = 0

error1 = 0
error2 = 0

martin_count = 0

# 설정값
target_point =  0.0116          # 익절 지점
switching_point =  0.004       # 스위칭 지점
switching_ratio =  2.42        # 스위칭 배율
switching_count =  1           # 스위칭 횟수
leverage = 20                  # 레버리지
symbol = 'SOL/BUSD'            # 거래 코인
start = 0.15                   # 시작 물량 비율
martin_limit = 0               # 마틴 리밋
martin_ratio = 1               # 마틴 배율
token = ''
chat_id = ''
거래코인 = ''


async def main_시작(): #실행시킬 함수명 임의지정 
    bot = telegram.Bot(token)
    await bot.send_message(chat_id, f"수익실현 지점 = {target_point}\n스위칭 지점 = {switching_point}\n스위칭 배율 = {switching_ratio}\n스위칭 한도 = {switching_count}\n레버리지 = {leverage}\n거래코인 = {symbol}\n첫 매수물량 = {start}\n자동 매매를 시작합니다")

async def main_롱진입():
    bot = telegram.Bot(token)
    message = "롱 진입 \n진입가 : {}"
    await bot.send_message(chat_id, message.format(reference_price))

async def main_숏진입():
    bot = telegram.Bot(token)
    message = "숏 진입 \n 진입가 : {}"
    await bot.send_message(chat_id, message.format(reference_price))

async def main_롱스위칭(): #실행시킬 함수명 임의지정
    bot = telegram.Bot(token)
    message = "롱 스위칭 \n 진입가 : {}"
    await bot.send_message(chat_id, message.format(simbol_price))

async def main_숏스위칭(): #실행시킬 함수명 임의지정
    bot = telegram.Bot(token)
    message = "숏 스위칭 \n 진입가 : {}"
    await bot.send_message(chat_id, message.format(simbol_price))

async def main_n번스위칭후익절(): #실행시킬 함수명 임의지정
    bot = telegram.Bot(token)
    await bot.send_message(chat_id,"%d번 스위칭 후 익절"%(count))

async def main_n번스위칭후손절(): #실행시킬 함수명 임의지정
    bot = telegram.Bot(token)
    await bot.send_message(chat_id,"%d번 스위칭 후 손절"%(count))

async def main_에러1():       
    bot = telegram.Bot(token)
    await bot.send_message(chat_id,'에러1')

async def main_에러2(): #실행시킬 함수명 임의지정
    bot = telegram.Bot(token)
    await bot.send_message(chat_id,'에러2')

async def main_정산():
    bot = telegram.Bot(token)
    await bot.send_message(chat_id, f"익절 = {count1_0 + count1_1}\n손절 = {count2_1}")

asyncio.run(main_시작()) #봇 실행하는 코드

while True:

    if count3 > count4:

            try:
                # 초기설정 (최소거래수량 확인 필요)
                balance = exchange.fetch_balance({'type':'future'})             # 선물 계좌로 변경
                binance_balance = balance[거래코인]['free']                          # 계좌 잔고 조회
                simbol_price = exchange.fetch_ticker(symbol)['last']               # 리플 현재가 조회
                if martin_count == 0:                                           # 초기 롱 물량(거래코인 최소거래수량 이상)
                    long_amount = (binance_balance * start * leverage) / simbol_price    
                else:
                    long_amount = (binance_balance * (start * (martin_ratio ** martin_count)) * leverage) / simbol_price
                short_amount = 0                                                # 초기 숏 물량
                exchange.create_market_buy_order(symbol, long_amount)
                positions = exchange.fetch_positions([symbol], {'type': 'future'})
                reference_price = positions[0]['entryPrice']                   # 기준값 설정
                amount = positions[0]['contracts']
                count = 0
                count3 = 0
                count4 = 0

                # asyncio.run(main_롱진입())         # 초기 롱 물량 매수
            
            
            except:
                error1 += 1
                
                asyncio.run(main_에러1()) #봇 실행하는 코드
                time.sleep(10)
                continue

            while True:
                try:
                    # 비트코인 현재가 확인
                    simbol_price = exchange.fetch_ticker(symbol)['last']

                    # 숏 포지션 물량이 없고 비트코인의 현재가가 기준값의 -1%일 경우 숏 포지션 생성(롱 포지션 3배 물량)
                    if short_amount == 0 and simbol_price <= reference_price * (1 - switching_point) and count < switching_count:
                        exchange.create_market_sell_order(symbol, long_amount * switching_ratio)
                        short_amount = long_amount * switching_ratio
                        short_amount = short_amount - long_amount
                        long_amount = 0
                        count += 1
                        
                        positions = exchange.fetch_positions([symbol], {'type': 'future'})
                        amount = positions[0]['contracts']
                        reference_price = positions[0]['entryPrice'] * (1 + switching_point)
                        # asyncio.run(main_숏스위칭()) #봇 실행하는 코드

                    # 롱 포지션 물량이 없고 비트코인의 현재가가 기준값과 동일할 경우 롱 포지션 생성(숏 포지션 3배 물량)
                    elif long_amount == 0 and simbol_price >= reference_price and count < switching_count:
                        
                        exchange.create_market_buy_order(symbol, short_amount * switching_ratio)
                        long_amount = short_amount * switching_ratio
                        long_amount = long_amount - short_amount
                        short_amount = 0
                        count += 1
                        
                        positions = exchange.fetch_positions([symbol], {'type': 'future'})
                        amount = positions[0]['contracts']
                        reference_price = positions[0]['entryPrice']
                        # asyncio.run(main_롱스위칭()) #봇 실행하는 코드

                    # 숏 포지션만 존재할 경우 묙표가 지점에서 모든 포지션 정리
                    elif long_amount == 0 and short_amount > 0 and simbol_price <= reference_price * (1 - (switching_point + target_point)):
                        
                        exchange.create_market_buy_order(symbol, amount)
                        

                        count4 += 1
                        martin_count = 0

                        
                        # asyncio.run(main_n번스위칭후익절()) #봇 실행하는 코드


                        if count == 1:
                            count1_1 += 1

                        elif count == 0:
                            count1_0 += 1

                        asyncio.run(main_정산())
                        break

                    # 롱 포지션만 존재할 경우 목표가 지점에서 모든 포지션 정리
                    elif short_amount == 0 and long_amount > 0 and simbol_price >= reference_price * (1 + target_point): 
                        
                        exchange.create_market_sell_order(symbol, amount)
                        
                        count3 += 1
                        martin_count = 0

                        
                        # asyncio.run(main_n번스위칭후익절()) #봇 실행하는 코드


                        if count == 1:
                            count1_1 += 1

                        elif count == 0:
                            count1_0 += 1

                        asyncio.run(main_정산())

                        break
                        
                    # 숏 보유중 - 마지막 스위칭 후 기준값 지점에서 모든 포지션 정리
                    elif long_amount == 0 and simbol_price >= reference_price and count >= switching_count:
                        
                        exchange.create_market_buy_order(symbol, amount)
                        

                        # asyncio.run(main_n번스위칭후손절()) #봇 실행하는 코드


                        count2_1 += 1
                        count4 += 1

                        asyncio.run(main_정산())

                        if martin_count < martin_limit:
                            martin_count += 1

                        break

                    # 롱 보유중 - 마지막 스위칭 후 스위칭 지점에서 모든 포지션 정리
                    elif short_amount == 0 and simbol_price <= reference_price * (1 - switching_point) and count >= switching_count:
                        
                        exchange.create_market_buy_order(symbol, amount)
                        
                        # asyncio.run(main_n번스위칭후손절()) #봇 실행하는 코드


                        count2_1 += 1
                        count3 += 1
                        
                        asyncio.run(main_정산())

                        if martin_count < martin_limit:
                            martin_count += 1

                        break

                except:
                    error2 += 1
                   

                    asyncio.run(main_에러2()) #봇 실행하는 코드
                    time.sleep(1)
                    continue

            

    elif count3 <= count4:

            try:
                # 초기설정 (최소거래수량 확인 필요)
                balance = exchange.fetch_balance({'type':'future'})             # 선물 계좌로 변경
                binance_balance = balance[거래코인]['free']                          # 계좌 잔고 조회
                simbol_price = exchange.fetch_ticker(symbol)['last']               # 리플 현재가 조회
                long_amount = 0                                                 # 초기 롱 물량
                if martin_count == 0:                                           # 초기 숏 물량(거래코인 최소거래수량 이상)
                    short_amount = (binance_balance * start * leverage) / simbol_price    
                else:
                    short_amount = (binance_balance * (start * (martin_ratio ** martin_count)) * leverage) / simbol_price                                   
                exchange.create_market_sell_order(symbol, short_amount)
                positions = exchange.fetch_positions([symbol], {'type': 'future'})  # 보유 포지션 조회
                reference_price = positions[0]['entryPrice']                        # 기준값 설정
                amount = positions[0]['contracts']
                count = 0
                count3 = 0
                count4 = 0

                

                # asyncio.run(main_숏진입())           # 초기 숏 물량 매수
            
            except:
                error1 += 1
                
                asyncio.run(main_에러1()) #봇 실행하는 코드
                time.sleep(10)
                continue

            while True:
                try:
                    # 비트코인 현재가 확인
                    simbol_price = exchange.fetch_ticker(symbol)['last']

                    # 롱 포지션 물량이 없고 비트코인의 현재가가 기준값의 +1%일 경우 롱 포지션 생성(숏 포지션 3배 물량)
                    if long_amount == 0 and simbol_price >= reference_price * (1 + switching_point) and count < switching_count:
                        exchange.create_market_buy_order(symbol, short_amount * switching_ratio)
                        long_amount = short_amount * switching_ratio
                        long_amount = long_amount - short_amount
                        short_amount = 0
                        count += 1
                        
                        positions = exchange.fetch_positions([symbol], {'type': 'future'})
                        amount = positions[0]['contracts']
                        reference_price = positions[0]['entryPrice'] * (1 - switching_point)

                       # asyncio.run(main_롱스위칭()) #봇 실행하는 코드

                    # 숏 포지션 물량이 없고 비트코인의 현재가가 기준값과 동일할 경우 숏 포지션 생성(롱 포지션 3배 물량)
                    elif short_amount == 0 and simbol_price <= reference_price and count < switching_count:
                        exchange.create_market_sell_order(symbol, long_amount * switching_ratio)
                        short_amount = long_amount * switching_ratio
                        short_amount = short_amount - long_amount
                        long_amount = 0
                        count += 1
                        
                        positions = exchange.fetch_positions([symbol], {'type': 'future'})
                        amount = positions[0]['contracts']
                        reference_price = positions[0]['entryPrice']

                        # asyncio.run(main_숏스위칭()) #봇 실행하는 코드

                    # 롱 포지션만 존재할 경우 묙표가 지점에서 모든 포지션 정리
                    elif short_amount == 0 and long_amount > 0 and simbol_price >= reference_price * (1 + (switching_point + target_point)):
                        
                        exchange.create_market_sell_order(symbol, amount)
                        
                        count3 += 1
                        martin_count = 0

                        
                       # asyncio.run(main_n번스위칭후익절()) #봇 실행하는 코드

                        if count == 1:
                            count1_1 += 1

                        elif count == 0:
                            count1_0 += 1

                        asyncio.run(main_정산())

                        break

                    # 숏 포지션만 존재할 경우 목표가 지점에서 모든 포지션 정리
                    elif long_amount == 0 and short_amount > 0 and simbol_price <= reference_price * (1 - target_point): 
                        
                        exchange.create_market_buy_order(symbol, amount)
                        
                        count4 += 1
                        martin_count = 0

                        
                        # asyncio.run(main_n번스위칭후익절()) #봇 실행하는 코드


                        if count == 1:
                            count1_1 += 1

                        elif count == 0:
                            count1_0 += 1

                        asyncio.run(main_정산())

                        break
                        
                    # 숏 보유중 - 마지막 스위칭 후 기준값 지점에서 모든 포지션 정리
                    elif long_amount == 0 and simbol_price >= reference_price * (1 + switching_point) and count >= switching_count:
                        
                        exchange.create_market_buy_order(symbol, amount)
                        
                        
                        count4 += 1

                        

                        # asyncio.run(main_n번스위칭후손절()) #봇 실행하는 코드

                        count2_1 += 1

                        asyncio.run(main_정산())

                        if martin_count < martin_limit:
                            martin_count += 1

                        break

                    # 롱 보유중 - 마지막 스위칭 후 스위칭 지점에서 모든 포지션 정리
                    elif short_amount == 0 and simbol_price <= reference_price and count >= switching_count:
                        
                        exchange.create_market_sell_order(symbol, amount)
                        

                        count3 += 1

                        
                        # asyncio.run(main_n번스위칭후손절()) #봇 실행하는 코드

                        count2_1 += 1

                        asyncio.run(main_정산())

                        if martin_count < martin_limit:
                            martin_count += 1

                        break

                except:
                    error2 += 1
                    

                    asyncio.run(main_에러2()) #봇 실행하는 코드
                    time.sleep(1)
                    continue
