def main_trading_function(stock_ticker,crypto_ticker):
    #import relevant libraries 
    import pandas as pd
    import plotly.express as px
    import panel as pn
    import hvplot.pandas
    import requests
    import json
    import numpy as np
    import matplotlib.pyplot as plt
    import json
    from pathlib import Path
    import alpaca_trade_api as tradeapi
    from dotenv import load_dotenv
    import os
    from datetime import datetime, timedelta,date
    from pandas import DataFrame

    # Pull in External Functions and Classes

    from ticker_data import *
    from coin_data import *
    from EMA import *
    from BOLLINGER import *
    from MACD import *
    from LSTM import *
    from new_order import *
    from coin_order import *

    # Get the Stock Ticker Data

    #set the stock of interest
    stock_ticker='SPY'
    #from ticker_data.py run function get_ticker_data
    stock_data_df=get_ticker_data(api, stock_ticker)

    # Get the Crypto Coin Data

    #set the crypto of interest
    crypto_ticker='BTC/USD'
    #from ticker_data.py run function get_ticker_data
    crypto_data_df=get_crypto_data(exchange, crypto_ticker)
    crypto_data_df.columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"]


    crypto_data_df.head()

    # EMA Simulation and Optimal Calculations

    #from EMA.py run EMA_Optimal Calculator
    ema_result=EMA_Optimal(stock_data_df)
    opt_ema_df=ema_result.head()


    #define the optimal outputs as variables
    period=opt_ema_df['period'].iloc[0]
    long_window=opt_ema_df['long_window'].iloc[0]
    short_window=opt_ema_df['short_window'].iloc[0]


    #from EMA.py run the EMA simulator on the optimal variables
    EMAsimulator = EMASimulator(
        stock_data_df, 
        #from_date="2018-01-01", 
        period=period, 
        long_window=long_window, 
        short_window=short_window
    )
    EMAsimulator.simulate()

    # Bollinger Band Simulation and Optimal Calculations

    #from BOLLINGER.py run Bollinger_Band_Optimal Calculator
    bollinger_result=Bollinger_Band_Optimal(stock_data_df)
    opt_bollinger_df=bollinger_result.head()


    #define the optimal outputs as variables
    period=opt_bollinger_df['period'].iloc[0]
    bollinger_window=int(opt_bollinger_df['bollinger_window'].iloc[0])
    no_of_std=opt_bollinger_df['no_of_std'].iloc[0]


    #from BOLLINGER.py run the BOLLINGER simulator on the optimal variables
    BOLLINGERsimulator = BollingerBandsSimulator(
        stock_data_df, 
        #from_date="2018-01-01", 
        period=period, 
        bollinger_window=bollinger_window, 
        no_of_std=no_of_std
    )
    BOLLINGERsimulator.simulate()

    # MACD Simulation and Optimal Calculations

    #from MACD.py run MACD_Optimal Calculator
    macd_result=MACD_Optimal(stock_data_df)
    opt_macd_df=macd_result.head()


    #define the optimal outputs as variables
    period=opt_macd_df['period'].iloc[0]
    span1=opt_macd_df['span1'].iloc[0]
    span2=opt_macd_df['span2'].iloc[0]
    span3=opt_macd_df['span3'].iloc[0]


    #from MACD.py run the MACD simulator on the optimal variables
    MACDsimulator = MACDSimulator(
        stock_data_df, 
        #from_date="2018-01-01", 
        period=period, 
        span1=span1,
        span2=span2,
        span3=span3
    )
    MACDSignals=MACDsimulator.simulate()

    # Look at the Resulting Signal Data and Stock Data

    stock_data_df.dropna(subset=('EMA Signal','Bollinger Signal', 'MACD Signal'),inplace=True)


    ema_signal_df=stock_data_df['EMA Signal']
    bollinger_signal_df=stock_data_df['Bollinger Signal']
    macd_signal_df=stock_data_df['MACD Signal']
    close_df=stock_data_df['Close']

    # Get All Signals and Combined Signal

    #function to get all trading signals
    #return data frame holding trading signals
    def get_trading_signals(close_df,ema_signal_df,bollinger_signal_df,macd_signal_df):
        trading_signal_df=pd.concat([close_df,ema_signal_df, bollinger_signal_df,macd_signal_df],axis=1,    join="inner")
        trading_signal_df['Signal']=trading_signal_df['EMA Signal']+ trading_signal_df['Bollinger Signal']+ trading_signal_df['MACD Signal']
        #trading_signal_df['Overall Entry/Exit']=trading_signal_df['Signal'].diff()
        return trading_signal_df
        


    trading_signal_df=get_trading_signals(close_df,ema_signal_df,bollinger_signal_df,macd_signal_df)
    trading_signal_df.tail()


    stocks=predict_price_model(trading_signal_df)



    signal_support_df=stocks[0]
    signal_support_df


    signal_support_value=signal_support_df['Support'].mean()


    stocks[1]

    # Check Signals and Call Functions to Place Trades

    if trading_signal_df['Signal'][-1]>=1 and signal_support_value>=1:
        #place a buy order
        side='buy'
        order_type='market'
        time_in_force='gtc'
        qty=1
        place_market_order(stock_ticker,qty, side, order_type, time_in_force)
    elif trading_signal_df['Signal'][-1]<=-1 and signal_support_value>=1:
        #place a sell order
        side='sell'
        order_type='market'
        time_in_force='gtc'
        qty=1
        place_market_order(stock_ticker,qty, side, order_type, time_in_force)

    # Apply for Crypto Data Signals and Simulators
    # EMA Simulator and Optimal Calculation Crypto

    #from EMA.py run EMA_Optimal Calculator
    ema_result=EMA_Optimal(crypto_data_df)
    opt_ema_df=ema_result.head()


    #define the optimal outputs as variables
    period=opt_ema_df['period'].iloc[0]
    long_window=opt_ema_df['long_window'].iloc[0]
    short_window=opt_ema_df['short_window'].iloc[0]


    #from EMA.py run the EMA simulator on the optimal variables
    EMAsimulator = EMASimulator(
        crypto_data_df, 
        #from_date="2018-01-01", 
        period=period, 
        long_window=long_window, 
        short_window=short_window
    )
    EMAsimulator.simulate()

    # Bollinger Bands Simulator and Optimal Calculation Crypto

    #from BOLLINGER.py run Bollinger_Band_Optimal Calculator
    bollinger_result=Bollinger_Band_Optimal(crypto_data_df)
    opt_bollinger_df=bollinger_result.head()


    #define the optimal outputs as variables
    period=opt_bollinger_df['period'].iloc[0]
    bollinger_window=int(opt_bollinger_df['bollinger_window'].iloc[0])
    no_of_std=opt_bollinger_df['no_of_std'].iloc[0]


    #from BOLLINGER.py run the BOLLINGER simulator on the optimal variables
    BOLLINGERsimulator = BollingerBandsSimulator(
        crypto_data_df, 
        #from_date="2018-01-01", 
        period=period, 
        bollinger_window=bollinger_window, 
        no_of_std=no_of_std
    )
    BOLLINGERsimulator.simulate()

    # MACD Simulator and Optimal Calculation Crypto

    #from MACD.py run MACD_Optimal Calculator
    macd_result=MACD_Optimal(crypto_data_df)
    opt_macd_df=macd_result.head()


    #define the optimal outputs as variables
    period=opt_macd_df['period'].iloc[0]
    span1=opt_macd_df['span1'].iloc[0]
    span2=opt_macd_df['span2'].iloc[0]
    span3=opt_macd_df['span3'].iloc[0]


    #from MACD.py run the MACD simulator on the optimal variables
    MACDsimulator = MACDSimulator(
        crypto_data_df, 
        #from_date="2018-01-01", 
        period=period, 
        span1=span1,
        span2=span2,
        span3=span3
    )
    MACDSignals=MACDsimulator.simulate()


    crypto_data_df.dropna(subset=('EMA Signal','Bollinger Signal', 'MACD Signal'),inplace=True)
    crypto_data_df.head()


    ema_signal_df=crypto_data_df['EMA Signal']
    bollinger_signal_df=crypto_data_df['Bollinger Signal']
    macd_signal_df=crypto_data_df['MACD Signal']
    close_df=crypto_data_df['Close']


    trading_signal_df=get_trading_signals(close_df,ema_signal_df,bollinger_signal_df,macd_signal_df)
    trading_signal_df.head()


    crypto=predict_price_model(trading_signal_df)


    signal_support_df=stocks[0]
    signal_support_df.tail(50)





    if trading_signal_df['Signal'][-1]>=1 and signal_support_value>=1:
        #place a buy order on kraken
        
        binance_buy_order(crypto_ticker)

        ###FUNCTION HERE
    elif trading_signal_df['Signal'][-1]<=-1 and signal_support_value>=-1:
        #place a sell order on kraken
        sell_coin_order(crypto_ticker)
        ####FUNCTION





