import numpy as np
import pandas as pd
import matplotlib.pylab as plt

import model
flu_countries = [
	"Argentina","Australia","Austria","Belgium","Bolivia","Brazil","Bulgaria",
	"Canada","Chile","France","Germany","Hungary","Japan","Mexico","Netherlands",
	"New Zealand","Norway","Paraguay","Peru","Poland","Romania","Russia",
	"South Africa","Spain","Sweden","Switzerland","Ukraine","United States","Uruguay"
	]

flu_pred_start_week = 660

dengue_countries = [
	'Argentina','Bolivia','Brazil','India','Indonesia','Mexico','Philippines','Singapore','Thailand','Venezuela'
	]

dengue_pred_start_week = 658

def main():
	# flu()
	dengue()

def flu():
	data = pd.read_csv('flu.csv')
	data.insert(0, 'Week', range(1, 1 + len(data)))
	pred(data, flu_countries, flu_pred_start_week)

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


def dengue():

	data = pd.read_csv('dengue.csv')
	data.insert(0, 'Week', range(1, 1 + len(data)))
	pred(data, dengue_countries, dengue_pred_start_week)

	# df = data[['Week', 'Argentina']]
	# df = df[np.isfinite(df['Argentina'])] # remove empty rows
	# df = df.rename(index=str, columns={'Argentina': "Now"})
	# df = prepare(df)
	# model.try_models(df)

	# plt.plot(df)
	# plt.show()

	# open('result.txt', 'w').close() # clear all the results before
	# for country in dengue_countries:
	# 	print '\n\n', country, ':'
	# 	model.record_to_file('\n\n' + country + ':')
	# 	df = data[['Week', country]]
	# 	df = df[np.isfinite(df[country])] # remove empty rows
	# 	df = df.rename(index=str, columns={country: "Now"})
	# 	df = prepare(df)
	# 	model.try_models(df)


def pred(data, countries, start):
	# ***** Get predictions for all country *****#
	open('predictions.txt', 'w').close()
	for country in countries:
		record_predictions('\n' + country + ':')
		print '\n', country, ':'
		df = data[['Week', country]]
		df = df[np.isfinite(df[country])] # remove empty rows
		df = df.rename(index=str, columns={country: "Now"})

		for i in range(3):
			df_ = df.copy()
			df_ = prepare(df_, pred=True)
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
			print 'features:', fea, '\npredictions:', y_pred[0]
			record_predictions(str(y_pred[0]))

			rec = pd.DataFrame([[start+i, y_pred[0]]], columns=['Week','Now'])
			# print '\nbefore appending\n', df
			df = df.append(rec)
			# print '\nafter appending\n', df


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

def record_predictions(line):
	with open('predictions.txt', 'a') as fhand:
		fhand.write(line+'\n')

if __name__ == "__main__":
	main()