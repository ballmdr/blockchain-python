
import backtrader as bt
from backtrader.utils import flushfile

oandastore = bt.stores.OandaStore
DataCls = bt.feeds.OandaData
# BrokerCls = bt.brokers.OandaBroker

class TestStrategy(bt.Strategy):
    params = dict(
        smaperiod = 35,
        trade = False,
        stake = 10,
        exectype = bt.Order.Market,
        stopafter = 0,
        valid = None,
        cancel = 0,
        donotcounter = False,
        sell = False,
        usebracket = False,
    )

    def __init__(self):
        self.orderid = list()
        self.order = None

        self.counttostop = 0
        self.datastatus = 0

        self.sma = bt.indicators.MovAv.SMA(self.data, period = self.p.smaperiod)


        print('Strategy Created')



if (__name__ == "__main__"):

    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)

    data = oandastore.getdata(dataname='EUR_USD')
    print(data)
    cerebro.run()
