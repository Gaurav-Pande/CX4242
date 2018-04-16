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
from sklearn.preprocessing import MinMaxScaler

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
X_train,X_test,y_train,y_test = train_test_split(x_data,y_data, test_size=0.30, shuffle=True, random_state=random_state)
# XXX



# ############################################### Linear Regression ###################################################
# XXX
# TODO: Create a LinearRegression classifier and train it.
lr = LinearRegression(fit_intercept=True, normalize=False, copy_X=True, n_jobs=1)
lr.fit(X_train,y_train)
# XXX

# XXX
# TODO: Test its accuracy (on the testing set) using the accuracy_score method.
# Note: Use y_predict.round() to get 1 or 0 as the output.
y_predict = lr.predict(X_train)
y_predict = y_predict.round()
accu = accuracy_score(y_train, y_predict)
print "Linear Regression Training Accuracy:", accu

y_predict = lr.predict(X_test)
y_predict = y_predict.round()
accu = accuracy_score(y_test, y_predict)
print "Linear Regression Testing Accuracy:", accu
# XXX


# ############################################### Multi Layer Perceptron #################################################
# XXX
# TODO: Create an MLPClassifier and train it.
nn = model = MLPClassifier(activation='relu', alpha=1e-05, batch_size='auto',beta_1=0.9, beta_2=0.999, early_stopping=False,epsilon=1e-08, hidden_layer_sizes=(100,), learning_rate='constant',learning_rate_init=0.02, max_iter=200, momentum=0.9,nesterovs_momentum=True, power_t=0.5, random_state=1, shuffle=True,solver='lbfgs', tol=0.0001, validation_fraction=0.1, verbose=False,warm_start=False)
nn.fit(X_train, y_train)
# XXX


# XXX
# TODO: Test its accuracy on the test set using the accuracy_score method.
y_predict = nn.predict(X_train)
y_predict = y_predict.round()
accu = accuracy_score(y_train, y_predict)
print "Neural Network Training Accuracy:", accu

y_predict = nn.predict(X_test)
y_predict = y_predict.round()
accu = accuracy_score(y_test, y_predict)
print "Neural Network Testing Accuracy:", accu
# XXX




# ############################################### Random Forest Classifier ##############################################
# XXX
# TODO: Create a RandomForestClassifier and train it.
rf = RandomForestClassifier(n_estimators=10, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None, bootstrap=True, oob_score=False, n_jobs=1, random_state=None, verbose=0, warm_start=False, class_weight=None)
rf.fit(X_train, y_train)
# XXX


# XXX
# TODO: Test its accuracy on the test set using the accuracy_score method.
y_predict = rf.predict(X_train)
y_predict = y_predict.round()
accu = accuracy_score(y_train, y_predict)
print "Random Forest Training Accuracy:", accu

y_predict = rf.predict(X_test)
y_predict = y_predict.round()
accu = accuracy_score(y_test, y_predict)
print "Random Forest Testing Accuracy:", accu
# XXX

# XXX
# TODO: Tune the hyper-parameters 'n_estimators' and 'max_depth'
#       and select the combination that gives the best testing accuracy.
#       After fitting, print the best params, using .best_params_, and print the best score, using .best_score_.
parameters = {'n_estimators':[3, 5, 10, 15, 20], 'max_depth':[5, 10, 20]} # n_estimators: num of trees in the forest
clf = GridSearchCV(rf, parameters, cv=10)
clf.fit(x_data, y_data)
print "Best Params:", clf.best_params_, "Best Score:", clf.best_score_
# XXX


# ############################################ Support Vector Machine ###################################################
# XXX
# TODO: Create a SVC classifier and train it.
svm = SVC(C=1.0, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape='ovr', random_state=None)
svm.fit(X_train, y_train)
# XXX

# XXX
# TODO: Test its accuracy on the test set using the accuracy_score method.
y_predict = svm.predict(X_train)
y_predict = y_predict.round()
accu = accuracy_score(y_train, y_predict)
print "Support Vector Machine Training Accuracy:", accu

y_predict = svm.predict(X_test)
y_predict = y_predict.round()
accu = accuracy_score(y_test, y_predict)
print "Support Vector Machine Testing Accuracy:", accu
# XXX

# XXX
# TODO: Tune the hyper-parameters 'C' and 'kernel' (use rbf and linear)
#       and select the set of parameters that gives the best testing accuracy.
#       After fitting, print the best params, using .best_params_, and print the best score, using .best_score_.
minmax = MinMaxScaler()
x_data_p = minmax.fit(x_data).transform(x_data)
parameters = {'kernel':('linear', 'rbf'), 'C':[0.01, 0.1, 1, 10]} # C: penalty parameter C of the error term
clf = GridSearchCV(svm, parameters, cv=10)
clf.fit(x_data_p, y_data)
print "Best Params:", clf.best_params_, "Best Score:", clf.best_score_
# XXX


# XXX
# ########## PART C #########
# TODO: Print your CV's best mean testing accuracy and its corresponding mean training accuracy and mean fit time.
# 		State them in report.txt
print clf.cv_results_['mean_test_score']
print clf.cv_results_['mean_train_score']
print clf.cv_results_['mean_fit_time']
# XXX

