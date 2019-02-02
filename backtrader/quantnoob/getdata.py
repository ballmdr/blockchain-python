import backtrader as bt
import pandas as pd

def getMt4Csv(
        ori_path='',
        filename='', 
        symbol='', 
        fromdate='', 
        todate=''
    ):

    path = ori_path + '/' + symbol + filename + '.csv'
    data = bt.feeds.GenericCSVData(
        headers = False,
        dataname = path,
        timeframe = bt.TimeFrame.Minutes,
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
        volume = 6,
        openinterest = -1
    )
    return data

def getPandaCsv(ori_path='', symbol='', filename='', fromdate='', todate=''):

    path = ori_path + '/' + symbol + filename + '.csv'
    
    df = pd.read_csv(path, names=['date', 'time', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

    #print(df['date'].tail())
    
    #print(df.loc[mask].tail())

    df.index = df['Datetime']
    df.drop(['date', 'time'], axis=1, inplace=True)

    if fromdate != '' and todate != '':
        df = getDateRange(df=df, fromdate=fromdate, todate=todate)

    df['Open'] = df['Open'].round(5)
    df['High'] = df['High'].round(5)
    df['Low'] = df['Low'].round(5)
    df['Close'] = df['Close'].round(5)

    return df
    
def getDateRange(df='', fromdate='', todate=''):

    mask = (df['Datetime'] > fromdate) & (df['Datetime'] <= todate)
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
