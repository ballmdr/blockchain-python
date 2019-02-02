import backtrader as bt
import backtrader.indicators as btind
import datetime
import pandas as pd
from pandas import Series, DataFrame
import random
from copy import deepcopy
from datetime import datetime
from quantnoob.getdata import getMt4Csv, getPandaCsv



class SMAC(bt.Strategy):
    """A simple moving average crossover strategy; crossing of a fast and slow moving average generates buy/sell
       signals"""
    params = {"fast": 20, "slow": 50,                  # The windows for both fast and slow moving averages
              "optim": False, "optim_fs": (20, 50)}    # Used for optimization; equivalent of fast and slow, but a tuple
                                                       # The first number in the tuple is the fast MA's window, the
                                                       # second the slow MA's window
 
    def __init__(self):


        self.fastma = dict()
        self.slowma = dict()
        self.regime = dict()
 
        #self._addobserver(True, bt.observers.BuySell)    
        
        # CAUTION: Abuse of the method, I will change this in future code (see: https://community.backtrader.com/topic/473/plotting-just-the-account-s-value/4)
 
        #optimization
        if self.params.optim:
            self.params.fast, self.params.slow = self.params.optim_fs    # fast and slow replaced by tuple's contents
 
 
        for d in self.getdatanames():
 
            # The moving averages
            self.fastma[d] = btind.SimpleMovingAverage(self.getdatabyname(d),      # The symbol for the moving average
                                                       period=self.params.fast,    # Fast moving average
                                                       plotname="FastMA: " + d)
            self.slowma[d] = btind.SimpleMovingAverage(self.getdatabyname(d),      # The symbol for the moving average
                                                       period=self.params.slow,    # Slow moving average
                                                       plotname="SlowMA: " + d)
 
            # Get the regime
            self.regime[d] = self.fastma[d] - self.slowma[d]    # Positive when bullish
 
    def next(self):
        """Define what will be done in a single step, including creating and closing trades"""
        for d in self.getdatanames():    # Looping through all symbols
            pos = self.getpositionbyname(d).size or 0
            if pos == 0:    # Are we out of the market?
                # Consider the possibility of entrance
                # Notice the indexing; [0] always means the present bar, and [-1] the bar immediately preceding
                # Thus, the condition below translates to: "If today the regime is bullish (greater than
                # 0) and yesterday the regime was not bullish"
                if self.regime[d][0] > 0 and self.regime[d][-1] <= 0:    # A buy signal
                    self.buy(data=self.getdatabyname(d))
                    print('Buy %s' % (self.getdatabyname(d)))
 
            else:    # We have an open position
                if self.regime[d][0] <= 0 and self.regime[d][-1] > 0:    # A sell signal
                    self.sell(data=self.getdatabyname(d))
                    print('Sell %s' % (self.getdatabyname(d)))


class PropSizer(bt.Sizer):
    """A position sizer that will buy as many stocks as necessary for a certain proportion of the portfolio
       to be committed to the position, while allowing stocks to be bought in batches (say, 100)"""
    params = {"prop": 0.1, "batch": 100}
 
    def _getsizing(self, comminfo, cash, data, isbuy):
        """Returns the proper sizing"""
 
        if isbuy:    # Buying
            target = self.broker.getvalue() * self.params.prop    # Ideal total value of the position
            price = self.dataclose[0]
            shares_ideal = target / price    # How many shares are needed to get target
            batches = int(shares_ideal / self.params.batch)    # How many batches is this trade?
            shares = batches * self.params.batch    # The actual number of shares bought
 
            if shares * price > cash:
                return 0    # Not enough money for this trade
            else:
                return shares
 
        else:    # Selling
            return self.broker.getposition(data).size    # Clear the position

def getAllSymbols():
    
    for symbol in symbols:
        print('get data %s' % (symbol))
        df = getPandaCsv(ori_path=ori_path, symbol=symbol, filename=filename, fromdate=fromdate, todate=todate)
        df = bt.feeds.PandasData(dataname=df, datetime=None, open='Open', high='High', low='Low', close='Close', volume='Volume', openinterest=None)
        #cerebro.adddata(df, name=symbol)
        cerebro.resampledata(df, timeframe=bt.TimeFrame.Days, compression=1440, name=symbol)
        print('get data finish %s' % (symbol))

class watchVar(bt.Strategy):

    params = (('fast', 5), ('slow', 8))

    def __init__(self):
        print('init strategy')

        self.dataclose = dict()
        self.sma_fast = dict()
        self.sma_slow = dict()
        self.longsignal = dict()
        self.shortsignal = dict()
        
        for symbol in self.getdatanames():
            self.dataclose[symbol] = self.datas[0].close
            self.sma_fast[symbol] = btind.SimpleMovingAverage(self.getdatabyname(symbol), period=self.p.fast, plotname="FastMA: " + symbol)
            self.sma_slow[symbol] = btind.SimpleMovingAverage(self.getdatabyname(symbol), period=self.p.slow, plotname="SlowMA: " + symbol)
            self.longsignal[symbol] = btind.CrossOver(self.sma_fast[symbol], self.sma_slow[symbol])
            self.shortsignal[symbol] = btind.CrossOver(self.sma_slow[symbol], self.sma_fast[symbol])
    
    def next(self):

        for symbol in self.getdatanames():
            data = self.getdatabyname(symbol)
            curdate = bt.num2date(data.datetime[0])

            pos = self.getpositionbyname(symbol).size
            if pos == 0:
                if self.longsignal[symbol] > 0:
                    print(curdate.isoformat() + 'Long %s @ %.2f' % (symbol, self.dataclose[symbol][0]))
                    self.buy(data=self.getdatabyname(symbol))
            else:
                if self.shortsignal[symbol] > 0:
                    print(curdate.isoformat() +  'Short %s @ %.2f' % (symbol, self.dataclose[symbol][0]))
                    self.sell(data=self.getdatabyname(symbol))
            


if __name__ == "__main__":

    ori_path = '/Users/ballmdr/Documents/data'

    #symbols = ['EURUSD', 'GBPUSD', 'AUDUSD', 'NZDUSD', 'USDJPY', 'USDCAD', 'USDCHF']
    symbols = ['EURUSD', 'GBPUSD']
    #symbol = 'EURUSD'
    filename = '_M1_2012_2019'
    fromdate = datetime(2012,1,1)
    todate = datetime(2014,2,1)

    cerebro = bt.Cerebro(stdstats=False)

    getAllSymbols()

    cerebro.broker.set_cash(1_000)
    cerebro.broker.setcommission(0.02)
    cerebro.addobservermulti(bt.observers.BuySell)

    cerebro.addstrategy(watchVar)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot(volume=False)