import backtrader as bt
import numpy as np
from datetime import datetime
from quantnoob.strategy.simplestrategy import simplestrategy
from quantnoob.strategy.kalmanpair import KalmanPair
from quantnoob.getdata import getMt4Csv
from quantnoob.strategy.rsioverzone_buyonly import RsiOverzone

def run():

    ori_path = '/Users/ballmdr/blockchain-python/backtrader'

    symbol = 'EURUSD'
    #symbol2 = 'NZDJPY'
    cerebro = bt.Cerebro()

    cerebro.addstrategy(RsiOverzone)

    data = getMt4Csv(ori_path=ori_path, symbol=symbol, tf='1440', fromdate=datetime(2011,1,1), todate=datetime(2018,12,31))
    #pair2 = getMt4Csv(ori_path=ori_path, symbol=symbol2, fromdate=datetime(2013,1,1), todate=datetime(2018,12,31))
    cerebro.adddata(data)
    #cerebro.adddata(pair2)
    # cerebro.broker.setcommission(commission=0.0001)
    cerebro.broker.setcash(100_000.0)

    print(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")
    cerebro.run()
   # print('Pair trading: '+ symbol1 + ' <-> ' + symbol2)
    print(f"Final Portfolio Value: {cerebro.broker.getvalue():.2f}")
    cerebro.plot()


if __name__ == "__main__":
    run()