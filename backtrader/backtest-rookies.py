import backtrader as bt
from datetime import datetime

indy = bt.indicators

class rsi_overzone(bt.Strategy):

    def __init__(self):
        self.rsi = indy.RSI_SMA(self.data.close, period=21)
    
    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.buy(size=100)
        else:
            if self.rsi > 70:
                self.sell(size=100)


if __name__ == "__main__":
    
    cerebro = bt.Cerebro()

    data = bt.feeds.YahooFinanceData(
        dataname='AAPL',
        fromdate=datetime(2016,1,1),
        todate=datetime(2017,1,1),
        buffered=True
    )
    cerebro.adddata(data)
    cerebro.addstrategy(rsi_overzone)
    cerebro.run()
    cerebro.plot(style='candlestick')