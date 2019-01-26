import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from quantnoob.getdata import getMt4Csv, getPandaCsv


indy = bt.indicators

class rsi_overzone(bt.Strategy):

    def __init__(self):
        self.rsi = indy.RSI_SMA(self.data.close, period=21)
    
    def next(self):
        if not self.position:
            if self.rsi < 30:
                print(round(self.rsi[0], 2))
                self.buy()
        else:
            if self.rsi > 70:
                print(round(self.rsi[0], 2))
                self.sell()

def run():

    ori_path = '/Users/ballmdr/Documents/data'

    #symbols = ['EURUSD', 'GBPUSD', 'AUDUSD', 'NZDUSD', 'USDJPY', 'USDCAD', 'USDCHF']
    symbol = 'EURUSD'
    filename = '_M1_2012_2019'
    fromdate = datetime(2012,1,1)
    todate = datetime(2012,1,2)
    cerebro = bt.Cerebro()

    cerebro.addstrategy(rsi_overzone)

    #for symbol in symbols:
    #print('symbol: ' + symbol)
    cerebro.broker.setcash(1_000.0)
    #df = getPandaCsv(ori_path=ori_path, symbol=symbol, filename=filename, fromdate=fromdate, todate=todate)
    df = getMt4Csv(ori_path=ori_path, filename=filename, symbol=symbol, fromdate=fromdate, todate=todate)
    #cerebro.resampledata(df, timeframe=bt.TimeFrame.Days, compression=1)
    #cerebro.adddata(df)

    print(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")

    cerebro.adddata(df)
    print(df)

    cerebro.broker.setcash(100000.0)

    cerebro.addstrategy(rsi_overzone)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcommission(commission=0.0)
    cerebro.run()
    cerebro.plot()
    print(f"Final Portfolio Value: {cerebro.broker.getvalue():.2f}")


if __name__ == "__main__":
    run()