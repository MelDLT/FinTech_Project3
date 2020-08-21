

import numpy as np
import pandas as pd
#import hvplot.pandas
import ccxt
import os



kraken_public_key = os.getenv('KRAKEN_PUBLIC_KEY')
kraken_secret_key = os.getenv('KRAKEN_SECRET_KEY')



exchange = ccxt.kraken({
    'apiKey': kraken_public_key,
    'secret': kraken_secret_key,
})



def get_crypto_details (exchange):
    crypto_details = exchange.load_markets()

    # Import data as a Pandas DataFrame
    crypto_df = pd.DataFrame(crypto_details)
    return crypto_df



#print(type(crypto_df.columns.values))
#print(crypto_df.columns.values)
#print(len(crypto_df.columns.values))



#exchange.has 


def get_crypto_data (exchange, ticker):
    historical_prices = exchange.fetch_ohlcv( ticker, "1d")

# Import the data as a Pandas DataFrame and set the columns
    historical_prices_df = pd.DataFrame(
    historical_prices, columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"]
)
   #historical_prices_df



    historical_prices_df["Date"] = pd.to_datetime(
    historical_prices_df["Timestamp"], unit="ms"
)
    

    historical_prices_df.set_index("date", inplace= True)
    

#, infer_datetime_format=True, parse_dates=True, inplace=True, ascending=True)
#historical_prices_df.head()

#df2  index_col="Date", infer_datetime_format=True, parse_dates=True)['Close']
#df2 = df2.sort_index()
#df2.tail()


    crypto_data_df= historical_prices_df



    return crypto_data_df


