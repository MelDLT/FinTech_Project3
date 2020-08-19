import numpy as np
#EMA Simulator to assess the asset and choose ideal, optimized short and long windows
class EMASimulator:
    def __init__(self, stock_data_df, period, long_window, short_window, figsize=None):
        self.stock_data_df = stock_data_df
        #self.from_date = from_date
        self.period = period
        self.long_window = long_window
        self.short_window = short_window
        self.figsize = figsize
    
    def _build_dataframe(self):
        self.stock_data_df.sort_index(ascending=True, inplace=True)
        
                
    def _ema(self):
        self.stock_data_df['EWM Short'] = self.stock_data_df['Close'].ewm(span=self.short_window).mean()
        self.stock_data_df['EWM Long']= self.stock_data_df['Close'].ewm(span=self.long_window).mean()
        
    def _calculate_ema_signals(self):
        self.stock_data_df['EMA Signal'] = None

        mode = 'Open'
        for index in range(len(self.stock_data_df)):
            if index == 0:
                continue

            row = self.stock_data_df.iloc[index]
            prev_row = self.stock_data_df.iloc[index - 1]

            # open?
            if mode == 'Open' and row['EWM Short'] > row['EWM Long']  and prev_row['EWM Short'] < prev_row['EWM Long']:
                self.stock_data_df.iloc[index, self.stock_data_df.columns.get_loc('EMA Signal')] = 1
                mode = 'Close'

            # close?
            if mode == 'Close' and row['EWM Long'] > row['EWM Short'] and prev_row['EWM Long'] < prev_row['EWM Short']:
                self.stock_data_df.iloc[index, self.stock_data_df.columns.get_loc('EMA Signal')] = -1
                mode = 'Open'        
        
    def _returns(self):
        self.stock_data_df['EMA Signal'].fillna(method='ffill', inplace=True)
        self.stock_data_df['EMA Daily Return'] = self.stock_data_df['Close'].pct_change()
        self.stock_data_df['EMA Strategy Return'] = self.stock_data_df['EMA Daily Return'] * self.stock_data_df['EMA Signal']

    def _plot_returns(self):
        self.stock_data_df['EMA Strategy Return'].cumsum().plot(figsize=self.figsize)

    def simulate(self):
        self._build_dataframe()
        self._ema()
        self._calculate_ema_signals()
        self._returns()
        self._plot_returns()

        return (
            self.period, 
            self.long_window, 
            self.short_window, 
            self.stock_data_df['EMA Strategy Return'].sum(),
            self.stock_data_df['EMA Signal']
        )

#EMA Optimal Calculation
def EMA_Optimal(stock_data_df):
    long_windows = np.linspace(10, 100, 5, dtype=int)
    short_windows = np.linspace(10, 100, 5, dtype=int)
    periods = np.array([12, 48])

    result_df = pd.DataFrame({
        'period': [], 
        'long_window': [],
        'short_window': [],
        'result': []
    })
    for long_window in long_windows:
        for short_window in short_windows:
            for period in periods:
                simulator = EMASimulator(
                    stock_data_df, 
                    #from_date 
                    period="{}H".format(period), 
                    long_window=long_window, 
                    short_window=short_window,
                    figsize=(14, 7)
                )
                period, long_window, short_window, result, signal = simulator.simulate()
                result_df = result_df.append({
                    'period': period, 
                    'long_window': long_window, 
                    'short_window': short_window, 
                    'result': result,
                    'signal': signal
                }, ignore_index=True)
    ema_result=result_df.sort_values(by=['result'], ascending=False)[:5]
    return ema_result