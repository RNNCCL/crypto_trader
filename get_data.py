import urllib2

res = urllib2.urlopen('https://poloniex.com/public?command=returnChartData&currencyPair=USDT_BTC&start=1405699200&end=9999999999&period=14400')
data = res.read()

f = open('btc_usd.json', 'w')
f.write(data)
f.close()