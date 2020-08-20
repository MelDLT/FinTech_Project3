
import numpy as np
import pandas as pd
import os
from pandas import DataFrame
#Bollinger Bands Simulator to assess the asset and choose ideal, optimized bollinger window, no of standard deviations, and period.
class BollingerBandsSimulator:

    def __init__(self, stock_data_df, period, bollinger_window, no_of_std, figsize=None):
        self.stock_data_df = stock_data_df
        #self.from_date = from_date
        self.period = period
        self.bollinger_window = bollinger_window
        self.no_of_std = no_of_std
        self.figsize = figsize
    
    def _build_dataframe(self):
        self.stock_data_df.sort_index(ascending=True, inplace=True)
        
                
    def _bollinger_bands(self):
        
        self.stock_data_df['Bollinger middle'] = self.stock_data_df['Close'].rolling(self.bollinger_window).mean()
        #self.stock_data_df['Bollinger Long']= self.stock_data_df['Close'].rolling(self.bollinger_window_long).mean()
        self.stock_data_df['Bollinger STD'] = self.stock_data_df['Close'].rolling(self.bollinger_window).std()

        self.stock_data_df['Bollinger Upper']  = self.stock_data_df['Bollinger middle'] + (self.stock_data_df['Bollinger STD'] * self.no_of_std)
        self.stock_data_df['Bollinger Lower']  = self.stock_data_df['Bollinger middle'] - (self.stock_data_df['Bollinger STD'] * self.no_of_std)


    def _calculate_signals(self):
        self.stock_data_df['Bollinger Signal'] = None

        mode = 'Open'
        for index in range(len(self.stock_data_df)):
            if index == 0:
                continue

            row = self.stock_data_df.iloc[index]
            prev_row = self.stock_data_df.iloc[index - 1]

            # open?
            if mode == 'Open' and row['Close'] < row['Bollinger Lower'] and prev_row['Close'] > prev_row['Bollinger Lower']:
                self.stock_data_df.iloc[index, self.stock_data_df.columns.get_loc('Bollinger Signal')] = 1
                mode = 'Close'

            # close?
            if mode == 'Close' and row['Close'] > row['Bollinger Upper'] and prev_row['Close'] < prev_row['Bollinger Upper']:
                self.stock_data_df.iloc[index, self.stock_data_df.columns.get_loc('Bollinger Signal')] = -1
                mode = 'Open'        
        
    def _returns(self):
        self.stock_data_df['Bollinger Signal'].fillna(method='ffill', inplace=True)
        self.stock_data_df['Bollinger Daily Return'] = self.stock_data_df['Close'].pct_change()
        self.stock_data_df['Bollinger Strategy Return'] = self.stock_data_df['Bollinger Daily Return'] * self.stock_data_df['Bollinger Signal']

    def _plot_returns(self):
        self.stock_data_df['Bollinger Strategy Return'].cumsum().plot(figsize=self.figsize)

    def simulate(self):
        self._build_dataframe()
        self._bollinger_bands()
        self._calculate_signals()
        self._returns()
        self._plot_returns()

        return (
            self.period, 
            self.bollinger_window, 
            self.no_of_std, 
            self.stock_data_df['Bollinger Strategy Return'].sum(),
            self.stock_data_df['Bollinger Signal']
        )

#Bollinger Band Optimal Calculation
def Bollinger_Band_Optimal(stock_data_df):
    windows = np.linspace(10, 100, 5, dtype=int)
    stds = np.linspace(1, 3, 5)
    periods = np.array([12, 48])

    result_df = pd.DataFrame({
        'period': [], 
        'bollinger_window': [],
        'no_of_std': [],
        'result': []
    })
    for window in windows:
        for std in stds:
            for period in periods:
                simulator = BollingerBandsSimulator(
                    stock_data_df, 
                    #from_date 
                    period="{}H".format(period), 
                    bollinger_window=window, 
                    no_of_std=std,
                    figsize=(14, 7)
                )
                period, bollinger_window, no_of_std, result, signal = simulator.simulate()
                result_df = result_df.append({
                    'period': period, 
                    'bollinger_window': bollinger_window, 
                    'no_of_std': no_of_std, 
                    'result': result,
                    'signal':signal
                }, ignore_index=True)
    bollinger_result=result_df.sort_values(by=['result'], ascending=False)[:5]
    return bollinger_result