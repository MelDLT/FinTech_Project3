
import alpaca_trade_api as tradeapi 
from dotenv import load_dotenv
import os

load_dotenv()
alpaca_api_key = os.getenv("ALPACA_API_KEY")
alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")
alpaca_base_url=os.getenv("APCA_API_BASE_URL")
api = tradeapi.REST(alpaca_api_key, alpaca_secret_key,alpaca_base_url, api_version='v2')

api = tradeapi.REST(
        alpaca_api_key,
        alpaca_secret_key,
        'https://paper-api.alpaca.markets', api_version='v2'
    )
os.environ["APCA_API_BASE_URL"] = "https://paper-api.alpaca.markets"
account = api.get_account()
account.status

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
