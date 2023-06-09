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
target_point =  0.0063      # 익절 지점
switching_point =  0.0015   # 스위칭 지점
switching_ratio =  2.42     # 스위칭 배율
switching_count =  1       # 스위칭 횟수
leverage = 20              # 레버리지
symbol = 'EDU/USDT'        # 거래 코인
start = 0.1
token = ''
chat_id = ''


async def main_시작(): #실행시킬 함수명 임의지정 
    bot = telegram.Bot(token)
    await bot.send_message(chat_id, f"수익실현 지점 = {target_point}\n스위칭 지점 = {switching_point}\n스위칭 배율 = {switching_ratio}\n스위칭 한도 = {switching_count}\n레버리지 = {leverage}\n거래코인 = {symbol}\n첫 매수물량 = {start}\n자동 매매를 시작합니다")

asyncio.run(main_시작()) #봇 실행하는 코드

while True:
    
    now = datetime.datetime.now()  # 현재 시간 조회

    if now.hour !=25:

        if count3 > count4:

                try:
                    # 초기설정 (최소거래수량 확인 필요)
                    balance = exchange.fetch_balance({'type':'future'})             # 선물 계좌로 변경
                    USDT_balance = 500000                                         # 계좌 잔고 조회
                    XRP_price = exchange.fetch_ticker(symbol)['last']               # 리플 현재가 조회
                    long_amount = (USDT_balance * start * leverage) / XRP_price    # 초기 롱 물량(거래코인 최소거래수량 이상)
                    short_amount = 0                                                # 초기 숏 물량
                    count = 0
                    count3 = 0      
                    count4 = 0                                                 # 카운팅
                    reference_price = XRP_price                                     # 기준값 설정
                
                except:
                    error1 += 1
                    print("에러1")

                    async def main_에러1(): #실행시킬 함수명 임의지정
                        
                        bot = telegram.Bot(token)
                        await bot.send_message(chat_id,'에러1')

                    asyncio.run(main_에러1()) #봇 실행하는 코드

                while True:
                    try:
                        # 비트코인 현재가 확인
                        XRP_price = exchange.fetch_ticker(symbol)['last']

                        # 숏 포지션 물량이 없고 비트코인의 현재가가 기준값의 -1%일 경우 숏 포지션 생성(롱 포지션 3배 물량)
                        if short_amount == 0 and XRP_price <= reference_price * (1 - switching_point) and count < switching_count:
                            short_amount = long_amount * switching_ratio
                            
                            short_amount = short_amount - long_amount
                            long_amount = 0
                            count += 1

                        # 롱 포지션 물량이 없고 비트코인의 현재가가 기준값과 동일할 경우 롱 포지션 생성(숏 포지션 3배 물량)
                        elif long_amount == 0 and XRP_price >= reference_price and count < switching_count:
                            long_amount = short_amount * switching_ratio
                            
                            long_amount = long_amount - short_amount
                            short_amount = 0
                            count += 1

                        # 숏 포지션만 존재할 경우 묙표가 지점에서 모든 포지션 정리
                        elif long_amount == 0 and short_amount > 0 and XRP_price <= reference_price * (1 - (switching_point + target_point)):

                            count4 += 1

                            if count == 1:
                                count1_1 += 1

                            elif count == 2:
                                count1_2 += 1

                            elif count == 3:
                                count1_3 += 1

                            elif count == 4:
                                count1_4 += 1

                            elif count == 5:
                                count1_5 += 1

                            elif count == 6:
                                count1_6 += 1

                            elif count == 0:
                                count1_0 += 1

                            break

                        # 롱 포지션만 존재할 경우 목표가 지점에서 모든 포지션 정리
                        elif short_amount == 0 and long_amount > 0 and XRP_price >= reference_price * (1 + target_point): 

                            count3 += 1

                            if count == 1:
                                count1_1 += 1

                            elif count == 2:
                                count1_2 += 1

                            elif count == 3:
                                count1_3 += 1

                            elif count == 4:
                                count1_4 += 1

                            elif count == 5:
                                count1_5 += 1

                            elif count == 6:
                                count1_6 += 1

                            elif count == 0:
                                count1_0 += 1

                            break
                            
                        # 숏 보유중 - 마지막 스위칭 후 기준값 지점에서 모든 포지션 정리
                        elif long_amount == 0 and XRP_price >= reference_price and count >= switching_count:

                            count2_1 += 1
                            count3 += 1
                            break

                        # 롱 보유중 - 마지막 스위칭 후 스위칭 지점에서 모든 포지션 정리
                        elif short_amount == 0 and XRP_price <= reference_price * (1 - switching_point) and count >= switching_count:

                            count2_1 += 1
                            count4 += 1
                            break

                    except:
                        error2 += 1
                        print("에러2")

                        async def main_에러2(): #실행시킬 함수명 임의지정
                            bot = telegram.Bot(token)
                            await bot.send_message(chat_id,'에러2')

                        # asyncio.run(main_에러2()) #봇 실행하는 코드

                        continue

                print("----------------------")
                print("0번 스위칭 후 익절 %d회"%(count1_0))
                print("1번 스위칭 후 익절 %d회"%(count1_1))
                print("----------------------")
                print("%d번 손절"%(count2_1))
                print("----------------------")

                async def main_정산():
                    bot = telegram.Bot(token)
                    await bot.send_message(chat_id, f"{count1_0}/{count1_1}/{count2_1}")

                asyncio.run(main_정산())

        elif count3 <= count4:

                try:
                    # 초기설정 (최소거래수량 확인 필요)
                    balance = exchange.fetch_balance({'type':'future'})             # 선물 계좌로 변경
                    USDT_balance = balance['USDT']['free']                          # 계좌 잔고 조회
                    XRP_price = exchange.fetch_ticker(symbol)['last']               # 리플 현재가 조회
                    long_amount = 0                                                 # 초기 롱 물량(거래코인 최소거래수량 이상)
                    short_amount = (USDT_balance * start * leverage) / XRP_price    # 초기 숏 물량
                    count = 0 
                    count3 = 0
                    count4 = 0                                                       # 카운팅
                    reference_price = XRP_price                                     # 기준값 설정
                
                except:
                    error1 += 1
                    print("에러1")

                    async def main_에러1(): #실행시킬 함수명 임의지정
                        
                        bot = telegram.Bot(token)
                        await bot.send_message(chat_id,'에러1')

                    asyncio.run(main_에러1()) #봇 실행하는 코드

                while True:
                    try:
                        # 비트코인 현재가 확인
                        XRP_price = exchange.fetch_ticker(symbol)['last']

                        # 롱 포지션 물량이 없고 비트코인의 현재가가 기준값의 +1%일 경우 롱 포지션 생성(숏 포지션 3배 물량)
                        if long_amount == 0 and XRP_price >= reference_price * (1 + switching_point) and count < switching_count:
                            long_amount = short_amount * switching_ratio
                            
                            long_amount = long_amount - short_amount
                            short_amount = 0
                            count += 1

                        # 숏 포지션 물량이 없고 비트코인의 현재가가 기준값과 동일할 경우 숏 포지션 생성(롱 포지션 3배 물량)
                        elif short_amount == 0 and XRP_price <= reference_price and count < switching_count:
                            short_amount = long_amount * switching_ratio
                            
                            short_amount = short_amount - long_amount
                            long_amount = 0
                            count += 1

                        # 롱 포지션만 존재할 경우 묙표가 지점에서 모든 포지션 정리
                        elif short_amount == 0 and long_amount > 0 and XRP_price >= reference_price * (1 + (switching_point + target_point)):

                            count3 += 1

                            if count == 1:
                                count1_1 += 1

                            elif count == 2:
                                count1_2 += 1

                            elif count == 3:
                                count1_3 += 1

                            elif count == 4:
                                count1_4 += 1

                            elif count == 5:
                                count1_5 += 1

                            elif count == 6:
                                count1_6 += 1

                            elif count == 0:
                                count1_0 += 1

                            break

                        # 숏 포지션만 존재할 경우 목표가 지점에서 모든 포지션 정리
                        elif long_amount == 0 and short_amount > 0 and XRP_price <= reference_price * (1 - target_point): 

                            count4 += 1

                            if count == 1:
                                count1_1 += 1

                            elif count == 2:
                                count1_2 += 1

                            elif count == 3:
                                count1_3 += 1

                            elif count == 4:
                                count1_4 += 1

                            elif count == 5:
                                count1_5 += 1

                            elif count == 6:
                                count1_6 += 1

                            elif count == 0:
                                count1_0 += 1

                            break
                            
                        # 숏 보유중 - 마지막 스위칭 후 기준값 지점에서 모든 포지션 정리
                        elif long_amount == 0 and XRP_price >= reference_price * (1 + switching_point) and count >= switching_count:
                            
                            count3 += 1

                            count2_1 += 1
                            break

                        # 롱 보유중 - 마지막 스위칭 후 스위칭 지점에서 모든 포지션 정리
                        elif short_amount == 0 and XRP_price <= reference_price and count >= switching_count:

                            count4 += 1

                            count2_1 += 1
                            break

                    except:
                        error2 += 1
                        print("에러2")

                        async def main_에러2(): #실행시킬 함수명 임의지정
                            bot = telegram.Bot(token)
                            await bot.send_message(chat_id,'에러2')

                        # asyncio.run(main_에러2()) #봇 실행하는 코드

                        continue

                print("----------------------")
                print("0번 스위칭 후 익절 %d회"%(count1_0))
                print("1번 스위칭 후 익절 %d회"%(count1_1))
                print("----------------------")
                print("%d번 손절"%(count2_1))
                print("----------------------")

                async def main_정산():
                    bot = telegram.Bot(token)
                    await bot.send_message(chat_id, f"{count1_0}/{count1_1}/{count2_1}")

                asyncio.run(main_정산())

    else:
        os.system('cls')
        print("----------------------")
        print("0번 스위칭 후 익절 %d회"%(count1_0))
        print("1번 스위칭 후 익절 %d회"%(count1_1))
        print("----------------------")
        print("%d번 손절"%(count2_1))
        print("----------------------")
        print("대기합니다")
        time.sleep(60)
