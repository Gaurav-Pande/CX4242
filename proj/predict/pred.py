import numpy as np
import pandas as pd
import matplotlib.pylab as plt

import model

def main():
	flu()
	# dengue()

def flu():
	flu_countries = [
		"Argentina","Australia","Austria","Belgium","Bolivia","Brazil","Bulgaria",
		"Canada","Chile","France","Germany","Hungary","Japan","Mexico","Netherlands",
		"New Zealand","Norway","Paraguay","Peru","Poland","Romania","Russia",
		"South Africa","Spain","Sweden","Switzerland","Ukraine","United States","Uruguay"
		]

	data = pd.read_csv('flu.csv')
	data.insert(0, 'Week', range(1, 1 + len(data)))


	# ***** Show one case ***** #x
	# df = data[['Week', 'Argentina']]
	# df = df[np.isfinite(df['Argentina'])] # remove empty rows
	# df = df.rename(index=str, columns={'Argentina': "Now"})
	# df = prepare(df)
	# model.try_models(df)


	# ***** Get socres for all country ***** #
	# open('result.txt', 'w').close() # clear all the results before
	# for country in flu_countries:
	# 	print '\n\n', country, ':'
	# 	model.record_to_file('\n\n' + country + ':')
	# 	df = data[['Week', country]]
	# 	df = df[np.isfinite(df[country])] # remove empty rows
	# 	df = df.rename(index=str, columns={country: "Now"})
	# 	df = prepare(df)
	# 	model.try_models(df)






	# ***** Get predictions for all country *****#
	df = data[['Week', 'Argentina']]
	df = df[np.isfinite(df['Argentina'])] # remove empty rows
	df = df.rename(index=str, columns={'Argentina': "Now"})

	flu_pred_start_week = 660

	df_ = prepare(df, pred=True)
	# train the model using all data except for the latest record
	X = df_.iloc[:,:-1]
	y = df_.iloc[:,-1]
	X,y = model.preprocess_data(X,y)
	X_train, y_train = X[:-1], y[:-1]
	# print X_train, '\n', y_train
	lr, label = model.lr(X_train,y_train)
	model.evaluate(lr,X,y,X_train,X_train,y_train,y_train,label,graph=False)

	fea = X[-1]
	y_pred = lr.predict([fea])
	print 'features:', fea, '\npredictions:', y_pred

	# rec = pd.DataFrame([[flu_pred_start_week, y_pred]], columns=['Week','Now'])
	# print '\nbefore appending\n', df
	# df.append(rec)
	# print '\nafter appending\n', df

	# df_ = prepare(df, pred=True)
	# # train the model using all data except for the latest record
	# X = df_.iloc[:,:-1]
	# y = df_.iloc[:,-1]
	# X,y = model.preprocess_data(X,y)
	# fea = X[-1]
	# y_pred = lr.predict([fea])
	# print 'features:', fea, '\npredictions:', y_pred








	# for i in range(3):
	# 	df_ = prepare(df, pred=True)
	# 	# train the model using all data except for the latest record
	# 	X = df_.iloc[:,:-1]
	# 	y = df_.iloc[:,-1]
	# 	X,y = model.preprocess_data(X[:-1],y[:-1])
	# 	lr, label = model.lr(X,y)
	# 	model.evaluate(lr,X,y,X[:-1],X[:-1],y[:-1],y[:-1],label,graph=False)

	# 	fea = X[-1]
	# 	y_pred = lr.predict([fea])
	# 	print 'features:', fea, '\npredictions:', y_pred

	# 	rec = pd.DataFrame([[flu_pred_start_week+i, y_pred]], columns=['Week','Now'])
	# 	df.append(rec)




	# for country in flu_countries:
	# 	print '\n\n', country, ':'
	# 	df = data[['Week', country]]
	# 	df = df[np.isfinite(df[country])] # remove empty rows
	# 	df = df.rename(index=str, columns={country: "Now"})
	# 	df = prepare(df)

	# 	# train the model first
	# 	X = df.iloc[:,:-1]
	# 	y = df.iloc[:,-1]

def dengue():
	dengue_countries = [
		'Argentina','Bolivia','Brazil','India','Indonesia','Mexico','Philippines','Singapore','Thailand','Venezuela'
		]

	data = pd.read_csv('dengue.csv')
	data.insert(0, 'Week', range(1, 1 + len(data)))

	# df = data[['Week', 'Argentina']]
	# df = df[np.isfinite(df['Argentina'])] # remove empty rows
	# df = df.rename(index=str, columns={'Argentina': "Now"})
	# df = prepare(df)
	# model.try_models(df)

	# plt.plot(df)
	# plt.show()

	open('result.txt', 'w').close() # clear all the results before
	for country in dengue_countries:
		print '\n\n', country, ':'
		model.record_to_file('\n\n' + country + ':')
		df = data[['Week', country]]
		df = df[np.isfinite(df[country])] # remove empty rows
		df = df.rename(index=str, columns={country: "Now"})
		df = prepare(df)
		model.try_models(df)


def prepare(df,pred=False): # if pred, leave the last record for prediction
	# df.set_index('Date').diff()
	# change all the information to log scale
	# df['Now'] = np.log(df['Now'])

	df['1wb'] = df['Now'].shift(1)
	df['1wbd'] = df['Now'] - df['Now'].shift(1)
	df['2wb'] = df['Now'].shift(2)
	df['2wbd'] = df['Now'] - df['Now'].shift(2)
	df['3wb'] = df['Now'].shift(3)
	df['3wbd'] = df['Now'] - df['Now'].shift(3)
	df['4wb'] = df['Now'].shift(4)
	df['4wbd'] = df['Now'] - df['Now'].shift(4)
	df['4wb'] = df['Now'].shift(4)
	df['4wbd'] = df['Now'] - df['Now'].shift(4)
	df['5wb'] = df['Now'].shift(5)
	df['5wbd'] = df['Now'] - df['Now'].shift(5)
	if not pred:
		df['target'] = df['Now'].shift(-1)
		df = df.dropna()
	else:
		df = df.dropna()
		df['target'] = df['Now'].shift(-1)

	return df

if __name__ == "__main__":
	main()