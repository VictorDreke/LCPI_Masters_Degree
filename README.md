# LCPI_Masters_Degree
This repository storages an implementation of my master's degree. 
Brief explanation: 
**A decision tree predicts the quality of mathematical prediction model**. A MPC controller located in a pH Neutralization plant uses these models. Different Key Performance Index of the plant define the quality of the model. 
Important files:
-	MPC_Predictor_pH: (main file) is a Jupyter Notebook. Contains the main program. This program basically do the following functions:
  1.	Define the possible model to predict its quality using transferFunctionsClass.
  2.	Load and visualize the data from the pH Neutralization plant.
  3.	Do a model validation using known metrics. The class ThresholdMetrcisClass and DameMetricsClass are the main tool to calculate these validation metrics.
  4.	Load the trained decision tree to predict the quality of the model. This decision tree was trained using the trainingClarkePlant.py
  5.	Visualize the cross-validation result of loaded decision tree.
  6.	Predict the model quality with the decision tree.
-	MPC_Tunning_Script: is a Matlab script. **Simulate the pH Neutralization plant using a digital twin**. Allows knowing the behavior of the plant controlled by an MPC that used the proposed model.

Data repository file name:
-	'Base de Datos Tree\' contains a set of trained tree
-	'Base de Datos Planta pH\Neutralization_DataSet_H.csv' contains the data from the pH control loop
-	'Base de Datos Planta pH\Neutralization_DataSet_pH.csv' contains the data from the Level control loop
-	'pH Neutralization plant Digital Twin\1. Funciones & Scripts\2. Data\Modelo_LCPI.mat' contains the digital twin of the plant.
-  'transferFunctions.py', 'thresholdMetric.py', 'dameMetric.py' contains TransferFunctionsClass, ThresholdMetrcisClass and DameMetricsClass respectivily.
