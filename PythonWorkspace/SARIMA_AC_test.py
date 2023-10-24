from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os
# Define the Mean Absolute Percentage Error (MAPE) calculation
def mape(y_true, y_pred):
    return 100 * np.mean(np.abs((y_true - y_pred) / y_true))

def sarima_grid_search(train, validation, p_values, d_values, q_values, P_values, D_values, Q_values, S=24):
    best_score, best_params = float("inf"), None
    
    # Iterate over all parameter combinations
    for p in p_values:
        for d in d_values:
            for q in q_values:
                for P in P_values:
                    for D in D_values:
                        for Q in Q_values:
                            order = (p,d,q)
                            seasonal_order = (P,D,Q,S)
                            try:
                                # Fit model
                                model = SARIMAX(train, order=order, seasonal_order=seasonal_order, 
                                               enforce_stationarity=False, enforce_invertibility=False)
                                results = model.fit(disp=0)
                                
                                # Rolling forecast on validation set
                                start_index = len(train)
                                end_index = start_index + len(validation) - 1
                                forecast = results.predict(start=start_index, end=end_index, dynamic=True)
                                
                                # Denormalize forecast
                                forecast = scaler.inverse_transform(forecast.values.reshape(-1, 1)).flatten()
                                
                                # Calculate MAPE
                                error = mape(validation, forecast)
                                
                                # Check if this combination gives a better score
                                if error < best_score:
                                    best_score, best_params = error, (order, seasonal_order)
                                    
                            except:
                                continue
                                
    return best_score, best_params

# Define the range of parameters for the grid search
p_values = [0, 1, 2]
d_values = [0, 1]
q_values = [0, 1, 2]
P_values = [0, 1]
D_values = [0, 1]
Q_values = [0, 1]



# Load the dataset
data = pd.read_csv('dataClean.csv')
# Convert the 'tstamp' column to datetime format and set it as the index
data['tstamp'] = pd.to_datetime(data['tstamp'])
data.set_index('tstamp', inplace=True)

data = data.asfreq('H')
# Splitting the data into training and validation sets
train = data['AC'][:-24]
validation = data['AC'][-24:]

# Normalize the data
scaler = MinMaxScaler(feature_range=(0, 1))
train_normalized = scaler.fit_transform(train.values.reshape(-1, 1))
train_normalized = pd.Series(train_normalized.flatten(), index=train.index)
# Run the grid search (this may take some time)
best_score, best_params = sarima_grid_search(train_normalized, validation, p_values, d_values, q_values, 
                                            P_values, D_values, Q_values)

best_score, best_params