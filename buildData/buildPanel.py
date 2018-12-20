import pandas as pd
from datetime import datetime as dt
import os
from buildData.manageFiles import loadJSON, saveJSON, loadPickle
from buildData.manageData import toPanel, writeStocks, loadTickers
from time import sleep

def getCorrelations(data, otherData, dayShift, shiftFactor=1):
    correlations = []
    otherDF = pd.DataFrame(otherData)
    df = data.join(otherDF)

    name = df.columns[0]
    for i in range(dayShift+1):
        if i > 0:
            df[name] = df[name].shift(shiftFactor)
        corr = df.corr()
        corr = corr.iloc[1, 0]
        correlations.append(corr)
    return correlations

def performAnalysis(tickers, fp, start, end=dt.now(), dayShift=1, shiftFactor=1, 
                    overwrite=False, returnType='panel'):
    totalToAnalyze = len(tickers)
    if fp and os.path.exists(fp) and not overwrite:
        results = loadJSON(fp)
    else:        
        results = {}
    
    validateSymbols(tickers, start, end, 'close')
    numComplete = 0
    if not overwrite:
        for tick in results:
            if tick in tickers:
                numComplete += 1
                tickers.remove(tick)

    for i, tick in enumerate(tickers):
        tickData = loadPickle('buildData/{}.pickle'.format(tick))
        tickData = pd.DataFrame(tickData)
        results[tick] = {}
        for otherTick in tickers:
            if otherTick is not tick:
                otherData = loadPickle('buildData/{}.pickle'.format(otherTick))
                correlations = getCorrelations(tickData, otherData, dayShift, shiftFactor)
                results[tick][otherTick] = correlations
        sleep(.1)
        saveJSON(fp, results)
        print(i+1+numComplete, 'out of', totalToAnalyze)
    print('Done')
    
    if returnType == 'dict':
        return results
    elif returnType == 'panel':
        return toPanel(fp)
    
def validateSymbols(symbols, start, end, what):
    invalid = []
    
    for tick in symbols:
        if not os.path.exists('buildData/{}.pickle'.format(tick)):
            invalid.append(tick)
            
    writeStocks(invalid, start, end, what)


if __name__ == '__main__':
    which = 'sp500'
    tickers = loadTickers(which)
    print(len(tickers), 'total tickers')
    dayShift = 1
    start = dt(2014, 1, 1)
    end  = dt(2018, 12, 20)
    #RUN ONCE
    #writeStocks(tickers, start, end, 'close')
    fp = 'results/{}_{}_{}_{}.json'.format(start.date(), end.date(), which, len(tickers), dayShift)
    print(fp)
    performAnalysis(tickers, start=start, end=end, dayShift=dayShift, fp=fp, overwrite=False)
