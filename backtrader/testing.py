
import backtrader as bt

from datetime import datetime
import os.path

class TestStrategy(bt.Strategy):
    params = (('maperiod', 35),)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close

        self.order = False

        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.maperiod)
        self.macd = bt.indicators.MACDHisto(self.datas[0])
        self.rsi = bt.indicators.RSI(self.datas[0])

    def next(self):
        if (self.order):

            if self.dataclose[0] > self.sma[0]:
                self.buy()
                self.order = True
                print('Buy Create, %.2f' % self.dataclose[0])
        
        else:
            if self.dataclose[0] < self.sma[0]:
                self.order = False
                print('Sell Create, %.2f' % self.dataclose[0])


if (__name__ == '__main__'):
    cerebro = bt.Cerebro()

    #data = pd.DataFrame()

    data = bt.feeds.YahooFinanceData(dataname='MSFT', fromdate=datetime(2011, 1, 1),
                                     todate=datetime(2012, 12, 31))
    cerebro.adddata(data)
    print(data)

    cerebro.broker.setcash(100000.0)

    cerebro.addstrategy(TestStrategy)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcommission(commission=0.0)
    cerebro.run()
    cerebro.plot()
    print(cerebro.broker.getvalue())

    