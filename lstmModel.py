# The aim of this class is to forecast the behaviour of variable of a pH Neutralization plant.
# In this case, the model that describe the plant behaviour is a LSTM network.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import time

# For LSTM model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.callbacks import EarlyStopping
from keras.models import load_model


class LSTMModelClass:
    def __init__(self, features_data, output_data):
        self.features_data = features_data
        self.output_data = output_data
        self.model = Sequential()
        self.s1 = MinMaxScaler(feature_range=(-1, 1))
        self.s2 = MinMaxScaler(feature_range=(-1, 1))

# ============================================ Plot loss ================================================ #
    def plot_loss(self, history_model):
        plt.figure(figsize=(16, 9))
        plt.semilogy(history_model.history['loss'])
        plt.xlabel('Epochs', fontsize=14)
        plt.ylabel('Loss', fontsize=14)
        plt.title('LSTM loss', fontsize=18)
        option_input = input('Please enter Y for saving the model')
        if option_input == 'Y':
            file_name = input('Please enter the name of the model. Do not use especial characters')
            file_name = file_name + '.h5'
            self.model.save(file_name)

# ============================================ Plotting  ================================================ #
    def plot_validation_prediction(self, output_predicted, output_measured):
        output_predicted_scaled = self.s2.inverse_transform(output_predicted)     # un-scale outputs
        output_measured_scaled = self.s2.inverse_transform(output_measured)
        plt.figure(figsize=(16, 9))
        plt.plot(output_predicted_scaled, '-k', linewidth=2, label='LSTM')
        plt.plot(output_measured_scaled, 'b', linewidth=2, label='Measured')
        plt.grid()
        plt.legend()
        plt.xlabel('Time(sec)', fontsize=14)
        plt.title('Validation of the LSTM')

# ====================================== Load model ===================================================== #
    def load_model_function(self, filename):
        self.model = load_model(filename)

# ====================================== Predict_with_help ================================================== #
    def predict_with_help(self, x_test, y_test, window=None):
        input_test_new = self.s1.transform(x_test)
        output_test_new = self.s2.transform(y_test)

        input_test_new_reshaped = []
        output_test_new_reshaped = []
        for i in range(window, len(input_test_new)):
            input_test_new_reshaped.append(input_test_new[i-window:i, :])
            output_test_new_reshaped.append(output_test_new[i])

        # Reshape data to format LSTM
        input_test_new_reshaped, output_test_new_reshaped = np.array(input_test_new_reshaped),\
                                                            np.array(output_test_new_reshaped)
        output_predicted_new = self.model.predict(input_test_new_reshaped)
        output_predicted = self.s2.inverse_transform(output_predicted_new)
        return output_predicted

# ========================================== Training LSTM ============================================== #
    #  This method fit the data into a LSTM network
    def training_lstm(self, window=None, number_neurons=50, dropout_set=0.2, optimizer_selection='adam',
                      loss_selection='mean_squared_error', metrics_selection=['accuracy']):
        # Scale features
        # s1 = MinMaxScaler(feature_range=(-1, 1))    # s1 is a auxiliary variable used pre-process the feature data
        x_feature_input = self.s1.fit_transform(self.features_data)
        # Scale predicted value (outputs)
        # s2 = MinMaxScaler(feature_range=(-1, 1))    # s1 is a auxiliary variable used pre-process the output data
        y_output = self.s2.fit_transform(self.output_data)

        # It is important to remember that each time step uses the last 'window' to predict the next change
        x_feature_reshaped = []
        y_output_reshaped = []

        for i in range(window, len(x_feature_input)):
            x_feature_reshaped.append(x_feature_input[i-window:i, :])
            y_output_reshaped.append(y_output)

        # Reshaped the data to format accepted by LSTM
        x_feature_reshaped, y_output_reshaped = np.array(x_feature_reshaped), np.array(y_output_reshaped)

        # ================================== Create LSTM network =========================================== #
        # model = Sequential()
        # Important this section need to be improved. Currently, it is only available for 2-d inputs features
        self.model.add(LSTM(units=number_neurons, return_sequences=True, input_shape=(x_feature_reshaped.shape[1],
                                                                                 x_feature_reshaped.shape[2])))
        self.model.add(Dropout(dropout_set))
        self.model.add(LSTM(units=number_neurons, return_sequences=True))
        self.model.add(Dropout(dropout_set))
        self.model.add(LSTM(units=number_neurons))
        self.model.add(Dropout(dropout_set))
        self.model.add(Dense(units=1))
        # ============================== Training the network ====================================== #

        self.model.compile(optimizer=optimizer_selection, loss=loss_selection, metrics=metrics_selection)
        # Allow for early exit
        early_stopping = EarlyStopping(monitor='loss', mode='min', verbose=1, patience=10)
        # Fit (and time) LSTM model
        # initial_time = time.time()
        history = self.model.fit(x_feature_reshaped, y_output_reshaped, epochs=10, batch_size=250,
                                 callbacks=[early_stopping], verbose=1)
        # final_time =time.time()
        self.plot_loss(history_model=history)

        # =================================== Validation ========================================= #
        # Verify the fit of the model
        y_output_predicted = self.model.predict(x_feature_reshaped)
        # Plot the validation results
        self.plot_validation_prediction(output_predicted=y_output_predicted, output_measured=y_output_reshaped)





