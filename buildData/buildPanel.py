import pandas as pd
from datetime import datetime as dt
from os.path import exists
from buildData.manageFiles import loadJSON, saveJSON
from buildData.manageData import writeStocks, loadTickers
from json.decoder import JSONDecodeError

def getCorrelations(data, otherData, dayShift, shiftFactor=1, neg=True):
    correlations = []

    for i in range(dayShift+1):
        if i > 0:
            data = data.shift(shiftFactor)
        corr = data.corr(otherData)
        if not neg and corr < 0:
            corr = -corr
        correlations.append(corr)
    return correlations

def _removeCompleted(results, tickers, overwrite):
    numComplete = 0
    if not overwrite:
        for tick in results:
            if tick in tickers:
                numComplete += 1
                tickers.remove(tick)
    return numComplete

def _handleJSONReadError(fp):
    with open(fp) as file:
        text = file.read()
        index = text.rfind('}')
        text = text[:index] + '}}'
    with open(fp, 'w') as file:
        file.write(text)
    with open(fp) as file:
        return loadJSON(fp)

def _loadResults(fp, overwrite):
    if fp and exists(fp) and not overwrite:
        try:
            results = loadJSON(fp)
        except JSONDecodeError:
            results = _handleJSONReadError(fp)
    else:        
        results = {}
    return results

def _loadStock(ticker):
    return pd.read_pickle('data/pickles/{}.pickle'.format(ticker))

def performAnalysis(tickers, fp, start, end=dt.now(), dayShift=1, shiftFactor=1, overwrite=False):
    
    totalToAnalyze = len(tickers)
    results = _loadResults(fp, overwrite)
    _validateSymbols(tickers, start, end, 'close')
    numComplete = _removeCompleted(results, tickers, overwrite)

    for i, tick in enumerate(tickers):
        tickData = _loadStock(tick)
        tickResults = {}
        for otherTick in tickers:
            if otherTick is not tick:
                otherData = _loadStock(otherTick)
                tickResults[otherTick] = getCorrelations(tickData, otherData, dayShift, shiftFactor)
        
        results[tick] = tickResults #to prevent incomplete writing
        saveJSON(fp, results)
        
        print(i+1+numComplete, 'out of', totalToAnalyze)
    print('Done')
    
def _validateSymbols(symbols, start, end, what):
    invalid = []
    
    for tick in symbols:
        if not exists('data/json/{}.json'.format(tick)):
            invalid.append(tick)
            
    writeStocks(invalid, start, end, what)

def initAnalysis(which, start, end, dayShift):
    tickers = loadTickers(which)    
    fp = 'results/{}_{}_{}_{}_{}.json'.format(start.date(), end.date(), which, len(tickers), dayShift)
    print(len(tickers), 'total tickers\n', fp)
    
    return tickers, fp

if __name__ == '__main__':
    start = dt(2014, 1, 1)
    end  = dt(2018, 12, 20)
    which = 'sp500'
    dayShift = 1
    
    tickers, fp = initAnalysis(which, start, end, dayShift)
    
    performAnalysis(tickers, start=start, end=end, dayShift=dayShift, fp=fp, overwrite=False)
