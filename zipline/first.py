from zipline.api import order, record, symbol, order_target
from zipline.algorithm import TradingAlgorithm
import pytz
from datetime import datetime
import pandas as pd


def initialize(context):
    context.security = symbol('AAPL')

def handle_data(context, data):
    MA1 = data[context.security].mavg(50)
    MA2 = data[context.security].mavg(100)
    date = str(data[context.security].datetime)[:10]
    current_price = data[context.security].price
    current_positions = context.portfolio.positions[symbol('AAPL')].amount
    cash = context.portfolio.cash
    value = context.portfolio.portfolio_value
    current_pnl = context.portfolio.pnl

    if (MA1 > MA2) and current_positions == 0:
        number_of_shares = int(cash/current_price)
        order(context.security, number_of_shares)
        record(date=date,MA1 = MA1, MA2 = MA2, Price= 
    current_price,status="buy",shares=number_of_shares,PnL=current_pnl,cash=cash,value=value)

    elif (MA1 < MA2) and current_positions != 0:
        order_target(context.security, 0)
        record(date=date,MA1 = MA1, MA2 = MA2, Price= current_price,status="sell",shares="--",PnL=current_pnl,cash=cash,value=value)

    else:
        record(date=date,MA1 = MA1, MA2 = MA2, Price= current_price,status="--",shares="--",PnL=current_pnl,cash=cash,value=value)

def getDateRange(df='', fromdate='', todate=''):

    mask = (df['Datetime'] > fromdate) & (df['Datetime'] <= todate)
    return df.loc[mask]

def getPandaCsv(ori_path='', symbol='', filename='', fromdate='', todate=''):

    path = ori_path + '/' + symbol + filename + '.csv'
    
    df = pd.read_csv(path, names=['date', 'time', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

    #print(df['date'].tail())
    
    #print(df.loc[mask].tail())

    #df.index = df['Date']

    df.drop(['date', 'time'], axis=1, inplace=True)

    if fromdate != '' and todate != '':
        df = getDateRange(df=df, fromdate=fromdate, todate=todate)

    df.index = df['Datetime']
    del df['Datetime']

    return df


if __name__ == "__main__":
    
    ori_path = '/Users/ballmdr/Documents/data'
    symbol = 'EURUSD'
    filename = '_M1_2012_2019'
    fromdate = datetime(2012,1,1)
    todate = datetime(2012,12,13)

    data = getPandaCsv(ori_path=ori_path, symbol=symbol, filename=filename, fromdate=fromdate, todate=todate)

    #data.to_csv('/Users/ballmdr/Documents/data/test.csv')

    algo_obj = TradingAlgorithm(initialize = initialize, handle_data = handle_data, caital_base = 1000.0)

    perf_manual = algo_obj.run(data)
    perf_manual[["MA1","MA2","Price"]].plot()