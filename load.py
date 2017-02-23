import pandas as pd

def load():
	# create a timerange you are interested in
	periods = pd.date_range('2017-02-10', '2017-02-17', freq='4H')
	# create an empty dataframe with dates as index
	df = pd.DataFrame(index=periods)
	# load data from json
	dfBTC = pd.read_json('./btc_usd.json', orient='records')
	# change index column of the new dataframe
	dfBTC.set_index('date', inplace=True)

	# drop not needed columns
	# dfBTC = dfBTC.drop('open', 1)
	dfBTC = dfBTC.drop('quoteVolume', 1)
	dfBTC = dfBTC.drop('volume', 1)
	dfBTC = dfBTC.drop('weightedAverage', 1)

	# join the two dataframes to only keep dates in df (left join)
	df = df.join(dfBTC)

	return df