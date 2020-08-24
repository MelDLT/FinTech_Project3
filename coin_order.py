#import krakenex
import ccxt
import os
import pandas as pd 
from dotenv import load_dotenv

load_dotenv()


kraken = ccxt.kraken({
    'apiKey': os.getenv('KRAKEN_PUBLIC_KEY'),
    'secret': os.getenv('KRAKEN_SECRET_KEY')
    #'url': os.getenv('KRAKEN_API_URL')
})


def execute_coin_order(signals, symbol, account):
    """Makes a buy/sell/hold decision."""

    print("Executing Trading Strategy!")

    if signals >= 1.0:
        print("buy")
        kraken.create_market_buy_order(symbol, 1, {'trading_agreement': 'agree'})
        #number_to_buy = round(account["balance"] / signals["close"].iloc[-1], 0) * 0.001
        #account["balance"] -= number_to_buy * signals["close"].iloc[-1]
        #account["shares"] += number_to_buy
    elif signals <= -1.0:
        print("sell")
        kraken.create_market_sell_order(symbol, 1)

        #account["balance"] += signals["close"].iloc[-1] * account["shares"]
        #ccount["shares"] = 0
    else:
        print("hold")

    return account

def buy_coin_order(symbol):

    kraken.create_market_buy_order(symbol, 1, {'trading_agreement': 'agree'})


def sell_coin_order(symbol):

   kraken.create_market_sell_order(symbol, 1)



#def Coin_Order():
#    kraken = krakenex.API()
#    kraken.load_key('kraken.key')
#
#    response = kraken.query_private('AddOrder',
#                                    {'pair': 'XXBTZEUR',
#                                     'type': 'buy',
#                                     'ordertype': 'limit',
#                                     'price': '1',
#                                     'volume': '1',
#                                     # `ordertype`, `price`, `price2` are valid
#                                     'close[ordertype]': 'limit',
#                                     'close[price]': '9001',
#                                     # these will be ignored!
#                                     'close[pair]': 'XXBTZEUR',
#                                     'close[type]': 'sell',
#                                     'close[volume]': '1'})
#    return response
#
#if __name__ == '__main__':
#    ret = main()
#    print(ret)

