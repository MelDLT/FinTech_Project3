
import numpy as np
import pandas as pd
import os
from pandas import DataFrame
#MACD Simulator
class MACDSimulator():
    def __init__(self, stock_data_df, period, span1, span2, span3, figsize = None):
        self.stock_data_df = stock_data_df
        self.period = period
        self.span1 = span1
        self.span2 = span2
        self.span3 = span3
        self.figsize = figsize

    def _build_dataframe(self):
        self.stock_data_df.sort_index(ascending=True, inplace=True)
    
    def _macd(self):
        self.stock_data_df['exp1'] = self.stock_data_df.Close.ewm(self.span1, adjust=False).mean()
        self.stock_data_df['exp2'] = self.stock_data_df.Close.ewm(self.span2, adjust=False).mean()
        self.stock_data_df['macd'] = self.stock_data_df.exp1-self.stock_data_df.exp2
        self.stock_data_df['macdout'] = self.stock_data_df.macd.ewm(self.span3, adjust=False).mean()

    def _calculate_macd_signals(self):
        self.stock_data_df['MACD Signal'] = None

        mode = 'Open'
        for index in range(len(self.stock_data_df)):
            if index == 0:
                continue

            row = self.stock_data_df.iloc[index]
            prev_row = self.stock_data_df.iloc[index - 1]

            # open?
            if mode == 'Open' and row['macd'] > row['macdout']  and prev_row['macd'] < prev_row['macdout']:
                self.stock_data_df.iloc[index, self.stock_data_df.columns.get_loc('MACD Signal')] = 1
                mode = 'Close'

            # close?
            if mode == 'Close' and row['macd'] < row['macdout'] and prev_row['macd'] > prev_row['macdout']:
                self.stock_data_df.iloc[index, self.stock_data_df.columns.get_loc('MACD Signal')] = -1
                mode = 'Open'

        #self.stock_data_df["MACD Signal"] = np.where(self.stock_data_df['macd'] > self.stock_data_df['macdout'], 1.0, 0.0)
        #self.stock_data_df["MACD Signal"] = np.where(self.stock_data_df['macd'] < self.stock_data_df['macdout'], -1.0, 0.0)
        #self.stock_data_df["MACD Signal"] = self.stock_data_df["MACD Short"] + self.stock_data_df["MACD Long"]

    def _returns(self):
        self.stock_data_df['MACD Signal'].fillna(method='ffill', inplace=True)
        self.stock_data_df['MACD Daily Return'] = self.stock_data_df['Close'].pct_change()
        self.stock_data_df['MACD Strategy Return'] = self.stock_data_df['MACD Daily Return'] * self.stock_data_df['MACD Signal']

    def _plot_returns(self):
        self.stock_data_df['MACD Strategy Return'].cumsum().plot(figsize=self.figsize)

    def simulate(self):
        self._build_dataframe()
        self._macd()
        self._calculate_macd_signals()
        self._returns()
        self._plot_returns()

        return (
            self.period, 
            self.span1, 
            self.span2, 
            self.span3,
            self.stock_data_df['MACD Strategy Return'].sum(),
            self.stock_data_df['MACD Signal']
        )










#MACD Optimal Calculation
def MACD_Optimal(stock_data_df):
    span1s = np.linspace(10, 100, 5, dtype=int)
    span2s= np.linspace(10, 100, 5, dtype=int)
    span3s= np.linspace(10, 100, 5, dtype=int)
    periods = np.array([12, 48])

    result_df = pd.DataFrame({
        'period': [], 
        'span1': [],
        'span2': [],
        'span3': [],
        'result': []
    })

    for span1 in span1s:
        for span2 in span2s:
            for span3 in span3s:
                for period in periods:
                    simulator = MACDSimulator(
                        stock_data_df, 
                        #from_date 
                        period="{}H".format(period), 
                        span1=span1, 
                        span2=span2, 
                        span3=span3,
                        figsize=(14, 7)
                    )
                    period, span1, span2, span3, result, signal = simulator.simulate()
                    result_df = result_df.append({
                        'period': period, 
                        'span1': span1, 
                        'span2': span2, 
                        'span3': span3,
                        'result': result,
                        'signal': signal
                    }, ignore_index=True)
    macd_result=result_df.sort_values(by=['result'], ascending=False)[:5]
    return macd_result