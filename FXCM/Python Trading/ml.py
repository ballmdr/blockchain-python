
#%%
import fxcmpy
import time
from datetime import datetime
import pickle
from sklearn.preprocessing import MinMaxScaler, scale, StandardScaler
from sklearn.decomposition import PCA
import tensorflow as tf
import pandas as pd
import numpy as np
import talib as ta
import os

os_path = os.getcwd()

symbol = 'EUR/USD'
timeframe = "m5"	        # (m1,m5,m15,m30,H1,H2,H3,H4,H6,H8,D1,W1,M1)
amount = 1
account_id = '01041561'

price = None
n_price = 300
con = None
maxdd = 0
gross_buy = 0
gross_sell = 0
last_direction = None
max_amountK = 0
limit = None
stop = None

sequence_len = 0

def getNewPrice():
	global price, con
	# update pricedata on first attempt
	new_price = con.get_candles(symbol, period=timeframe, number=n_price)
	
	if new_price.index.values[-1] != price.index.values[-1]:
		price = new_price
		return True

	counter = 0
	# If data is not available on first attempt, try up to 3 times to update pricedata
	while new_price.index.values[-1] == price.index.values[-1] and counter < 3:
		print("No updated prices found, trying again in 10 seconds...")
		time.sleep(10)
		new_price = con.get_candles(symbol, period=timeframe, number=n_price)
		counter += 1
	if new_price.index.values[-1] != price.index.values[-1]:
		price = new_price
		return True
	else:
		return False

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True,feat_name=None):
    
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [f'{feat_name[j]}(t-{i})' for j in range(n_vars)]
    
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [f'{feat_name[j]}(t)' for j in range(n_vars)]
        else:
            names += [f'{feat_name[j]}(t+{i})' for j in range(n_vars)]
    
    # put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    
    return agg

