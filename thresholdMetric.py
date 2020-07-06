# thresholdMetric defines the thresholdMetricClass that is used to represent the validation metric based on thresholds.
# This is child class of validationMetricClass.In this case, the inputs are the same that in validationMetricClass:
# #     predicted_data  -> representing the data predicted by the models (type pandas.Series)
# #     real_data       -> representing the data measured in the real environment (type pandas.Series)
# #     reference_data  -> representing the data of reference in the real environment (type pandas.Series). This one is
# #                         different of real_data.

# # The metrics implemented in this class are:
# #           Dvurecenska metric       -> fit_index        -> presented in Dvurecesnka, 19xx       -> Checked 06/17/2020

import math
# import pandas as pd
import numpy as np
from validationMetric import ValidationMetricClass


class ThresholdMetricClass(ValidationMetricClass):
    def __init__(self, predicted_data, real_data, reference_data):
        super().__init__(predicted_data, real_data)
        self.reference_data = reference_data

    def dvurecesnka_metric(self, calibration_uncertainty=0):
        temp_validationMetric_object = ValidationMetricClass(self.real_data, self.reference_data)
        if self.have_integrity() & temp_validationMetric_object.have_integrity():
            if not self.real_data.max() == 0:
                try:
                    squared_decomposition__uncertainty = (1 / len(self.reference_data)) * sum(
                        (self.reference_data - self.real_data)
                        ** 2)
                    total_uncertainty = math.sqrt(calibration_uncertainty ** 2 + squared_decomposition__uncertainty)
                    threshold_normalized_value = total_uncertainty / self.real_data.max()
                    error_normalized_series = abs((self.predicted_data - self.real_data) / self.real_data.max())
                    if not sum(error_normalized_series) == 0:
                        weighted_error_normalized_series = (error_normalized_series / sum(
                            error_normalized_series)) * 100
                        dvurecenska_metric_value = sum(weighted_error_normalized_series[error_normalized_series <
                                                                                        threshold_normalized_value])
                        return np.array([dvurecenska_metric_value, threshold_normalized_value])
                    else:
                        return np.array([int(100), threshold_normalized_value])

                except ZeroDivisionError:
                    print('A ZeroDivisionError has occur. Please check that the error_normalized_error is not equal to '
                          'zero')
                    return float('Inf')
                except ValueError:
                    print('A ValueError has occur. Please check that calibration is a scalar number')
                    return float('Inf')
            else:
                print('Impossible to calculated this metric, because the real data maximum value is zero. Please'
                      ' normalized your data to solve this problem')
                return float('Inf')
