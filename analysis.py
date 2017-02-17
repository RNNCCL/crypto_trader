import pandas as pd

# create a timerange you are interested in
periods = pd.date_range('2016-01-01', '2017-01-01', freq='4H')
# create an empty dataframe with dates as index
df = pd.DataFrame(index=periods)
# load data from json
dfBTC = pd.read_json('./btc_usd.json', orient='records')
# change index column of the new dataframe
dfBTC.set_index('date', inplace=True)

#join empty and loaded dataframes to end up with loaded data only for timerange of interest
df = df.join(dfBTC)