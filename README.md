Crypto trader is a price predictor project for Bitcoins

Usage:

Data points:

Run 
```
python get_data.py 
```

to get json data points from poloniex and save them in a file (modify get_data.py to get desired timeframe/crypto_pair).

You can also import other json datapoints which have the following form:

```
[
{
open: 1.000
close: 1.000
high: 1.000
low: 1.000
volume: 1.000
}
...
]
```

Add custom inidcators:

You can add custom indicators in indicators.py. Follow the function_name(df, *args) -> return df with one new column that represents the indicator.
Don't forget to add function to indicator list

Run statistics:

Open learn_bitcoin notebook and run cells.
