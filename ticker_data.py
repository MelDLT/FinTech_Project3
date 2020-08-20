import pandas as pd
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv
import os
from pandas import DataFrame

## Get Market Data for S&P500 
#engage API keys by activating .env file for Alpaca Api
load_dotenv()
alpaca_api_key = os.getenv("ALPACA_API_KEY")
alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")
alpaca_base_url=os.getenv("APCA_API_BASE_URL")
api = tradeapi.REST(alpaca_api_key, alpaca_secret_key,alpaca_base_url, api_version='v2')



#function to read the api data for stock ticker
#returns dataframe of closing price and daily returns for a given ticker symbol
def get_ticker_data(api,ticker):
    #load in historical data for provided ticker
    stock_data_df = api.alpha_vantage.historic_quotes(ticker, adjusted=True, output_format='pandas')

    #Clean Data
    

    #Sort earliest to latest. so that .pct_change() function works right.
    stock_data_df.sort_index(inplace=True, ascending=True)

    # Drop nulls
    stock_data_df.dropna(inplace=True)

    # drop duplicates
    stock_data_df.drop_duplicates(inplace=True)

    #count nulls 
    stock_data_df.isnull().sum()

    #create a dataframe column for the daily returns (pct_change) values and concat 
    returns_df = stock_data_df['5. adjusted close'].pct_change()
    stock_data_df = pd.concat([stock_data_df, returns_df], axis="columns", join="inner")

    #Change column names to avoid confusion
    columns = ['Open','High','Low','Close','Adjusted Close','Volume','Dividend Amount','Split Coefficient','Daily Returns']
    stock_data_df.columns = columns

    # Drop nulls
    stock_data_df.dropna(inplace=True)

    #drop duplicates
    stock_data_df.drop_duplicates(inplace=True) 
    return stock_data_df

