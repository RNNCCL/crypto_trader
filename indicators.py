import pandas as pd
import numpy as np


def wilder_smooth(value_list, period):
	nan_offset = np.isnan(value_list).sum()
	smoothened = [np.nan for i in range(period-1+nan_offset)]
	smoothened.append(np.mean(value_list[nan_offset:period+nan_offset]))
	for i in range(period+nan_offset, len(value_list)):
		smoothened.append(smoothened[i-1] + (value_list[i] - smoothened[i-1]) / period)
	return np.array(smoothened)


def MA(df, period):
	mean = df['close'].rolling(period).mean().to_frame(name='mean_{}'.format(period))
	return df.join(mean)


def EMA(df, period):
	mean = df['close'].ewm(span=period, min_periods=period-1).mean().to_frame(name='ema_{}'.format(period))
	return df.join(mean)


def MOM(df, period):
	momentum = (df['close'].diff(period)).to_frame(name='moment_{}'.format(period))
	return df.join(momentum)


def ROC(df, period):
	roc = (df['close'] / df['close'].shift(period)).to_frame(name='roc_{}'.format(period))
	return df.join(roc)


def BBANDS(df, period, std_off):
	boil_mean = df['close'].rolling(period).mean().to_frame(name='boil_mean_{}_{}'.format(period, std_off))
	boil_std = df['close'].rolling(period).std().to_frame(name='boil_std_{}_{}'.format(period, std_off))

	boil_up = (boil_mean['boil_mean_{}_{}'.format(period, std_off)] + std_off*boil_std['boil_std_{}_{}'.format(period, std_off)]).to_frame(name='boil_up_{}_{}'.format(period, std_off))
	boil_down = (boil_mean['boil_mean_{}_{}'.format(period, std_off)] - std_off*boil_std['boil_std_{}_{}'.format(period, std_off)]).to_frame(name='boil_down_{}_{}'.format(period, std_off))

	df = df.join(boil_mean)
	df = df.join(boil_up)
	df = df.join(boil_down)

	return df

def normalizedBBands(df, period, std_off):
	boil_mean = df['close'].rolling(period).mean().values
	boil_std = df['close'].rolling(period).std().values

	boil_up = boil_mean + std_off*boil_std
	boil_down = boil_mean - std_off*boil_std

	df['normBB'] = 0

	df['normBB'] = (df[df['close'].values > boil_up]['close'] / boil_up[df['close'].values > boil_up]).to_frame(name='normBB')
	df['normBB'] = (df[df['close'].values < boil_down]['close'] / boil_down[df['close'].values < boil_down]).to_frame(name='normBB')

	return df


def RSI(df, period):
	rsi = (100.0 - 100.0 / (1.0 + df['close'].diff(1).gt(0).rolling(period).mean() / df['close'].diff(1).lt(0).rolling(period).mean())).to_frame(name='rsi_{}'.format(period))

	return df.join(rsi)


def STOCHASTICS(df, period, smooth):
	stoch_k = (100.0 * (df['close'] - df['low'].rolling(period).min()) / (df['high'].rolling(period).max() - df['low'].rolling(period).min())).to_frame(name='stoch_k_{}'.format(period))
	stoch_d = stoch_k['stoch_k_{}'.format(period)].rolling(smooth).mean().to_frame(name='stoch_d_{}_{}'.format(period, smooth))

	df = df.join(stoch_k)
	df = df.join(stoch_d)

	return df


def MACD(df, period_fast, period_slow, smooth):
	macd = df['close'].ewm(span=period_fast, min_periods=period_fast-1).mean() - df['close'].ewm(span=period_slow, min_periods=period_slow-1).mean()
	macd_smoothed = macd_diff.ewm(smooth).mean()

	macd_hist = (macd - macd_smoothed).to_frame(name='macd_{}_{}_{}'.format(period_fast, period_slow, smooth))

	return df.join(macd_hist)


def ATR(df, period):
	TR = pd.concat([df['high'], df['close'].shift(1)], 1).max(1) - pd.concat([df['low'], df['close'].shift(1)], 1).min(1)
	ATR = TR.rolling(period).mean().to_frame(name='atr_{}'.format(period))
	return df.join(ATR)


def ADX(df, period):
	TR = pd.concat([df['high'], df['close'].shift(1)], 1).max(1) - pd.concat([df['low'], df['close'].shift(1)], 1).min(1)
	df['ATR'] = wilder_smooth(TR, period)
	# ATR = TR.rolling(period).mean()

	up_down = df['high'].diff(1).gt(-1*df['low'].diff(1))

	pDM = df['high'].diff(1) * df['high'].diff(1).gt(0) * up_down
	mDM = df['low'].diff(1) * df['low'].diff(1).lt(0) * (up_down - 1)

	pDI = 100 * wilder_smooth(pDM.values, period) / df['ATR']
	mDI = 100 * wilder_smooth(mDM.values, period) / df['ATR']

	DX = (100 * (pDI - mDI).abs() / (pDI + mDI))

	ADX = pd.DataFrame(wilder_smooth(DX, period), index=df.index, columns=['adx_{}'.format(period)])

	return df.join(ADX)

