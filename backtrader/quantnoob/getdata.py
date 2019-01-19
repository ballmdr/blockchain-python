import backtrader as bt

def getMt4Csv(ori_path='', symbol='', tf='1440', fromdate='', todate=''):

    path = ori_path + '/data/csv/' + symbol + tf + '.csv'
    data = bt.feeds.GenericCSVData(
        dataname = path,
        timeframe = bt.TimeFrame.Days,
        fromdate = fromdate,
        todate = todate,
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
    return data