import pandas as pd
import matplotlib.pyplot as plt
from indicators import MACD

# create a timerange you are interested in
periods = pd.date_range('2017-02-14', '2017-02-17', freq='4H')
# create an empty dataframe with dates as index
df = pd.DataFrame(index=periods)
# load data from json
dfBTC = pd.read_json('./btc_usd.json', orient='records')
# change index column of the new dataframe
dfBTC.set_index('date', inplace=True)

# df = df.join(dfBTC)

df = MACD(dfBTC, 12, 26)
df.set_index('date', inplace=True)

df['close'].plot()
plt.show()

print df

# plot chart
# ax = df['close'].plot()

# plt.show()