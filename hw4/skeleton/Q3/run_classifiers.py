## Data and Visual Analytics - Homework 4
## Georgia Institute of Technology
## Applying ML algorithms to recognize seizure from EEG brain wave signals

import numpy as np
import pandas as pd
import time 

from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier

######################################### Reading and Splitting the Data ###############################################

# Read in all the data.
data = pd.read_csv('seizure_dataset.csv')

# Separate out the x_data and y_data.
x_data = data.loc[:, data.columns != "y"]
y_data = data.loc[:, "y"]

# The random state to use while splitting the data. DO NOT CHANGE.
random_state = 100 # DO NOT CHANGE

# XXX
# TODO: Split each of the features and labels arrays into 70% training set and
#       30% testing set (create 4 new arrays). Call them x_train, x_test, y_train and y_test.
#       Use the train_test_split method in sklearn with the paramater 'shuffle' set to true 
#       and the 'random_state' set to 100.
# XXX



# ############################################### Linear Regression ###################################################
# XXX
# TODO: Create a LinearRegression classifier and train it.
# XXX

# XXX
# TODO: Test its accuracy (on the testing set) using the accuracy_score method.
# Note: Use y_predict.round() to get 1 or 0 as the output.
# XXX


# ############################################### Multi Layer Perceptron #################################################
# XXX
# TODO: Create an MLPClassifier and train it.
# XXX


# XXX
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX




# ############################################### Random Forest Classifier ##############################################
# XXX
# TODO: Create a RandomForestClassifier and train it.
# XXX


# XXX
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX

# XXX
# TODO: Tune the hyper-parameters 'n_estimators' and 'max_depth' 
#       and select the combination that gives the best testing accuracy.
#       After fitting, print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX


# ############################################ Support Vector Machine ###################################################
# XXX
# TODO: Create a SVC classifier and train it.
# XXX

# XXX
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX

# XXX
# TODO: Tune the hyper-parameters 'C' and 'kernel' (use rbf and linear) 
#       and select the set of parameters that gives the best testing accuracy.
#       After fitting, print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX


# XXX 
# ########## PART C ######### 
# TODO: Print your CV's best mean testing accuracy and its corresponding mean training accuracy and mean fit time.
# 		State them in report.txt
# XXX

