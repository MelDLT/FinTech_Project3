
import alpaca_trade_api as tradeapi 
api = tradeapi.REST(
        ALPACA_API_KEY,
        ALPACA_SECRET_KEY,
        'https://paper-api.alpaca.markets', api_version='v2'
    )

def place_market_order(ticker,qty, side, order_type, time_in_force):
    # Place a market order to buy qty of number of shares 
    api.submit_order(
        symbol=ticker,
        qty=qty,
        side=side, #define side as either 'buy' or sell'
        type=order_type, #define the type of the order: 'market', 'limit'
        time_in_force=time_in_force, #define time in force: 'gtc'=,'opg'=opening
    )

 def place_limit_order(ticker,qty, side, order_type, time_in_force,limit_price):  
    api.submit_order(
        symbol=ticker,
        qty=qty,
        side=side, #define side as either 'buy' or sell'
        type=order_type, #define the type of the order: 'market', 'limit'
        time_in_force=time_in_force, #define time in force: 'gtc'=,'opg'=opening
        limit_price=limit_price #define limit_price for the order
    )
