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
count1_0 = 0  # 익절 카운트
count1_1 = 0  # 익절 카운트
count2_1 = 0  # 손절 카운트

count3 = 0
count4 = 0

martin_count = 0

ikson_list = []

# 설정값
target_point =  0.0172         # 익절 지점
switching_point =  0.006       # 스위칭 지점
switching_ratio =  2.42        # 스위칭 배율
switching_count =  1           # 스위칭 횟수
leverage = 20                  # 레버리지
start = 0.153                  # 시작 물량 비율
timesleep = 0.1                # 대기시간
ikson_range = 10               # 데이터 수집 범위

symbol = 'TOMO/USDT'            # 거래 코인
stablecoin = 'USDT'            # 스테이블코인

martin_limit = 0               # 마틴 리밋
martin_ratio = 1               # 마틴 배율

ikson_start = 8             # 시작 익절 카운트
ikson_stop = 6              # 정지 익절 카운트

token = '6199814629:AAEe6VU6PJdbPaa8JrQQhHm-DFRfGkhyqHI'
chat_id = '6012236354'

async def main_시작():
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"수익실현 지점 = {target_point}\n스위칭 지점 = {switching_point}\n스위칭 배율 = {switching_ratio}\n스위칭 한도 = {switching_count}\n레버리지 = {leverage}\n거래코인 = {symbol}\n첫 매수물량 = {start}\n시작 익절 카운트 = {ikson_start}\n종료 익절 카운트 = {ikson_stop}\n자동 매매를 시작합니다")
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
            continue

async def main_정산_데이터갱신(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"{ikson_list.count(1)}/{ikson_list.count(0)} 데이터 갱신\n{ikson_list}")
            break
        except:
            await asyncio.sleep(timesleep)
            continue

async def main_정산_매매(): #실행시킬 함수명 임의지정
    while True:
        try:
            bot = telegram.Bot(token)
            await bot.send_message(chat_id, f"{count1_0 + count1_1}/{count2_1} 매매\n{ikson_list.count(1)}/{ikson_list.count(0)} 데이터 갱신\n{ikson_list}")
            break
        except:
            await asyncio.sleep(timesleep)
            continue

asyncio.run(main_시작())


