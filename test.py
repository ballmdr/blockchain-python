import pandas as pd
import numpy as np

from datetime import datetime
import time
import fxcmpy
con = fxcmpy.fxcmpy(config_file = '../data/fxcm.cfg')
from functools import reduce


symbol = 'EUR/USD'
tf = 'D1'
n = 1000
loops = 10

df = con.get_candles(symbol, period=tf, number=n)
close = df['askclose'] + df['bidclose'] / 2

df.head()

def initArr(l):
    arr = []
    for i in range(l):
        arr.append(i)
    return arr

def percentChange(start, current):
    try:
        x =  ((float(current) - start) / abs(start)) * 100.00
        if x == 0.0:
            return 0.000000000001
        else:
            return x
    except:
        return 0.00000000001

def patternStorage(df, close):
    patStartTime = time.time()
    
    x = len(close) - 30
    y = loops + 1
    p = initArr(loops)
    
    while y < x:
        j = loops - 1
        
        for i in range(loops):
            p[i] = percentChange(close[y-loops], close[y-j])
            j -= 1
            
        outcomeRange = close[y+20:y+30]
        current = close[y]
        
        try:
            avgOutcome = reduce(lambda x, y: x+y, outcomeRange) / len(outcomeRange)
        except:
            avgOutcome = 0

        futureOutcome = percentChange(current, avgOutcome)
        patternArr.append(p[:])
        performanceArr.append(futureOutcome)
        
        #print(p)
        #print('$$$$$$$$$$$')
        #print(futureOutcome)
        y += 1
    
    patEndTime = time.time()
    #print(patternArr[0] == patternArr[1])
    #print(len(patternArr))
    #print(len(performanceArr))
    #print('pattern storage took:', patEndTime-patStartTime,' seconds')
    
def currentPattern(df, close):
    
    cp = initArr(loops)
    j = loops * -1
    for i in range(loops):
        cp[i] = percentChange(close[-loops+1], close[j])
        j += 1
        patForRec.append(cp[i])
        
    #print(patForRec)
    #print('##########')

def patternRecognition(df, close):
    sim = initArr(loops)
    
    for pattern in patternArr:
        #print(pattern[0])
        howSim = 0.00
        for i in range(loops):
            sim[i] = 100.00 - abs(percentChange(pattern[i], patForRec[i]))
            howSim += sim[i]
        
        howSim /= float(loops)
        
        if howSim > 70:
            print('howSim', howSim)
            patdex = patternArr.index(pattern)
            print('##########################')
            print(patForRec)
            print('==========================')
            print(pattern)
            print('==========================')
            print('predicted outcome', performanceArr[patdex])
            
            xp = initArr(loops)
            plt.plot(xp, patForRec)
            plt.plot(xp, eachPattern)
            plt.show()

if __name__ == "__main__": 
    
    patternArr = []
    performanceArr = []
    patForRec = []

    totalStart = time.time()

    patternStorage(df, close)
    currentPattern(df, close)
    patternRecognition(df, close)
    totalTime = time.time() - totalStart

    print('Entire processing time took:', totalTime, ' seconds')
    