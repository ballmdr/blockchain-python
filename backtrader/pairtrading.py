import backtrader as bt
import numpy as np
import datetime

indy = bt.indicators
btfeed = bt.feeds

symbol1 = 'USDJPY'
symbol2 = 'NZDJPY'

class KalmanPair(bt.Strategy):
    params = (("printlog", False), ("quantity", 1000))

    def log(self, txt, dt=None, doprint=False):
        """Logging function for strategy"""
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f"{dt.isoformat()}, {txt}")

    def __init__(self):
        self.delta = 0.0001
        self.Vw = self.delta / (1 - self.delta) * np.eye(2)
        self.Ve = 0.001

        self.beta = np.zeros(2)
        self.P = np.zeros((2, 2))
        self.R = np.zeros((2, 2))

        self.position_type = None  # long or short
        self.quantity = self.params.quantity

    def next(self):

        x = np.asarray([self.data0[0], 1.0]).reshape((1, 2))
        y = self.data1[0]

        self.R = self.P + self.Vw  # state covariance prediction
        yhat = x.dot(self.beta)  # measurement prediction

        Q = x.dot(self.R).dot(x.T) + self.Ve  # measurement variance

        e = y - yhat  # measurement prediction error

        K = self.R.dot(x.T) / Q  # Kalman gain

        self.beta += K.flatten() * e  # State update
        self.P = self.R - K * x.dot(self.R)

        sqrt_Q = np.sqrt(Q)

        if self.position:
            if self.position_type == "long" and e > -sqrt_Q:
                self.close(self.data0)
                self.close(self.data1)
                self.position_type = None
            if self.position_type == "short" and e < sqrt_Q:
                self.close(self.data0)
                self.close(self.data1)
                self.position_type = None

        else:
            if e < -sqrt_Q:
                self.sell(data=self.data0, size=(self.quantity * self.beta[0]))
                self.buy(data=self.data1, size=self.quantity)

                self.position_type = "long"
            if e > sqrt_Q:
                self.buy(data=self.data0, size=(self.quantity * self.beta[0]))
                self.sell(data=self.data1, size=self.quantity)
                self.position_type = "short"

        self.log(f"beta: {self.beta[0]}, alpha: {self.beta[1]}")


def run():
    cerebro = bt.Cerebro()
    cerebro.addstrategy(KalmanPair)

    # startdate = datetime.datetime(2007, 1, 1)
    # enddate = datetime.datetime(2017, 1, 1)

    # ewa = bt.feeds.YahooFinanceData(dataname="EWA", fromdate=startdate, todate=enddate)
    # ewc = bt.feeds.YahooFinanceData(dataname="EWC", fromdate=startdate, todate=enddate)

    path = '/Users/ballmdr/Documents/' + symbol1 + '1440.csv'
    pair1 = btfeed.GenericCSVData(
        dataname = path,
        timeframe = bt.TimeFrame.Days,
        fromdate = datetime.datetime(2013, 1, 1),
        todate = datetime.datetime(2018, 12, 31),
        nullvalue = 0.0,
        dtformat = ('%Y.%m.%d'),
        tmformat = ('%H:%M'),
        datetime = 0,
        time = 1,
        open = 2,
        high = 3,
        low = 4,
        close = 5,
        volume = -1,
        openinterest = -1
    )

    path = '/Users/ballmdr/Documents/' + symbol2 + '1440.csv'
    pair2 = btfeed.GenericCSVData(
        dataname = path,
        timeframe = bt.TimeFrame.Days,
        fromdate = datetime.datetime(2018, 1, 1),
        todate = datetime.datetime(2018, 12, 31),
        nullvalue = 0.0,
        dtformat = ('%Y.%m.%d'),
        tmformat = ('%H:%M'),
        datetime = 0,
        time = 1,
        open = 2,
        high = 3,
        low = 4,
        close = 5,
        volume = -1,
        openinterest = -1
    )
    cerebro.adddata(pair1)
    cerebro.adddata(pair2)
    # cerebro.adddata(ewa)
    # cerebro.adddata(ewc)
    # cerebro.broker.setcommission(commission=0.0001)
    cerebro.broker.setcash(100_000.0)

    print(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")
    cerebro.run()
    print('Pair trading: '+ symbol1 + ' <-> ' + symbol2)
    print(f"Final Portfolio Value: {cerebro.broker.getvalue():.2f}")
    #cerebro.plot()


if __name__ == "__main__":
    run()