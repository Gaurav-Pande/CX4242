import sys
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt		# For plotting the data

##### Preprocessing #####
from sklearn.preprocessing import StandardScaler

##### Model Selection #####

## Cross Validation ##
from sklearn.model_selection import ShuffleSplit
from sklearn.cross_validation import train_test_split

## Models ##
from sklearn.neural_network import MLPClassifier	# For Neural Network
from sklearn.neighbors import KNeighborsClassifier	# For Support Vector Machine
from sklearn.svm import SVC, NuSVC, LinearSVC	# For Support Vector Machine
from sklearn.linear_model import LinearRegression	# For Linear Regression

## Plots ##
from sklearn.model_selection import learning_curve

## Model Evaluation ##
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score

# Regression #
from sklearn.metrics import explained_variance_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import r2_score

Random_State = 5
# TITLE = "Learning Curve (Neural Network)"
ARCHI = (100,)
N_NEI = 10

def nn(df):
	X = df.iloc[:,:-1]
	y = df.iloc[:,-1]
	X = preprocess_data(X)
	X_train,X_test,y_train,y_test = train_test_split(X,y, random_state=Random_State)
	# X_train,X_test = preprocess_feature(X_train,X_test)

	model = MLPClassifier(activation='relu', alpha=1e-05, batch_size='auto',beta_1=0.9, beta_2=0.999, early_stopping=False,epsilon=1e-08, hidden_layer_sizes=ARCHI, learning_rate='constant',learning_rate_init=0.02, max_iter=200, momentum=0.9,nesterovs_momentum=True, power_t=0.5, random_state=1, shuffle=True,solver='lbfgs', tol=0.0001, validation_fraction=0.1, verbose=False,warm_start=False)
	model = fit_model(model,X_train,y_train,X_test,y_test)
	label = "Neural Net-L=0.02,L" + str(ARCHI)
	# learn_cur(model,TITLE,X,y,label)
	pred = model.predict(X)
	evaluate(y,pred)
	plot_curve(y,pred,label)
	# plot_against(y,pred,label)

def knn(df):
	X = df.iloc[:,:-1]
	y = df.iloc[:,-1]
	X = preprocess_data(X)
	X_train,X_test,y_train,y_test = train_test_split(X,y, test_size=0.33, random_state=Random_State)
	# X_train,X_test = preprocess_feature(X_train,X_test)

	model = KNeighborsClassifier(n_neighbors=N_NEI)
	model = fit_model(model,X_train,y_train,X_test,y_test)
	label = "KNN-Neighbors " + str(N_NEI)

	pred = model.predict(X)
	evaluate(y,pred)
	plot_curve(y,pred,label)

def svm(df):
	X = df.iloc[:,:-1]
	y = df.iloc[:,-1]
	X = preprocess_data(X)
	X_train,X_test,y_train,y_test = train_test_split(X,y, random_state=Random_State)
	# X_train,X_test = preprocess_feature(X_train,X_test)

	model = LinearSVC(multi_class = 'ovr')
	model = fit_model(model,X_train,y_train,X_test,y_test)
	label = "SVM"

	pred = model.predict(X)
	evaluate(y,pred)
	plot_curve(y,pred,label)

def lr(df):
	X = df.iloc[:,:-1]
	y = df.iloc[:,-1]
	X = preprocess_data(X)
	X_train,X_test,y_train,y_test = train_test_split(X,y, random_state=Random_State)
	# X_train,X_test = preprocess_feature(X_train,X_test)

	model = LinearRegression(fit_intercept=True, normalize=False, copy_X=True, n_jobs=1)

	model = fit_model(model,X_train,y_train,X_test,y_test)
	label = "Linear Regression"

	pred = model.predict(X)
	evaluate(y,pred)
	plot_curve(y,pred,label)

def evaluate(ytrue,ypred):

	print "Explained Variance Score:\t",explained_variance_score(ytrue, ypred)
	print "Mean Absolute Error:\t",mean_absolute_error(ytrue, ypred)
	print "Mean Squared Error:\t",mean_squared_error(ytrue, ypred)
	print "Mean Squared Log Error:\t", mean_squared_log_error(ytrue, ypred)
	print "R2 Score:\t",r2_score(ytrue, ypred)

def plot_curve(tar,pred,label):
	plt.figure()
	plt.title(label)

	plt.xlabel("Weeks")
	plt.ylabel("Flu Influenza Activity")
	# x values
	x_values = np.arange(1,tar.shape[0],1)

	plt.plot(tar, '--', color="r", label="Real Value")
	plt.plot(pred, '--', color="b", label="Predicted Value")

	plt.legend(loc="best")
	print "Check out the graph popped up"
	plt.show()

def plot_against(tar,pred,label):
	plt.figure()
	plt.title(label)

	plt.xlabel("Targets")
	plt.ylabel("Predictions")
	plt.plot(tar,pred, '-o', color="b")

	print "Check out the graph popped up"
	plt.show()

def preprocess_data(X):
	scaler = StandardScaler().fit(X)
	return scaler.transform(X)

def preprocess_feature(X_train,X_test):
	# Preprocess the Features
	scaler = StandardScaler().fit(X_train)
	X_train = scaler.transform(X_train)	# Rescale the data
	X_test = scaler.transform(X_test)
	return X_train,X_test


def score_model(model,X,y):
	cv_scores = cross_val_score(model,X,y,cv=Random_State)
	print "Cross Validation Scores:"
	print cv_scores


def fit_model(model,X_train,y_train,X_test,y_test):
	print "Training size:\t"
	print X_train.shape[0]
	model.fit(X_train,y_train)
	# accu = accuracy_score(y_test,model.predict(X_test))
	# print "Accuracy: \t", accu

	return model


def learn_cur(model, title, X, y, label=None, ylim=None, cv=None, n_jobs=1, train_sizes=np.linspace(.1, 1.0, 10)):
								# ylim : tuple, shape (ymin, ymax), optional. Defines minimum and maximum yvalues plotted.

	# Cross validation with 100 iterations to get smoother mean test and train
	# score curves, each time with 20% data randomly selected as a validation set.
	cv = ShuffleSplit(n_splits=10, test_size=0.2, random_state=0)

	plt.figure()
	plt.title(title + label)
	if ylim is not None:
		plt.ylim(*ylim)
	plt.xlabel("Training examples ")
	plt.ylabel("Score")
	train_sizes, train_scores, test_scores = learning_curve(
		model, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
	train_scores_mean = np.mean(train_scores, axis=1)
	train_scores_std = np.std(train_scores, axis=1)
	test_scores_mean = np.mean(test_scores, axis=1)
	test_scores_std = np.std(test_scores, axis=1)
	plt.grid()

	plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
					 train_scores_mean + train_scores_std, alpha=0.1,
					 color="r")
	plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
					 test_scores_mean + test_scores_std, alpha=0.1, color="g")
	plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
			 label="Training score")
	plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
			 label="Cross-validation score")

	plt.legend(loc="best")

	return plt

if __name__ == '__main__':
	# df = data_loader.load_data(sys.argv[1]) # argv[1] is the file storing the dataset
	# neural_network(df)
	print "nn.py not for direct usage"