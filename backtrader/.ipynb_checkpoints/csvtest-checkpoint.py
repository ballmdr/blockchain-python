import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import quandl

cerebro = bt.Cerebro()
btind = bt.indicators

class myFirstStrategy(bt.Strategy):

    params = (('period', 35),)

    def __init__(self):
        sma = btind.SMA(self.data, period=self.p.period)
        self.crossover = btind.CrossOver(self.data, sma)
   
    def next(self):
        if self.crossover > 0:
            self.buy()
        elif self.crossover < 0:
            self.sell()

class SmaCross(bt.SignalStrategy):

    def __init__(self):
        sma1, sma2 = btind.SMA(period=5), btind.SMA(period=8)
        crossover = btind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)
        

class RSI_momentum(bt.Strategy):

    def __init__(self):
        self.rsi = btind.RelativeStrengthIndex()
        self.bias = None
    
    def next(self):
        last_rsi = round(self.rsi[0], 2)
        if self.bias == None:
            print('rsi: ' + str(last_rsi))
            if last_rsi > 66.67:
                self.bias = True
            elif last_rsi < 33.33:
                self.bias = False

        elif self.bias:
            if last_rsi > 40 and last_rsi < 50:
                print('Buy bias: {} rsi: {}'.format(str(self.bias), str(last_rsi)))
                self.buy()
                self.bias = None
        elif not self.bias:
            if last_rsi < 60 and last_rsi > 50:
                print('Sell bias: {} rsi: {}'.format(str(self.bias), str(last_rsi)))
                self.sell()
                self.bias = None
    

path = '/Users/ballmdr/Documents/EURUSD1440.csv'
data = btfeed.GenericCSVData(
    dataname = path,
    timeframe = bt.TimeFrame.Days,
    fromdate = datetime.datetime(2018, 1, 1),
    todate = datetime.datetime(2018, 12, 31),
    nullvalue = 0.0,
    dtformat = ('%Y.%m.%d'),
    tmformat = ('%H:%M'),
    datetime = 0,
    time = 1,
    open = 2,
    high = 3,
    low = 4,
    close = 5,
    volumn = -1,
    openinterest = -1
)

# df = quandl.get("PERTH/USD_JPY_D", authtoken="BtTbtBEhiWH3aJTHWhEP", start_date="2017-01-01", end_date="2018-12-31")
# df.rename(columns={'Ask Average': 'close'}, inplace=True)

# data = bt.feeds.PandasData(dataname=df)

cerebro.adddata(data)
#cerebro.resampledata(dataMinute, timeframe=bt.TimeFrame.Days, compression=1)
cerebro.addstrategy(SmaCross)
cerebro.run()
cerebro.plot(volume=0)
