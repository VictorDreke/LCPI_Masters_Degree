# transeferFuntions defines the class TransferFunctionsClass. This class describe a time series of typical linear
# transfer function of a dynamic system. In this case the inputs are:
#           k_p         -> gain the system
#           tau         -> time constant
#           zeta        -> damping factor
#           theta       -> time delay
#           selecting_order     -> used to select the order. False = First order, True = Second Order
# If you are not familiarized with this term consult the Ogata, Modern Control Theory. This class do the following
# actions:
#           transfer_function_generator     -> Checked: 06/18/2020
#           plot_transfer_function
#           step_information

import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
import math
# from scipy.integrate import odeint


class TransferFunctionsClass:
    def __init__(self, k_p, tau, zeta=0, theta=0, selecting_order=False):
        self.k_p = k_p
        self.tau = tau
        self.zeta = zeta
        self.theta = theta
        self.selecting_order = selecting_order

    def transfer_function_generator(self):
        numerator = [self.k_p]
        if self.selecting_order:
            denominator = [self.tau, 1]
        else:
            denominator = [self.tau ** 2, 2 * self.zeta * self.tau, 1]
        transfer_function = signal.TransferFunction(numerator, denominator)
        return transfer_function

    def plot_transfer_function(self, time_array_line_space, enable_ploting=False):
        time_array, output_array = signal.step(self.transfer_function_generator(), T=time_array_line_space)
        if enable_ploting:
            plt.figure(1)
            plt.plot(time_array, output_array, 'b--', linewidth=1, label='Transfer Fcn')
            # plt.show()
        return pd.Series(output_array, index=time_array, name='Predicted Model Response')

    def step_information(self, time_array_line_space, settling_criteria=0.98, rising_criteria=0.95, enable_ploting=False):
        time_series_temp = self.plot_transfer_function(time_array_line_space, enable_ploting=enable_ploting)

        settling_time_value = self.k_p * (1 - settling_criteria)
        rising_time_value_first = self.k_p * (1 - rising_criteria)
        rising_time_value_second = self.k_p * rising_criteria
        try:
            rising_time_first = time_series_temp[time_series_temp >= rising_time_value_first].index[0]
            rising_time_second = time_series_temp[time_series_temp >= rising_time_value_second].index[0]
            rising_time = rising_time_second - rising_time_first
        except IndexError:
            print('An IndexError has occur. Please check that the values of rising time are inbound the time series')
            rising_time = float('Inf')

        try:
            number_of_iteration = 1
            find_settling_time = False
            array_position = -1
            while (number_of_iteration <= len(time_series_temp)) & ~find_settling_time:
                if abs(time_series_temp.iloc[array_position] - self.k_p) <= abs(settling_time_value):
                    find_settling_time = False
                elif abs(time_series_temp.iloc[array_position] - self.k_p) > abs(settling_time_value):
                    find_settling_time = True
                    if array_position < -1:
                        settling_time = time_series_temp.index[array_position]
                    else:
                        settling_time = float('Inf')

                else:
                    print('Something went wrong. It was impossible to satisfied the settling criteria')
                array_position -= 1
                number_of_iteration += 1
        except IndexError:
            print('An IndexError has occur. Please check that the values of settling time are inbound the time series')
            settling_time = float('Inf')
        try:
            if (self.zeta > 0) & (self.zeta < 1):
                overshoot_exponent = -(self.zeta / math.sqrt(1 - self.zeta ** 2)) * math.pi
                overshoot = math.exp(overshoot_exponent) * 100
                overshoot_time = math.pi / (math.sqrt(1 - self.zeta ** 2) / self.tau)
            else:
                overshoot_time = float('Inf')
                overshoot = 0
        except ValueError:
            print('Something happen. Check the math functions')
            overshoot = float('Inf')
            overshoot_time = float('Inf')
        except ZeroDivisionError:
            print('A ZeroDivisionError has occur. Please check the value of zeta.')
            overshoot = float('Inf')
            overshoot_time = float('Inf')
        if enable_ploting:
            plt.scatter(overshoot_time, (overshoot / 100 + 1) * self.k_p, c='g', marker='x')

        return rising_time, settling_time, overshoot

    def simulated_validation_data(self, sample_time=0.1, step_time=10):
        time_array, output_array = signal.step(self.transfer_function_generator(),
                                               T=np.arange(0, step_time, sample_time))
        initial_condition_2 = np.arange(9501) * 0
        initial_condition = output_array * 0
        first_step_up = output_array
        second_step_down = first_step_up[-1] - output_array
        third_step_down = second_step_down[-1] - output_array
        four_step_up = third_step_down[-1] + output_array
        output = np.concatenate((initial_condition_2, initial_condition,
                                 first_step_up, second_step_down, third_step_down, four_step_up))
        time = np.arange(0, 17001, sample_time)
        return time, output







