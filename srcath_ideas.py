import pandas as pd
import numpy as np
from sklearn import tree
import pickle

from scipy.integrate import odeint
# from validationMetric import ValidationMetricClass
# from dameMetric import DameMetricClass
# from thresholdMetric import ThresholdMetricClass
# import math
from transferFunctions import TransferFunctionsClass
# from scipy import signal
import matplotlib.pyplot as plt
import graphviz
from graphviz import  Source
import pydotplus

try:
    temp_time_series_1 = pd.Series(np.arange(3))
    temp_time_series_2 = pd.Series(np.array([3, 1, 1]))
    temp_time_series_3 = pd.Series(np.array([1, 1, 1]))
except ZeroDivisionError:
    print('la cagastes')

t = TransferFunctionsClass(tau=0.1, k_p=3, zeta=0.6)
# plt.figure(1)
# # tr = t.plot_transfer_function(np.arange(1000)*0.1, enable_ploting=False)
#
# # print(t.step_information(np.arange(100)*0.1)[2:4])
# # print(t.step_information(np.arange(30000)*0.1, rising_criteria=0.95, enable_ploting=True))
# t, y = t.simulated_validation_data(step_time=1500, sample_time=1)
# print('len(t): ' + str(len(t)) + '\nlen(y): ' + str(len(y)))
# plt.plot(t, y)
# plt.show()
# Kp = 3
# taup = 2
#
#
# def model3(y, t):
#     u = 2
#     return (-y + Kp * u) / taup
#
#
# t3 = np.linspace(0, 14, 100)
# y3 = odeint(model3, 0, t3)
# plt.plot(t3, y3, 'r-', linewidth=2)
# plt.show()
with open('Tree_Trained_pH_4', 'rb') as f:
    tree_saved, validation_result = pickle.load(f)


graph = Source(tree.export_graphviz(
    tree_saved,
    out_file=None,
    feature_names=['TIC', 'Willmott', 'Russell_Pr', 'Dvure', 'V_Tr', 'V_Ts', 'V_Mp'],
    class_names=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'Z']
))
graph.format = 'png'
graph.render('dt_render', view=True)
png_bytes = graph.pipe(format='png')
with open('dtree_pipe.png', 'wb') as f:
    f.write(png_bytes)
