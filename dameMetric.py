# dameMetric defines the dameMetricClass that is used to represent a series of DAME validation metrics. The term was
# presented in Willmott, 2014. This is a child class of validationMetricClass from validationMetric. In this case, the
# inputs are the same that in validationMetricClass:
#           predicted_data -> representing the data predicted by the models (type pandas.Series)
#           real_data      -> representing the data measured in the real environment (type pandas.Series)
# The metrics implemented in this class are:
#           FIT index       -> fit_index        -> presented in Ljung, 19xx             -> Checked 06/17/2020
#           TIC index       -> tic_index        -> presented in Theil, 19xx             -> Checked 06/17/2020
#           Willmott index  -> willmott_index   -> presented in Wilmmott, 2000          -> Checked 06/17/2020
#           Russell index   -> russell_index    -> presented in Russell,                -> Checked 06/17/2020

from validationMetric import ValidationMetricClass
# import pandas as pd
import numpy as np
import math


class DameMetricClass(ValidationMetricClass):
    def __init__(self, predicted_data, real_data):
        super().__init__(predicted_data, real_data)

#   fit_index function it is used to calculated the fit between to time series.
    def fit_index(self):
        if self.have_integrity():
            try:
                fit_index_value = 1 - np.sqrt(
                    sum((self.real_data - self.predicted_data) ** 2) / sum(
                        (self.real_data - self.real_data.mean()) ** 2))
                return fit_index_value
            except ZeroDivisionError:
                print('Check your real_data. It must have standard deviation of 0; therefore, it is impossible to DIV')
                return float('Inf')
        else:
            # fit_index_value = float('Inf')
            return float('Inf')

#   tic_index function is used to calculated the Theil Inequality Coefficient index.
    def tic_index(self):
        if self.have_integrity():
            try:
                tic_numerator = np.sqrt(sum((self.real_data - self.predicted_data) ** 2) / len(self.real_data))
                tic_denominator_real = np.sqrt(sum(self.real_data ** 2) / len(self.real_data))
                tic_denominator_predicted = np.sqrt(sum(self.predicted_data ** 2) / len(self.predicted_data))
                tic_index_value = tic_numerator / (tic_denominator_real + tic_denominator_predicted)
                return tic_index_value
            except ZeroDivisionError:
                print('Check your data. Apparently the sum of the predicted data\' '
                      'RMS and real data\' RMS is equal to 0\n')
                print('Therefore, an ZeroDivision error occur')
                return float('Inf')
        else:
            return float('Inf')

    def willmott_index(self):
        if self.have_integrity():
            c = 2               # c is constant of the formula used this value can be modified depending
            # of the applications. In this case, it is used a value of 2.
            sum_of_error_of_prediction = sum(abs(self.real_data - self.predicted_data))
            sum_of_error_with_the_mean_of_real_data = sum(abs(self.real_data - self.real_data.mean()))
            try:
                if sum_of_error_of_prediction < (c * sum_of_error_with_the_mean_of_real_data):
                    return 1 - (sum_of_error_of_prediction / (c * sum_of_error_with_the_mean_of_real_data))
                elif sum_of_error_of_prediction > (c * sum_of_error_with_the_mean_of_real_data):
                    return ((c * sum_of_error_with_the_mean_of_real_data) / sum_of_error_of_prediction) - 1
                elif sum_of_error_of_prediction == (c * sum_of_error_with_the_mean_of_real_data):
                    return 0
                else:
                    print('Something went extremely wrong')
            except ZeroDivisionError:
                print('ZeroDivisionError. Please check your code, because in this metrics should not occur division '
                      'by 0')
                return float('Inf')
        else:
            return float('Inf')

    def russell_index(self):
        if self.have_integrity():
            sum_squared_predicted_data = sum(self.predicted_data ** 2)
            sum_squared_real_data = sum(self.real_data ** 2)
            exist_rme_index = False
            exist_phase_russell = False
            try:
                rme_index = (sum_squared_predicted_data - sum_squared_real_data)\
                            / math.sqrt(sum_squared_predicted_data * sum_squared_real_data)
                exist_rme_index = True
            except ZeroDivisionError:
                print('A ZeroDivisionError has occur on the rme_index. One of the time series have all it is values '
                      'equal to zero')
                rme_index = float('Inf')
            except ValueError:
                print('A ValueError has occur. Please check the input of math.sqrt()')
                rme_index = float('Inf')
            try:
                phase_russell = (1 / math.pi) * math.acos(sum(self.predicted_data * self.real_data) /
                                                          math.sqrt(sum_squared_predicted_data * sum_squared_real_data))
                exist_phase_russell = True
            except ZeroDivisionError:
                print('A ZeroDivisionError has occur on the phase_index. One of the time series have all it is values '
                      'equal to zero')
                phase_russell = float('Inf')
            except ValueError:
                print('A ValueError has occur. Please check the input of math.sqrt() or math.acos()')
                phase_russell = float('Inf')
            if exist_phase_russell & exist_rme_index:
                magnitude_russell = np.sign(rme_index) * math.log10(1 + abs(rme_index))
                overall_russell = math.sqrt((math.pi / 4) * (magnitude_russell**2 + phase_russell**2))
                return np.array([phase_russell, magnitude_russell, overall_russell])
            else:
                return np.array([float('Inf'), float('Inf'), float('Inf')])