while True:
    if len(ikson_list) < ikson_range:  # 초기 데이터 수집
        if count3 >= count4: # 롱스타트
            while True:
                try:
                    # 초기설정 (최소거래수량 확인 필요)
                    balance = exchange.fetch_balance({'type':'future'})             # 선물 계좌로 변경
                    binance_balance = balance[stablecoin]['free']                           # 계좌 잔고 조회
                    symbol_price = exchange.fetch_ticker(symbol)['last']               # 리플 현재가 조회
                    long_amount = (binance_balance * start * leverage) / symbol_price    # 초기 롱 물량(거래코인 최소거래수량 이상)
                    short_amount = 0                                                # 초기 숏 물량
                    count = 0
                    count3 = 0      
                    count4 = 0                                                 # 카운팅
                    reference_price = symbol_price                                     # 기준값 설정
                    break
                except:
                    print("에러1")
                    asyncio.run(main_에러1()) #봇 실행하는 코드

            while True:
                try:
                    # 비트코인 현재가 확인
                    symbol_price = exchange.fetch_ticker(symbol)['last']
                    time.sleep(timesleep)

                    # 롱스타트 숏 스위칭
                    if short_amount == 0 and symbol_price <= reference_price * (1 - switching_point) and count < switching_count:
                        short_amount = long_amount * switching_ratio
                        short_amount = short_amount - long_amount
                        long_amount = 0
                        count += 1

                    # 롱스타트 롱 스위칭
                    elif long_amount == 0 and symbol_price >= reference_price and count < switching_count:
                        long_amount = short_amount * switching_ratio
                        long_amount = long_amount - short_amount
                        short_amount = 0
                        count += 1

                    # 롱스타트 익절
                    elif long_amount == 0 and short_amount > 0 and symbol_price <= reference_price * (1 - (switching_point + target_point)):
                        count4 += 1
                        if count == 1:
                            count1_1 += 1
                        elif count == 0:
                            count1_0 += 1
                        ikson_list.insert(0,1)
                        if len(ikson_list) > ikson_range:
                            del ikson_list[ikson_range:]
                        break

                    # 롱스타트 익절
                    elif short_amount == 0 and long_amount > 0 and symbol_price >= reference_price * (1 + target_point): 
                        count3 += 1
                        if count == 1:
                            count1_1 += 1
                        elif count == 0:
                            count1_0 += 1
                        ikson_list.insert(0,1)
                        if len(ikson_list) > ikson_range:
                            del ikson_list[ikson_range:]
                        break
                        
                    # 롱스타트 손절
                    elif long_amount == 0 and symbol_price >= reference_price and count >= switching_count:
                        count2_1 += 1
                        count3 += 1
                        ikson_list.insert(0,0)
                        if len(ikson_list) > ikson_range:
                            del ikson_list[ikson_range:]
                        break

                    # 롱스타트 손절
                    elif short_amount == 0 and symbol_price <= reference_price * (1 - switching_point) and count >= switching_count:
                        count2_1 += 1
                        count4 += 1
                        ikson_list.insert(0,0)
                        if len(ikson_list) > ikson_range:
                            del ikson_list[ikson_range:]
                        break

                except:
                    print("에러2")
                    asyncio.run(main_에러2()) #봇 실행하는 코드
                    continue

            asyncio.run(main_정산_데이터갱신())

        elif count3 < count4: # 숏스타트
            while True:
                try:
                    # 초기설정 (최소거래수량 확인 필요)
                    balance = exchange.fetch_balance({'type':'future'})             # 선물 계좌로 변경
                    binance_balance = balance[stablecoin]['free']                          # 계좌 잔고 조회
                    symbol_price = exchange.fetch_ticker(symbol)['last']               # 리플 현재가 조회
                    long_amount = 0                                                 # 초기 롱 물량(거래코인 최소거래수량 이상)
                    short_amount = (binance_balance * start * leverage) / symbol_price    # 초기 숏 물량
                    count = 0 
                    count3 = 0
                    count4 = 0                                                       # 카운팅
                    reference_price = symbol_price                                     # 기준값 설정
                    break
                except:
                    print("에러1")
                    asyncio.run(main_에러1()) #봇 실행하는 코드

            while True:
                try:
                    # 비트코인 현재가 확인
                    symbol_price = exchange.fetch_ticker(symbol)['last']
                    time.sleep(timesleep)

                    # 숏스타트 롱스위칭
                    if long_amount == 0 and symbol_price >= reference_price * (1 + switching_point) and count < switching_count:
                        long_amount = short_amount * switching_ratio
                        long_amount = long_amount - short_amount
                        short_amount = 0
                        count += 1

                    # 숏스타트 숏스위칭
                    elif short_amount == 0 and symbol_price <= reference_price and count < switching_count:
                        short_amount = long_amount * switching_ratio
                        short_amount = short_amount - long_amount
                        long_amount = 0
                        count += 1

                    # 숏스타트 익절
                    elif short_amount == 0 and long_amount > 0 and symbol_price >= reference_price * (1 + (switching_point + target_point)):
                        count3 += 1
                        if count == 1:
                            count1_1 += 1
                        elif count == 0:
                            count1_0 += 1
                        ikson_list.insert(0,1)
                        if len(ikson_list) > ikson_range:
                            del ikson_list[ikson_range:]
                        break

                    # 숏스타트 익절
                    elif long_amount == 0 and short_amount > 0 and symbol_price <= reference_price * (1 - target_point): 
                        count4 += 1
                        if count == 1:
                            count1_1 += 1
                        elif count == 0:
                            count1_0 += 1
                        ikson_list.insert(0,1)
                        if len(ikson_list) > ikson_range:
                            del ikson_list[ikson_range:]
                        break
                        
                    # 숏스타트 손절
                    elif long_amount == 0 and symbol_price >= reference_price * (1 + switching_point) and count >= switching_count:
                        count3 += 1
                        count2_1 += 1
                        ikson_list.insert(0,0)
                        if len(ikson_list) > ikson_range:
                            del ikson_list[ikson_range:]
                        break

                    # 숏스타트 손절
                    elif short_amount == 0 and symbol_price <= reference_price and count >= switching_count:
                        count4 += 1
                        count2_1 += 1
                        ikson_list.insert(0,0)
                        if len(ikson_list) > ikson_range:
                            del ikson_list[ikson_range:]
                        break

                except:
                    print("에러2")
                    asyncio.run(main_에러2()) #봇 실행하는 코드
                    continue

            asyncio.run(main_정산_데이터갱신())

    elif len(ikson_list) >= ikson_range:   # 초기 데이터 수집 이후
        if ikson_list.count(1) != ikson_start: # 손익비 갱신
            while True:
                if count3 >= count4: # 롱스타트
                    while True:
                        try:
                            # 초기설정 (최소거래수량 확인 필요)
                            balance = exchange.fetch_balance({'type':'future'})             # 선물 계좌로 변경
                            binance_balance = balance[stablecoin]['free']                           # 계좌 잔고 조회
                            symbol_price = exchange.fetch_ticker(symbol)['last']               # 리플 현재가 조회
                            long_amount = (binance_balance * start * leverage) / symbol_price    # 초기 롱 물량(거래코인 최소거래수량 이상)
                            short_amount = 0                                                # 초기 숏 물량
                            count = 0
                            count3 = 0      
                            count4 = 0                                                 # 카운팅
                            reference_price = symbol_price                                     # 기준값 설정
                            break
                        except:
                            print("에러1")
                            asyncio.run(main_에러1()) #봇 실행하는 코드
                            continue
    
                    while True:
                        try:
                            # 비트코인 현재가 확인
                            symbol_price = exchange.fetch_ticker(symbol)['last']
                            time.sleep(timesleep)
    
                            # 롱스타트 숏 스위칭
                            if short_amount == 0 and symbol_price <= reference_price * (1 - switching_point) and count < switching_count:
                                short_amount = long_amount * switching_ratio
                                short_amount = short_amount - long_amount
                                long_amount = 0
                                count += 1
    
                            # 롱스타트 롱 스위칭
                            elif long_amount == 0 and symbol_price >= reference_price and count < switching_count:
                                long_amount = short_amount * switching_ratio
                                long_amount = long_amount - short_amount
                                short_amount = 0
                                count += 1
    
                            # 롱스타트 익절
                            elif long_amount == 0 and short_amount > 0 and symbol_price <= reference_price * (1 - (switching_point + target_point)):
                                count4 += 1
                                if count == 1:
                                    count1_1 += 1
                                elif count == 0:
                                    count1_0 += 1
                                ikson_list.insert(0,1)
                                if len(ikson_list) > ikson_range:
                                    del ikson_list[ikson_range:]
                                break
    
                            # 롱스타트 익절
                            elif short_amount == 0 and long_amount > 0 and symbol_price >= reference_price * (1 + target_point): 
                                count3 += 1
                                if count == 1:
                                    count1_1 += 1
                                elif count == 0:
                                    count1_0 += 1
                                ikson_list.insert(0,1)
                                if len(ikson_list) > ikson_range:
                                    del ikson_list[ikson_range:]
                                break
                                
                            # 롱스타트 손절
                            elif long_amount == 0 and symbol_price >= reference_price and count >= switching_count:
                                count2_1 += 1
                                count3 += 1
                                ikson_list.insert(0,0)
                                if len(ikson_list) > ikson_range:
                                    del ikson_list[ikson_range:]
                                break
    
                            # 롱스타트 손절
                            elif short_amount == 0 and symbol_price <= reference_price * (1 - switching_point) and count >= switching_count:
                                count2_1 += 1
                                count4 += 1
                                ikson_list.insert(0,0)
                                if len(ikson_list) > ikson_range:
                                    del ikson_list[ikson_range:]
                                break
    
                        except:
                            print("에러2")
                            asyncio.run(main_에러2()) #봇 실행하는 코드
                            continue
    
                    asyncio.run(main_정산_데이터갱신())
    
                    if ikson_list.count(1) == ikson_start:
                        break
    
                elif count3 < count4: # 숏스타트
                    while True:
                        try:
                            # 초기설정 (최소거래수량 확인 필요)
                            balance = exchange.fetch_balance({'type':'future'})             # 선물 계좌로 변경
                            binance_balance = balance[stablecoin]['free']                          # 계좌 잔고 조회
                            symbol_price = exchange.fetch_ticker(symbol)['last']               # 리플 현재가 조회
                            long_amount = 0                                                 # 초기 롱 물량(거래코인 최소거래수량 이상)
                            short_amount = (binance_balance * start * leverage) / symbol_price    # 초기 숏 물량
                            count = 0 
                            count3 = 0
                            count4 = 0                                                       # 카운팅
                            reference_price = symbol_price                                     # 기준값 설정
                            break
                        except:
                            print("에러1")
                            asyncio.run(main_에러1()) #봇 실행하는 코드
    
                    while True:
                        try:
                            # 비트코인 현재가 확인
                            symbol_price = exchange.fetch_ticker(symbol)['last']
                            time.sleep(timesleep)
    
                            # 숏스타트 롱스위칭
                            if long_amount == 0 and symbol_price >= reference_price * (1 + switching_point) and count < switching_count:
                                long_amount = short_amount * switching_ratio
                                long_amount = long_amount - short_amount
                                short_amount = 0
                                count += 1
    
                            # 숏스타트 숏스위칭
                            elif short_amount == 0 and symbol_price <= reference_price and count < switching_count:
                                short_amount = long_amount * switching_ratio
                                short_amount = short_amount - long_amount
                                long_amount = 0
                                count += 1
    
                            # 숏스타트 익절
                            elif short_amount == 0 and long_amount > 0 and symbol_price >= reference_price * (1 + (switching_point + target_point)):
                                count3 += 1
                                if count == 1:
                                    count1_1 += 1
                                elif count == 0:
                                    count1_0 += 1
                                ikson_list.insert(0,1)
                                if len(ikson_list) > ikson_range:
                                    del ikson_list[ikson_range:]
                                break
    
                            # 숏스타트 익절
                            elif long_amount == 0 and short_amount > 0 and symbol_price <= reference_price * (1 - target_point): 
                                count4 += 1
                                if count == 1:
                                    count1_1 += 1
                                elif count == 0:
                                    count1_0 += 1
                                ikson_list.insert(0,1)
                                if len(ikson_list) > ikson_range:
                                    del ikson_list[ikson_range:]
                                break
                                
                            # 숏스타트 손절
                            elif long_amount == 0 and symbol_price >= reference_price * (1 + switching_point) and count >= switching_count:
                                count3 += 1
                                count2_1 += 1
                                ikson_list.insert(0,0)
                                if len(ikson_list) > ikson_range:
                                    del ikson_list[ikson_range:]
                                break
    
                            # 숏스타트 손절
                            elif short_amount == 0 and symbol_price <= reference_price and count >= switching_count:
                                count4 += 1
                                count2_1 += 1
                                ikson_list.insert(0,0)
                                if len(ikson_list) > ikson_range:
                                    del ikson_list[ikson_range:]
                                break
    
                        except:
                            print("에러2")
                            asyncio.run(main_에러2()) #봇 실행하는 코드
                            continue
    
                    asyncio.run(main_정산_데이터갱신())
    
                    if ikson_list.count(1) == ikson_start:
                        break

        elif ikson_list.count(1) == ikson_start: # 매매 시작
            while True:
                try:
                    count1_0 = 0
                    count1_1 = 0
                    count2_1 = 0
                    break
                except:
                    asyncio.run(main_에러0())
                    continue
            while True:
                try:
                    if count3 >= count4:
                        while True:
                            try:
                                # 초기설정 (최소거래수량 확인 필요)
                                balance = exchange.fetch_balance({'type':'future'})             # 선물 계좌로 변경
                                binance_balance = balance[stablecoin]['free']                          # 계좌 잔고 조회
                                symbol_price = exchange.fetch_ticker(symbol)['last']               # 리플 현재가 조회
                                if martin_count == 0:                                           # 초기 롱 물량(거래코인 최소거래수량 이상)
                                    long_amount = (binance_balance * start * leverage) / symbol_price    
                                else:
                                    long_amount = (binance_balance * (start * (martin_ratio ** martin_count)) * leverage) / symbol_price
                                short_amount = 0                                                # 초기 숏 물량
                                exchange.create_market_buy_order(symbol, long_amount)
                                while True:
                                    try:
                                        positions = exchange.fetch_positions([symbol], {'type': 'future'})
                                        reference_price = positions[0]['entryPrice']                   # 기준값 설정
                                        amount = positions[0]['contracts']
                                        break
                                    except:
                                        continue
                                count = 0
                                count3 = 0
                                count4 = 0
                                break
                            except:
                                print("에러1")
                                asyncio.run(main_에러1()) #봇 실행하는 코드
                                continue

                        while True:
                            try:
                                # 비트코인 현재가 확인
                                symbol_price = exchange.fetch_ticker(symbol)['last']
                                time.sleep(timesleep)

                                # 롱스타트 숏스위칭
                                if short_amount == 0 and symbol_price <= reference_price * (1 - switching_point) and count < switching_count:
                                    exchange.create_market_sell_order(symbol, long_amount * switching_ratio)
                                    short_amount = long_amount * switching_ratio
                                    short_amount = short_amount - long_amount
                                    long_amount = 0
                                    count += 1
                                    while True:
                                        try:
                                            positions = exchange.fetch_positions([symbol], {'type': 'future'})
                                            amount = positions[0]['contracts']
                                            reference_price = positions[0]['entryPrice'] * (1 + switching_point)
                                            break
                                        except:
                                            print("에러3")
                                            asyncio.run(main_에러3()) #봇 실행하는 코드
                                            continue
                                    print("숏 스위칭")

                                # 롱스타트 롱스위칭
                                elif long_amount == 0 and symbol_price >= reference_price and count < switching_count:
                                    exchange.create_market_buy_order(symbol, short_amount * switching_ratio)
                                    long_amount = short_amount * switching_ratio
                                    long_amount = long_amount - short_amount
                                    short_amount = 0
                                    count += 1
                                    while True:
                                        try:
                                            positions = exchange.fetch_positions([symbol], {'type': 'future'})
                                            amount = positions[0]['contracts']
                                            reference_price = positions[0]['entryPrice']
                                            break
                                        except:
                                            print("에러3")
                                            asyncio.run(main_에러3()) #봇 실행하는 코드
                                            continue
                                    print("롱 스위칭")

                                # 롱스타트 익절
                                elif long_amount == 0 and short_amount > 0 and symbol_price <= reference_price * (1 - (switching_point + target_point)):
                                    exchange.create_market_buy_order(symbol, amount)
                                    print("%d번 스위칭 후 익절"%(count))
                                    count4 += 1
                                    martin_count = 0
                                    if count == 1:
                                        count1_1 += 1
                                    elif count == 0:
                                        count1_0 += 1
                                    ikson_list.insert(0,1)
                                    if len(ikson_list) > ikson_range:
                                        del ikson_list[ikson_range:]
                                    break

                                # 롱스타트 익절
                                elif short_amount == 0 and long_amount > 0 and symbol_price >= reference_price * (1 + target_point): 
                                    exchange.create_market_sell_order(symbol, amount)
                                    print("%d번 스위칭 후 익절"%(count))
                                    count3 += 1
                                    martin_count = 0
                                    if count == 1:
                                        count1_1 += 1
                                    elif count == 0:
                                        count1_0 += 1
                                    ikson_list.insert(0,1)
                                    if len(ikson_list) > ikson_range:
                                        del ikson_list[ikson_range:]
                                    break
                                    
                                # 롱스타트 손절
                                elif long_amount == 0 and symbol_price >= reference_price and count >= switching_count:
                                    exchange.create_market_buy_order(symbol, amount)
                                    print("%d번 스위칭 후 손절"%(count))
                                    count2_1 += 1
                                    count3 += 1
                                    if martin_count < martin_limit:
                                        martin_count += 1
                                    ikson_list.insert(0,0)
                                    if len(ikson_list) > ikson_range:
                                        del ikson_list[ikson_range:]
                                    break

                                # 롱스타트 손절
                                elif short_amount == 0 and symbol_price <= reference_price * (1 - switching_point) and count >= switching_count:
                                    exchange.create_market_buy_order(symbol, amount)
                                    print("%d번 스위칭 후 손절"%(count))
                                    count2_1 += 1
                                    count4 += 1
                                    if martin_count < martin_limit:
                                        martin_count += 1
                                    ikson_list.insert(0,0)
                                    if len(ikson_list) > ikson_range:
                                        del ikson_list[ikson_range:]
                                    break

                            except:
                                print("에러2")
                                asyncio.run(main_에러2()) #봇 실행하는 코드
                                continue

                        asyncio.run(main_정산_매매())

                        if ikson_list.count(1) == ikson_stop:
                            break

                    elif count3 < count4:
                        while True:
                            try:
                                # 초기설정 (최소거래수량 확인 필요)
                                balance = exchange.fetch_balance({'type':'future'})             # 선물 계좌로 변경
                                binance_balance = balance[stablecoin]['free']                          # 계좌 잔고 조회
                                symbol_price = exchange.fetch_ticker(symbol)['last']               # 리플 현재가 조회
                                long_amount = 0                                                 # 초기 롱 물량
                                if martin_count == 0:                                           # 초기 숏 물량(거래코인 최소거래수량 이상)
                                    short_amount = (binance_balance * start * leverage) / symbol_price    
                                else:
                                    short_amount = (binance_balance * (start * (martin_ratio ** martin_count)) * leverage) / symbol_price                                   
                                exchange.create_market_sell_order(symbol, short_amount)
                                while True:
                                    try:
                                        positions = exchange.fetch_positions([symbol], {'type': 'future'})
                                        reference_price = positions[0]['entryPrice']                   # 기준값 설정
                                        amount = positions[0]['contracts']
                                        break
                                    except:
                                        continue
                                count = 0
                                count3 = 0
                                count4 = 0
                                break
                            except:
                                print("에러1")
                                asyncio.run(main_에러1()) #봇 실행하는 코드
                                continue

                        while True:
                            try:
                                # 비트코인 현재가 확인
                                symbol_price = exchange.fetch_ticker(symbol)['last']
                                time.sleep(timesleep)

                                # 숏스타트 숏스위칭
                                if long_amount == 0 and symbol_price >= reference_price * (1 + switching_point) and count < switching_count:
                                    exchange.create_market_buy_order(symbol, short_amount * switching_ratio)
                                    long_amount = short_amount * switching_ratio
                                    long_amount = long_amount - short_amount
                                    short_amount = 0
                                    count += 1
                                    while True:
                                        try:
                                            positions = exchange.fetch_positions([symbol], {'type': 'future'})
                                            amount = positions[0]['contracts']
                                            reference_price = positions[0]['entryPrice'] * (1 - switching_point)
                                            break
                                        except:
                                            print("에러3")
                                            asyncio.run(main_에러3()) #봇 실행하는 코드
                                            continue
                                    print("롱 스위칭")


                                # 숏스타트 롱스위칭
                                elif short_amount == 0 and symbol_price <= reference_price and count < switching_count:
                                    exchange.create_market_sell_order(symbol, long_amount * switching_ratio)
                                    short_amount = long_amount * switching_ratio
                                    short_amount = short_amount - long_amount
                                    long_amount = 0
                                    count += 1
                                    while True:
                                        try:
                                            positions = exchange.fetch_positions([symbol], {'type': 'future'})
                                            amount = positions[0]['contracts']
                                            reference_price = positions[0]['entryPrice'] * (1 - switching_point)
                                            break
                                        except:
                                            print("에러3")
                                            asyncio.run(main_에러3()) #봇 실행하는 코드
                                            continue
                                    print("숏 스위칭")

                                # 숏스타트 익절
                                elif short_amount == 0 and long_amount > 0 and symbol_price >= reference_price * (1 + (switching_point + target_point)):
                                    exchange.create_market_sell_order(symbol, amount)
                                    print("%d번 스위칭 후 익절"%(count))
                                    count3 += 1
                                    martin_count = 0
                                    if count == 1:
                                        count1_1 += 1
                                    elif count == 0:
                                        count1_0 += 1
                                    ikson_list.insert(0,1)
                                    if len(ikson_list) > ikson_range:
                                        del ikson_list[ikson_range:]
                                    break

                                # 숏스타트 익절
                                elif long_amount == 0 and short_amount > 0 and symbol_price <= reference_price * (1 - target_point): 
                                    exchange.create_market_buy_order(symbol, amount)
                                    print("%d번 스위칭 후 익절"%(count))
                                    count4 += 1
                                    martin_count = 0
                                    if count == 1:
                                        count1_1 += 1
                                    elif count == 0:
                                        count1_0 += 1
                                    ikson_list.insert(0,1)
                                    if len(ikson_list) > ikson_range:
                                        del ikson_list[ikson_range:]
                                    break
                                    
                                # 숏스타트 손절
                                elif long_amount == 0 and symbol_price >= reference_price * (1 + switching_point) and count >= switching_count:
                                    exchange.create_market_buy_order(symbol, amount)
                                    print("%d번 스위칭 후 손절"%(count))
                                    count3 += 1
                                    count2_1 += 1
                                    if martin_count < martin_limit:
                                        martin_count += 1
                                    ikson_list.insert(0,0)
                                    if len(ikson_list) > ikson_range:
                                        del ikson_list[ikson_range:]
                                    break

                                # 숏스타트 손절
                                elif short_amount == 0 and symbol_price <= reference_price and count >= switching_count:
                                    exchange.create_market_sell_order(symbol, amount)
                                    print("%d번 스위칭 후 손절"%(count))
                                    count4 += 1
                                    count2_1 += 1
                                    if martin_count < martin_limit:
                                        martin_count += 1
                                    ikson_list.insert(0,0)
                                    if len(ikson_list) > ikson_range:
                                        del ikson_list[ikson_range:]
                                    break

                            except:
                                print("에러2")
                                asyncio.run(main_에러2()) #봇 실행하는 코드
                                continue

                        asyncio.run(main_정산_매매())
                        if ikson_list.count(1) == ikson_stop:
                            break
                except:
                    asyncio.run(main_에러0()) #봇 실행하는 코드
                    continue
