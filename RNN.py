# Recurrent Neural Network



# Part 1 - Data Preprocessing

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the training set
dataset_train = pd.read_csv('ie_data.csv')
training_set = dataset_train.iloc[127:1767, [1,2,3,4,6,12]].values

# Feature Scaling
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)

# Creating a data structure with 60 timesteps and 1 output
X_train = []
y_train = []
for i in range(60, 1258):
    X_train.append(training_set_scaled[i-60:i,:])
    y_train.append(training_set_scaled[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)

# Reshaping
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 6))



# Part 2 - Building the RNN

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

# Initialising the RNN
regressor = Sequential()

# Adding the first LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 6)))
regressor.add(Dropout(0.2))

# Adding a second LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

# Adding a third LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

# Adding a fourth LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

# Adding the output layer
regressor.add(Dense(units = 1))

# Compiling the RNN
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

# Fitting the RNN to the Training set
regressor.fit(X_train, y_train, epochs = 100, batch_size = 32)



# Part 3 - Making the predictions and visualising the results

# Getting the real stock price of 2017
dataset_test = pd.read_csv('ie_data.csv')
real_stock_price = dataset_test.iloc[1767:1792, 1:2].values
real_stock_price = list(map(float, real_stock_price))

# Getting the predicted stock price of 2017
inputs = dataset_test.iloc[1708:1792, [1,2,3,4,6,12]].values
# inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)
X_test = []
for i in range(60, 84):
    X_test.append(inputs[i-60:i, :])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 6))
predicted_stock_price = regressor.predict(X_test)
trainPredict_dataset_like = np.zeros(shape=(len(predicted_stock_price), 6) )
trainPredict_dataset_like[:,0] = predicted_stock_price[:,0]
trainPredict= sc.inverse_transform(trainPredict_dataset_like)[:,0]
trainPredict=trainPredict.reshape((24,1))
trainPredict[:,0]+=float(dataset_test.iloc[1766:1767, 1:2].values)-float(dataset_test.iloc[1708:1709, 1:2].values)


# Visualising the results
plt.plot(real_stock_price, color = 'red', label = 'Real S&P 500')
plt.plot(trainPredict[:,0], color = 'blue', label = 'Predicted S&P 500')
plt.title('S&P 500 Prediction')
plt.xlabel('Time (Months starting from October 2017) ')
# plt.ylabel('S&P 500')
plt.legend()
plt.show(block=True)
