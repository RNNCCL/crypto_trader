import pandas as pd

periods = pd.date_range('2016-01-01', '2017-01-01', freq='4H')
df = pd.DataFrame(index=periods)
dfBTC = pd.read_json('./btc_usd.json', orient='records')
dfBTC.set_index('date', inplace=True)

df = df.join(dfBTC)