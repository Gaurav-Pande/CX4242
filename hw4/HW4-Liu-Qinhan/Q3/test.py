import numpy as np
import pandas as pd
import time

from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler

data = pd.read_csv('seizure_dataset.csv')

# Separate out the x_data and y_data.
x_data = data.loc[:, data.columns != "y"]
y_data = data.loc[:, "y"]

# The random state to use while splitting the data. DO NOT CHANGE.
random_state = 100 # DO NOT CHANGE
X_train,X_test,y_train,y_test = train_test_split(x_data,y_data, test_size=0.30, shuffle=True, random_state=random_state)

# start = time.time()

# print "Start Grid Search"
# parameters = {'n_estimators':[5, 10], 'max_depth':[5, 10, 20]} # n_estimators: num of trees in the forest
# clf = GridSearchCV(rf, parameters, cv=10)
# clf.fit(x_data, y_data)
# print "Best Params:", clf.best_params_, "Best Score:", clf.best_score_
# end = time.time()
# print "Time spent:", end-start


svm = SVC(C=1.0, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape='ovr', random_state=None)
svm.fit(X_train, y_train)

start = time.time()
y_predict = svm.predict(X_test)
y_predict = y_predict.round()
accu = accuracy_score(y_test, y_predict)
print "Support Vector Machine Testing Accuracy:", accu

end = time.time()
print "Time spent:", end-start
print 80*(end-start)

# exit()

start = time.time()

print "Start Grid Search"

minmax = MinMaxScaler()
x_data_p = minmax.fit(x_data).transform(x_data)
print x_data_p
parameters = {'kernel':('linear', 'rbf'), 'C':[0.01, 0.1, 1, 10]} # C: penalty parameter C of the error term
clf = GridSearchCV(svm, parameters, cv=10)
clf.fit(x_data_p, y_data)
print "Best Params:", clf.best_params_, "Best Score:", clf.best_score_

end = time.time()
print "Time spent:", end-start
