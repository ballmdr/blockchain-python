import backtrader as bt
from datetime import datetime
import quandl

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


if __name__ == "__main__":
    
    cerebro = bt.Cerebro()

    df = quandl.get("PERTH/USD_JPY_D", authtoken="BtTbtBEhiWH3aJTHWhEP", start_date="2017-01-01", end_date="2018-12-31")
    df.rename(columns={'Ask Average': 'close'}, inplace=True)

    data = bt.feeds.PandasData(dataname=df)
    
    cerebro.adddata(data)
    cerebro.addstrategy(rsi_overzone)
    cerebro.run()
    cerebro.plot(volume=0)

