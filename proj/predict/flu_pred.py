import numpy as np
import pandas as pd
import matplotlib.pylab as plt

import model

def main():
	# dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d')
	# data = pd.read_csv('flu_data.csv', parse_dates=['Date'], index_col='Date',date_parser=dateparse)
	# print data.head()
	# print data.dtypes
	# print data.index
	countries = [
		"Argentina","Australia","Austria","Belgium","Bolivia","Brazil","Bulgaria",
		"Canada","Chile","France","Germany","Hungary","Japan","Mexico","Netherlands",
		"New Zealand","Norway","Paraguay","Peru","Poland","Romania","Russia",
		"South Africa","Spain","Sweden","Switzerland","Ukraine","United States","Uruguay"
		]

	data = pd.read_csv('flu_data.csv')
	data.insert(0, 'Week', range(1, 1 + len(data)))

	us = data[['Week', 'United States']]
	us = us[np.isfinite(us['United States'])] # remove empty rows
	model.nn(us)
	model.knn(us)
	model.svm(us)
	model.lr(us)

	# fr = data[['Week', 'France']]
	# fr = fr[np.isfinite(fr['France'])]
	# model.neural_network(fr)

	# plt.plot(us)
	# plt.show()



def prepare(df):
	df = df.rename(index=str, columns={"United States": "Now", "C": "c"})
	# df.set_index('Date').diff()
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
	df['target'] = df['Now'].shift(-1)
	df = df.dropna()

	return df

if __name__ == "__main__":
	main()