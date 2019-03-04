import backtrader as bt
from datetime import datetime

import os
os_path = os.getcwd()

import fxcmpy
con = fxcmpy.fxcmpy(config_file = os_path + '/FXCM/fxcm.cfg', server='demo')

indy = bt.indicators

class rsi_overzone(bt.Strategy):

    def __init__(self):
        self.rsi = indy.RSI_SMA(self.data.close, period=14)
    
    def next(self):
        if not self.position:
            if self.rsi < 30:
                print(round(self.rsi[0], 2))
                self.buy()
        else:
            if self.rsi > 70:
                print(round(self.rsi[0], 2))
                self.sell()


if __name__ == "__main__":
    
    symbol = 'EUR/USD'
    df = con.get_candles(symbol, period='H1', number=1260) #1 Years
    df['Close'] = (df['bidclose'] + df['askclose']) / 2

    cerebro = bt.Cerebro(stdstats=False)

    data = bt.feeds.PandasData(dataname=df)

    cerebro.adddata(data)
    cerebro.addstrategy(rsi_overzone)
    cerebro.run()
    cerebro.plot(volume=0)

