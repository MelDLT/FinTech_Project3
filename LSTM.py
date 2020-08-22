import numpy as np
import pandas as pd
import hvplot.pandas
from sklearn.preprocessing import MinMaxScaler
#initialize tensorflow and keras models
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

#  Initialize close values as features in the model
def window_data(trading_signal_df, window, feature_col_number, target_col_number):
    X = []
    y = []
    for i in range(len(trading_signal_df) - window - 1):
        features = trading_signal_df.iloc[i:(i + window), feature_col_number]
        target = trading_signal_df.iloc[(i + window), target_col_number]
        X.append(features)
        y.append(target)
    return np.array(X), np.array(y).reshape(-1, 1)

def predict_price_model(trading_signal_df):
    

    #  Create LSTM predictive price model to validate the signals
    
    # Predict Closing Prices using a 10 day window of previous closing prices
    # Try a window size anywhere from 1 to 10 and see how the model performance changes
    window_size = 1

    # Column index 0 is the `Close` column
    feature_column = 0
    target_column = 0
    X, y = window_data(trading_signal_df, window_size, feature_column, target_column)

    # Use 70% of the data for training and the remaining 30% for testing
    split = int(0.7 * len(X))
    X_train = X[: split - 1]
    X_test = X[split:]
    y_train = y[: split - 1]
    y_test = y[split:]

    # Use MinMaxScaler to scale the data between 0 and 1. 
    scaler = MinMaxScaler()
    scaler.fit(X)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    scaler.fit(y)
    y_train = scaler.transform(y_train)
    y_test = scaler.transform(y_test)

    # Reshape the features for the model
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
    print (f"X_train sample values:\n{X_train[:1]} \n")
    print (f"X_test sample values:\n{X_test[:1]}")

    # Build the LSTM model. 
    model = Sequential()
    number_units = 10
    dropout_fraction = 0.2

    # Layer 1
    model.add(LSTM(
        units=number_units,
        return_sequences=True,
        input_shape=(X_train.shape[1], 1))
        )
    model.add(Dropout(dropout_fraction))
    # Layer 2
    model.add(LSTM(units=number_units, return_sequences=True))
    model.add(Dropout(dropout_fraction))
    # Layer 3
    model.add(LSTM(units=number_units))
    model.add(Dropout(dropout_fraction))
    # Output layer
    model.add(Dense(1))

    # Compile the model
    model.compile(optimizer="adam", loss="mean_squared_error")

    # Summarize the model
    model.summary()

    # Train the model
    model.fit(X_train, y_train, epochs=20, shuffle=False, batch_size=1, verbose=1)

    # Evaluate the model
    model.evaluate(X_test, y_test)

    # Make some predictions for future price
    predicted = model.predict(X_test)

    # Recover the original prices instead of the scaled version
    predicted_prices = scaler.inverse_transform(predicted)
    real_prices = scaler.inverse_transform(y_test.reshape(-1, 1))

    # Create a DataFrame of Real and Predicted values
    stocks = pd.DataFrame({
        "Real": real_prices.ravel(),
        "Predicted": predicted_prices.ravel()
    })
    stocks.tail()


    # Plot the real vs predicted values as a line chart
    stock_plot = stocks.hvplot(title ="Real vs Predicted Closing Price", value_label = 'Price (USD)')


    #get the difference between the real and predicted price in time
    stocks['Difference']=abs(stocks['Real']-stocks['Predicted'])
    #get 1 std deviation from the real stock price
    standard_deviation=stocks['Real'].std()

    #check if the difference is within 1 std deviation
    
    for index,row in stocks.iterrows():
        if row['Difference']<(15):
            stocks['Support']=1
        elif row['Difference']>(15):
            stocks['Support']=-1


    return stocks,stock_plot


