import ccxt

# API 키 설정
api_key = ''
secret_key = ''

# 거래소 생성
exchange = ccxt.bitget({
    'apiKey': api_key,
    'secret': secret_key,
    'enableRateLimit': True,
})

# 거래할 티커 설정
symbol = 'INJ/USDT'

# 주문 수량 설정
amount = 1  # INJ 코인을 1개 사거나 판매합니다.

# 주문 생성 (매수)
buy_order = exchange.create_market_buy_order(symbol, amount)

# 주문 생성 (매도)
sell_order = exchange.create_market_sell_order(symbol, amount)

print("INJ 코인을 시장 가격으로 성공적으로 사고 팔았습니다!")
