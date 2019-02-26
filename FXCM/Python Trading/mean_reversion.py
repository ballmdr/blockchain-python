import pandas as pd
import numpy as np
from datetime import datetime
import time

import fxcmpy
from apscheduler.schedulers.blocking import BlockingScheduler
import os

os_path = os.getcwd()

def z(df):
    return (df - df.mean()) / df.std()

sched = BlockingScheduler()
lot = 100
tf = 'm1'

#@sched.scheduled_job('interval', seconds=60)
def timed_job():
    print('new time job')
    con = fxcmpy.fxcmpy(config_file = 'fxcm.cfg')
    if (len(con.get_open_positions()) > 0):
        check_position(con)
    trading(con)
    
def check_position(con):
    i = 0
    for i in range(len(con.open_pos)):
        print('i = %i' % i)
        trade_id = con.get_open_trade_ids()[i]
        pos = con.get_open_position(trade_id)
        amount = pos.get_amount()
        symbol = pos.get_currency()
        data = con.get_candles(symbol, period=tf, number=100)
        if (pos.get_isBuy()):
            data['Close_z'] = z(data['bidclose'])
            print(data.iloc[-1]['Close_z'])
            if data.iloc[-1]['Close_z'] > -1:
                con.close_trade(trade_id=trade_id, amount=amount)
                print('close %s' % symbol)
            else:
                print('no close')
        else:
            data['Close_z'] = z(data['askclose'])
            print(data.iloc[-1]['Close_z'])
            if data.iloc[-1]['Close_z'] < 1:
                con.close_trade(trade_id=trade_id, amount=amount)
                print('close %s id: %i amount: %i' % (symbol, trade_id, amount))
            else:
                print('no close')
        i += 1
            

    
def trading(con):
    
    symbols = ['EUR/USD', 'USD/JPY', 'GBP/USD', 'USD/CAD', 'USD/CHF', 'AUD/USD', 'NZD/USD', 'EUR/AUD', 'EUR/CAD', 'EUR/CHF', 'EUR/GBP', 'EUR/JPY', 'EUR/NZD', 'GBP/AUD', 'GBP/CAD', 'GBP/CHF', 'GBP/JPY', 'GBP/NZD', 'AUD/CAD', 'AUD/CHF', 'AUD/JPY', 'AUD/NZD', 'NZD/CAD', 'NZD/CHF', 'NZD/JPY', 'CAD/CHF', 'CAD/JPY', 'CHF/JPY']
    df = dict()
    for symbol in symbols:
        df[symbol] = con.get_candles(symbol, period=tf, number=100)
        df[symbol]['bid_Close_z'] = z(df[symbol]['bidclose'])
        df[symbol]['ask_Close_z'] = z(df[symbol]['askclose'])
        if df[symbol].iloc[-1]['ask_Close_z'] < -2:
            print('buy signal')
            if not hasCurrency(con, symbol):
                order = con.create_market_buy_order(symbol, lot)
                if order:
                    print('buy %s success' % symbol)
                else:
                    print('buy %s not success' % symbol)
        elif df[symbol].iloc[-1]['bid_Close_z'] > 2:
            print('sell signal')
            if not hasCurrency(con, symbol):
                order = con.create_market_sell_order(symbol, lot)
                if order:
                    print('sell %s success' % symbol)
                else:
                    print('sell %s not success' % symbol)
    print('---------')

def hasCurrency(con, symbol):
    i = 0
    for i in range(len(con.open_pos)):
        trade_id = con.get_open_trade_ids()[i]
        pos = con.get_open_position(trade_id)
        if symbol == pos.get_currency():
            print('have position')
            return True
    print('%i not have position %s' % (i, symbol))
    return False
    

#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=10)
#def scheduled_job():
#    print('This job is run every weekday at 10am.')

if __name__ == "__main__":  
    while True:
        timed_job()
        time.sleep(60)