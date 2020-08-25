
# %%
import os
import binance
import datetime
from binance.client import Client
from dotenv import load_dotenv


# %%
load_dotenv()
api_key = os.environ.get('api')
api_secret = os.environ.get('secret')


# %%
client = Client(api_key,api_secret)


# %%
trades = client.get_historical_trades(symbol='BNBBTC')


# %%
print(client.get_account())


# %%
#priting my balance on binance for Trx,
print(client.get_asset_balance(asset='TRX'))


# %%
# get latest price from Binance API
btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
# print full output (dictionary)
print(btc_price)


# %%
#since i dont have enough funds we get this error, but it is actually connecting to my binance account
def binance_buy_order(symbol)
    order = client.create_order(  #create_test_order
        symbol='BNBBTC',
        side=Client.SIDE_BUY,
        type=Client.ORDER_TYPE_MARKET,
        quantity=1)

# get all symbol prices

prices = client.get_all_tickers()


# %%



