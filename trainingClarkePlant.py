# This function  is used to carry out the training of the Machine Learning algorithm from the of the csv values.
# Decision Tree Classification

# Importing the main libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn import metrics
import pickle


# ===================================== CUSTOMIZED FUNCTION ==================================================
def handling_data_function(path_of_file, selected_features, output_name, indicated_index=0):
    # This function handles the data cleaning of the data set imported. This data set are .csv files.
    #   selected_features is a array with the name of the feature used in the training stage.
    #   output_name is the name of the column of the output desired.
    #   indicated_index is the number of the column position where the index is.
    data_set = pd.read_csv(path_of_file, index_col=indicated_index)     # Reading  .csv file and tun it in DataFrame
    data_set = data_set.replace([np.inf,  -np.inf], np.nan)     # Cleaning the data from NaN, Null and Inf values
    data_set = data_set.dropna()
    feature_input = data_set[selected_features]     # Inputs (X)
    output_target = data_set[output_name]           # Targets(Y)
    return feature_input, output_target.astype('int32')


def validation_classifier_function(real_output_target, predicted_output_target, prob_predicted_output_target):
    clarke_accuracy = metrics.accuracy_score(real_output_target, predicted_output_target)
    clarke_f1_score = metrics.f1_score(real_output_target, predicted_output_target, average=None)
    clarke_roc_auc_score = metrics.roc_auc_score(real_output_target, prob_predicted_output_target, multi_class='ovo')
    return clarke_accuracy, clarke_f1_score, clarke_roc_auc_score


def saving_the_tree_object(tree_to_be_save, validation_result, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump([tree_to_be_save, validation_result], f)


def retrieving_the_tree_object(file_name):
    with open(file_name, 'rb') as f:
        tree_saved, validation_result = pickle.load(f)
    return tree_saved, validation_result


# ====================================== LOADING DATA ========================================================
# Clarke plant initialization values
path_clarke_plant_csv_file = 'Base de Datos Planta pH/Clarke_DataSet.csv'
features_clarke_plant = ['Willmott', 'Russell_Pr', 'Dvure', 'Anova', 'N_nAIC', 'V_Tr', 'V_Ts', 'V_Mp']
target_name_column = 'ID_norm'
# Level control loop initialization values
path_level_loop_csv_file = 'Base de Datos Planta pH/Neutralization_DataSet_H.csv'
features_level_loop = ['TIC', 'Willmott', 'Russell_Pr', 'Dvure', 'V_Tr', 'V_Ts', 'V_Mp']
# pH control loop initialization values
path_ph_loop_csv_file = 'Base de Datos Planta pH/Neutralization_DataSet_pH.csv'
features_ph_loop = ['TIC', 'Willmott', 'Russell_Pr', 'Dvure', 'V_Tr', 'V_Ts', 'V_Mp']
# Loading ...
feature_input_x, output_target_y = handling_data_function(
    path_of_file=path_ph_loop_csv_file, selected_features=features_ph_loop, output_name=target_name_column)


# ======================================= SPLITTING DATA ===================================================
# Splitting the dataset into the Training and Test set (30 % of the Dataset)
test_percentage = 30
test_percentage = test_percentage/100

train_x_feature, test_x_feature, train_y_target, test_y_target = \
    train_test_split(feature_input_x, output_target_y, test_size=test_percentage, random_state=0)

# ======================================= FEATURE SCALING ==================================================
# Feature Scaling (In this case,it is not need it)
# from sklearn.preprocessing import StandardScaler
# sc = StandardScaler()
# x_train = sc.fit_transform(x_train)
# x_test = sc.transform(x_test)

# ======================================= HYPERPARAMETER TUNING =============================================
# Setup the parameter and distributions to sample from: param_dist
param_dist = {
    "max_depth": [20, 30, 35],  # 40, 45, 50, None],
    "min_samples_leaf": np.arange(10, 50, 1),
    "criterion": ['gini', 'entropy']
}

# Instantiate a Decision Tree Classifier: tree
# Instantiate the RandomizedSearchCv or SearchGridCV object: tree_cv
tree_classifier = RandomizedSearchCV(tree.DecisionTreeClassifier(), param_distributions=param_dist, cv=5, n_iter=60)

# ======================================= Fitting Classifier ================================================
# Fitting classifier to the training set
tree_classifier.fit(train_x_feature, train_y_target)

# ====================================== Predicting =========================================================
# Predicting the Test set result
prediction_target_y = tree_classifier.best_estimator_.predict(test_x_feature)
prediction_probability_target_y = tree_classifier.best_estimator_.predict_proba(test_x_feature)

# ====================================== Validation Visualization ===========================================
# Making the confusion Matrix
accuracy, f1_score, roc_auc = validation_classifier_function(test_y_target,
                                                             prediction_target_y, prediction_probability_target_y)
metrics.plot_confusion_matrix(tree_classifier.best_estimator_, test_x_feature, test_y_target, labels=None)
cm = metrics.confusion_matrix(test_y_target, prediction_target_y)
print(accuracy, f1_score, roc_auc)
print('\n')
print(pd.DataFrame(tree_classifier.cv_results_)[['param_max_depth', 'param_min_samples_leaf', 'mean_test_score']])
print('\n')
print(tree_classifier.best_params_)
print('\n')
wait = input('Write c\n')
if wait == 'c':
    plt.show()
wait = input('Write c\n')
if wait == 'c':
    file_name_new = input('Insert the name of the file: \n')
    saving_the_tree_object(tree_classifier.best_estimator_, [accuracy, f1_score, roc_auc, cm], file_name=file_name_new)
else:
    temp, temp2 = retrieving_the_tree_object('Base de Datos Tree/Trained_Tree_ph')
    print(temp2)

# plt.show()


