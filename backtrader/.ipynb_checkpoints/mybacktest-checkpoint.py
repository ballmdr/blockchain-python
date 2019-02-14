from __future__ import (absolute_import, division, print_function, unicode_literals)

import backtrader as bt
import pandas as pd
from datetime import datetime
from quantnoob.getdata import getMt4Csv, getPandaCsv


indy = bt.indicators


class myStrategy(bt.Strategy):

    params = (
        ('rsi_period', 14),
        ('exitbars', 5),
        ('sma_period', 35)
    )

    def log(self, txt, dt=None, doprint=False):
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)  
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):

        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.sma_period)
        # Indicators for the plotting show
        # bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        # bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
        #                                     subplot=True)
        # bt.indicators.StochasticSlow(self.datas[0])
        # bt.indicators.MACDHisto(self.datas[0])
        # rsi = bt.indicators.RSI(self.datas[0])
        # bt.indicators.SmoothedMovingAverage(rsi, period=10)
        # bt.indicators.ATR(self.datas[0], plot=False)

        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('Buy Executed, %.2f' % order.executed.price)
            elif order.issell():
                self.log('Sell Executed, %.2f' % order.executed.price)
            
            self.bar_executed = len(self)
        
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        
        self.order = None
    
    def notify_trade(self, trade):

        if not trade.isclosed:
            return
        
        self.log('Operation profit, gross %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))
               
    def next(self):

        #curdate = bt.num2date(self.data.datetime[0])
        #print(str(self.i) + curdate.isoformat() + ' ' + str(self.data.close[0]))
        #self.i += 1

        # มี pending order ผ่านเลย ไม่เปิดเพิ่ม
        if self.order:
            return

        
        if not self.position:
            if self.smaPrice('long'):
                self.log('Buy %.2f' % (self.dataclose[0]))
                self.order = self.buy()
        elif self.smaPrice('short'):
            self.log('Sell %.2f' % (self.dataclose[0]))
            self.order = self.sell()

    def threeDay(self, direction='long'):
        if direction == 'long':
            if self.dataclose[0] < self.dataclose[-1]:
                if self.dataclose[-1] < self.dataclose[-2]:
                    return True
        elif direction == 'short':
            if len(self) >= (self.bar_executed + self.params.exitbars):
                return True
        
        return False

    def smaPrice(self, direction='long'):
        if direction == 'long':
            if self.dataclose[0] > self.sma[0]:
                return True
        elif direction == 'short':
            if self.dataclose[0] < self.sma[0]:
                return True
        
        return False


if __name__ == "__main__":

    ori_path = '/Users/ballmdr/Documents/data'

    #symbols = ['EURUSD', 'GBPUSD', 'AUDUSD', 'NZDUSD', 'USDJPY', 'USDCAD', 'USDCHF']
    symbol = 'EURUSD'
    filename = '_M1_2012_2019'
    fromdate = datetime(2012,1,1)
    todate = datetime(2012,2,1)
    cerebro = bt.Cerebro(optreturn=False)

    #cerebro.addstrategy(myStrategy)
    cerebro.optstrategy(myStrategy, sma_period=(10,11))

    #for symbol in symbols:
    #print('symbol: ' + symbol)
    
    df = getPandaCsv(ori_path=ori_path, symbol=symbol, filename=filename, fromdate=fromdate, todate=todate)
    df = bt.feeds.PandasData(dataname=df, datetime=None, open='Open', high='High', low='Low', close='Close', volume='Volume', openinterest=None)

    #df = getMt4Csv(ori_path=ori_path, filename=filename, symbol=symbol, fromdate=fromdate, todate=todate)

    #cerebro.resampledata(df, timeframe=bt.TimeFrame.Days, compression=1440)
    #print('resample')
    startcash = 1000
    cerebro.adddata(df)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcash(startcash)
    cerebro.broker.setcommission(commission=0.001)

    #print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    opt_runs = cerebro.run()

    # Generate results list
    final_results_list = []
    for run in opt_runs:
        for strategy in run:
            value = round(strategy.broker.get_value(),2)
            PnL = round(value - startcash,2)
            period = strategy.params.period
            final_results_list.append([period,PnL])

    #Sort Results List
    by_period = sorted(final_results_list, key=lambda x: x[0])
    by_PnL = sorted(final_results_list, key=lambda x: x[1], reverse=True)

    #Print results
    print('Results: Ordered by period:')
    for result in by_period:
        print('Period: {}, PnL: {}'.format(result[0], result[1]))
    print('Results: Ordered by Profit:')
    for result in by_PnL:
        print('Period: {}, PnL: {}'.format(result[0], result[1]))
    #print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    #cerebro.plot()