def predictSignal():

    global price, model, pca

    df = pd.DataFrame()
    df['Open'] = (price.askopen + price.bidopen) / 2
    df['High'] = (price.askhigh + price.bidhigh) / 2
    df['Low'] = (price.asklow + price.bidlow) / 2
    df['Close'] = (price.askclose + price.bidclose) / 2
    df['Volume'] = price.tickqty
    df.index = price.index

    df['Returns'] = df.Close.pct_change()
    df['Linear_regression'] = ta.LINEARREG(df.Close, timeperiod=14)
    df['Linear_angle'] = ta.LINEARREG_ANGLE(df.Close, timeperiod=14)
    df['Linear_slope'] = ta.LINEARREG_SLOPE(df.Close, timeperiod=14)
    df['Linear_intercept'] = ta.LINEARREG_INTERCEPT(df.Close, timeperiod=14)

    df['body_candle'] = df.Open - df.Close
    df['high_low'] = df.High - df.Low
    macd, macdsignal, macdhist = ta.MACD(df['Close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
    df['macd'] = macd
    df['macdsignal'] = macdsignal
    df['macdhist'] = macdhist
    df['ma35'] = ta.SMA(df['Close'].values, timeperiod=35)
    df['range_ma35'] = df.Close - df.ma35
    df['ma200'] = ta.SMA(df['Close'].values, timeperiod=200)
    df['Returns'] = np.log(df.Close/df.Close.shift(1))
    df['ATR'] = ta.ATR(df['High'].values, df['Low'], df['Close'], timeperiod=14)
    df['ADX'] = ta.ADX(df.High, df.Low, df.Close, timeperiod=14)
    df['CCI'] = ta.CCI(df.High, df.Low, df.Close, timeperiod=14)
    df['MOM'] = ta.MOM(df.Close, timeperiod=10)
    df['RSI'] = ta.RSI(df.Close, timeperiod=14)

    df['Median'] = ta.MEDPRICE(df.High, df.Low)
    df['STD'] = np.std(df.Close)
    df['Pearson_coef'] = ta.CORREL(df.High, df.Low, timeperiod=30)
    df['Beta'] = ta.BETA(df.High, df.Low, timeperiod=5)
    df['obv'] = ta.OBV(df.Close, df.Volume)
    df['trendmode'] = ta.HT_TRENDMODE(df.Close)
    df['sine'], df['leadsine'] = ta.HT_SINE(df.Close)
    df['avgprice'] = ta.AVGPRICE(df.Open, df.High, df.Low, df.Close)
    df['typical_price'] = ta.TYPPRICE(df.High, df.Low, df.Close)
    df['weight_close'] = ta.WCLPRICE(df.High, df.Low, df.Close)
    df['aroondown'], df['aroonup'] = ta.AROON(df.High, df.Low, timeperiod=14)
    df['trendline'] = ta.HT_TRENDLINE(df.Close)
    df['kama'] = ta.KAMA(df.Close, timeperiod=35)
    df['midpoint'] = ta.MIDPRICE(df.High, df.Low, timeperiod=14)
    df['sar'] = ta.SAR(df.High, df.Low, acceleration=0, maximum=0)
    df['wma'] = ta.WMA(df.Close, timeperiod=35)
    df['upperband'], df['middleband'], df['lowerband'] = ta.BBANDS(df.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

    df.drop(['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'], axis=1, inplace=True)
    df.dropna(inplace=True)

    reframed = series_to_supervised(df.values, sequence_len, 1, feat_name=df.columns)
    reframed = reframed.dropna()
    x = reframed.values
    scaler = StandardScaler()
    x = scaler.fit_transform(x)
    predict_arr = pd.DataFrame(x[-1:])

    #predict_arr = scale(predict_arr.values).reshape(1,-1)
    #predict_arr = pca.transform(predict_arr)
    pred = model.predict(predict_arr)
    #print(predict_arr)
    print('predicted: ', pred)
    return pred
    # if pred == 1:
    #     return True
    # else:
    #     return False


def Update(con):
	global last_direction, gross_buy, gross_sell

	if getNewPrice():
		print(str(datetime.now()) + " Got new prices -> Predicted Signal...")
		isBuy = predictSignal()
		#open_new = checkPosition(isBuy)
		#if open_new:
		if isBuy:
			if last_direction == None or not last_direction or gross_buy >= 0:
				print('Open Buy')
				try:
					opentrade = con.open_trade(symbol=symbol, is_buy=isBuy, amount=amount, time_in_force='GTC',order_type='AtMarket',is_in_pips=True,limit=limit, stop=stop)
				except:
					print('buy %s not success' % symbol)
				else:
					print(opentrade)
					last_direction = True
			else:
				print('Cannot buy')
		else:
			if  last_direction == None or last_direction or gross_sell >= 0:
				print('Open Sell')
				try:
					opentrade = con.open_trade(symbol=symbol, is_buy=isBuy, amount=amount, time_in_force='GTC',order_type='AtMarket',is_in_pips=True,limit=limit, stop=stop)
				except:
					print('sell %s not success' % symbol)
				else:
					print(opentrade)
					last_direction = False
			else:
				print('Cannot Sell')
	
			

#%%

#load model
with open('log_final_data5_m30.pickle', 'rb') as file:
	model = pickle.load(file)
#with open('pca_data3_m5.pickle', 'rb') as file:
#	pca = pickle.load(file)

#model = tf.keras.models.load_model('deep_25042019_data3_m5.h5')

con = fxcmpy.fxcmpy(config_file = os_path + '/fxcm.cfg')

poses = con.get_open_positions(kind='dataframe')
if len(poses) > 0:
	last_direction = poses.iloc[-1].isBuy

# Get First Price
price = con.get_candles(symbol, period=timeframe, number=n_price)

try_again = False
while True:
	currenttime = datetime.now()
	#print(currenttime.minute, ' ', currenttime.second)
	if currenttime.second == 0 or try_again:
		print(currenttime.minute,':',currenttime.second)
		poses = con.get_open_positions()

		#try_again = True
		#else:
			#try_again = False
		if len(poses) > 0:
			gross = poses.grossPL.sum()
			sum_amountK = poses.amountK.sum()
			if sum_amountK > max_amountK:
				max_amountK = sum_amountK
			print('AmountK', sum_amountK)
			print('Max amountK', max_amountK)
			if gross < maxdd:
				maxdd = gross
			print('maxdd: ', maxdd)
			print('Gross PL: ', gross)
			gross_buy = poses[poses['isBuy']].grossPL.sum()
			gross_sell = poses[poses['isBuy'] != True].grossPL.sum()
			print('Gross Buy: ', gross_buy)
			print('Gross Sell: ', gross_sell)
			print('Last Direction: ', last_direction)
			if gross >= 1:
				print('Close All')
				try:
					con.close_all_for_symbol(symbol)
				except:
					print('Close All Failed')
				else:
					print('Close All Success')
					last_direction = None
			else:
				if gross_buy >= 1:
					print('Close all buy')
					for pos in poses[poses['isBuy']].iterrows():
						trade_id = pos[1]['tradeId']
						pos = con.get_open_position(trade_id)
						lot = pos.get_amount()
						try:
							print(trade_id, lot)
							close = con.close_trade(trade_id=trade_id, amount=lot)
						except:
							print('Close buy failed')
						else:
							print(close)
				elif gross_sell >= 1:
					print('Close all sell')
					for pos in poses[poses['isBuy'] != True].iterrows():
						trade_id = pos[1]['tradeId']
						pos = con.get_open_position(trade_id)
						lot = pos.get_amount()
						try:
							print(trade_id, lot)
							close = con.close_trade(trade_id=trade_id, amount=lot)
						except:
							print('Close sell failed')
						else:
							print(close)
		#if True:
		if currenttime.minute % 5 == 0:
			print('awakening...')
			Update(con)
			print('sleeping...')
	time.sleep(1)
