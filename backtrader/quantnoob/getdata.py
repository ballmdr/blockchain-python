import backtrader as bt
import pandas as pd

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

def getPandaCsv(ori_path='', symbol='', tf='1440'):

    path = ori_path + '/data/csv/' + symbol + tf + '.csv'
    
    df = pd.read_csv(path, names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
    df['date'] = pd.to_datetime(df['date'], format='%Y.%m.%d')
    df.index = df['date']
    del df['date']

    X = df[['open', 'high', 'low', 'volume']]
    y = df['close']

    return X, y
    