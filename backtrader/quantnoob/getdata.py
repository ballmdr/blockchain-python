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
    #print(df['date'].tail())
    
    #print(df.loc[mask].tail())
    #df.index = df['date']
    #del df['date']

    return df
    
def getDateRange(df='', fromdate='', todate=''):

    mask = (df['date'] > fromdate) & (df['date'] <= todate)
    return df.loc[mask]

def getTrainTest(df='', trainfrom='', trainto='', testfrom='', testto='', X_columns='', y_columns=''):

    df_train = getDateRange(df=df, fromdate=trainfrom, todate=trainto)
    X_train = df_train[X_columns]
    y_train = df_train[y_columns].shift(-1)
    X_train.drop(X_train.tail(1).index,inplace=True)
    y_train.drop(y_train.tail(1).index,inplace=True)

    df_test = getDateRange(df=df, fromdate=testfrom, todate=testto)
    X_test = df_test[X_columns]
    y_test = df_test[y_columns].shift(-1)
    X_test.drop(X_test.tail(1).index,inplace=True)
    y_test.drop(y_test.tail(1).index,inplace=True)

    return X_train, y_train, X_test, y_test
