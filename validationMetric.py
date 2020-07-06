# validationMetrics defines the class validationMetricClass that it is used to describe a generic Validation Metric
# As all validation metrics we have to variable: the predicted data -> predicted_data and  the real data -> real_data
# The real data also called observed data is obtained by measurements and it is the reference. In this both input
# variables  have to be a pandas.Series type
# Check done 06/16/2020

# import numpy as np
import pandas as pd
import math


class ValidationMetricClass:
    def __init__(self, predicted_data, real_data):
        self.predicted_data = predicted_data        # predicted_data stands for the predicted by the models
        self.real_data = real_data                  # real_data stands for the measured and stored data

    # The method is_a_eries checks that both predicted_data and real_data are pandas.Series type
    # Check date 06/16/2020
    def is_a_series(self):
        if isinstance(self.predicted_data, pd.Series) & isinstance(self.real_data, pd.Series):
            return True
        elif (not(isinstance(self.predicted_data, pd.Series))) & (not(isinstance(self.real_data, pd.Series))):
            print('Neither variables  are not a pandas.Series type\n')
            return False
        elif not(isinstance(self.real_data, pd.Series)):
            print('The variable real_data is not a pandas.Series type\n')
            return False
        else:
            print('The variable predicted_data is not a pandas.Series type \n')
            return False

    # All the validation metrics have to used time series with the same length; therefore, this is verified on this
    # function
    # Check done 06/16/2020
    def have_same_length(self):
        if self.is_a_series():
            if self.real_data.shape == self.predicted_data.shape:

                return True
            else:
                print('The time series does not have the same length\n')
                return False
        else:
            return False

    # All the Time Series have to have a monotonic increasing and the values have to be numerical. Therefore, function
    # checks these two conditions be true
    def is_a_time_series(self):
        if self.is_a_series() & self.have_same_length():
            if (not self.real_data.index.is_monotonic_increasing) | (not self.predicted_data.index.is_monotonic_increasing):
                print('One of the inputs is not a monotonic increasing time series\n')
                return False
            elif (self.real_data.dtype == object) | (self.predicted_data.dtype == object):
                print('One of the inputs has not numerical values in the array\n')
                return False
            else:
                return True
        else:
            print('The inputs are not time series with the same length\n')
            return False

    # Finally, it is checked the integrity of the data. To do the validation of a time series this one can not have Null
    # Inf or other strange values, and obviously have to fulfill the others conditions evaluated.
    def have_integrity(self):
        if self.is_a_series() & self.have_same_length() & self.is_a_time_series():
            for value_is_null in self.predicted_data.isnull():
                if value_is_null:
                    print('The predicted_data has NULL values\n')
                    return False

                # The line before means: return False is predicted_data has null values
            for value_is_null in self.real_data.isnull():
                if value_is_null:
                    print('The real_data has NULL values\n')
                    return False

            # The line before means: return False is real_data has null values

            # After verifies that both predicted_data and real_data have not null values
            # It is checked that does not have NaN or Inf; therefore is a finite number
            for value_is_finite in self.predicted_data:
                if not math.isfinite(value_is_finite):
                    print('The predicted data has Inf values\n')
                    return False
                # The line before means that the predicted_data have infinite values
            for values_is_finite in self.real_data:
                if not math.isfinite(value_is_finite):
                    print('The real data has Inf values\n')
                    return False
            # Finally, is neither of aforementioned conditions are met then the data have requested conditions
            return True
        else:
            print('Check the others conditions of correct time series for validation')
            return False







