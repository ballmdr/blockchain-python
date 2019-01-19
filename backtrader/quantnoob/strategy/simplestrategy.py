import backtrader as bt

class simplestrategy(bt.Strategy):

    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=14)
        self.macd = bt.indicators.MACDHisto(self.data.close)