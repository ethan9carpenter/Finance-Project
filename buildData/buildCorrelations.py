from datetime import datetime as dt
from os.path import exists
from buildData.manageFiles import saveJSON
from buildData.manageStockData import loadTickers, writeStocks, loadStock
from buildData.manageResults import loadResults
from buildData.monitors import printMessage

def getCorrelations(data, otherData, maxShift, minShift=0, shiftFactor=1, neg=True):
    correlations = []

    data = data.shift(shiftFactor)
    for _ in range(maxShift-minShift):
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

def performAnalysis(tickers, fp, start, end, maxShift, minShift=1, shiftFactor=1, overwrite=False):
    totalToAnalyze = len(tickers)
    results = loadResults(fp, overwrite)
    _validateSymbols(tickers, start, end, 'close')
    numComplete = _removeCompleted(results, tickers, overwrite)
    stockData = {}
    printMessage('Loading Stocks')
    for tick in tickers:
        stockData[tick] = loadStock(tick)
    printMessage('Done')
    printMessage('Calculating Correlations')
    
    for i, tick in enumerate(tickers):
        tickResults = {}
        for other in tickers:
            if other is not tick:
                tickResults[other] = getCorrelations(stockData[tick], stockData[other], 
                                                         maxShift, minShift, shiftFactor)
        results[tick] = tickResults #to prevent incomplete writing
        saveJSON(fp, results)
        print(i+1+numComplete, 'out of', totalToAnalyze, dt.now().time())
    
    printMessage('Done')
    
def _validateSymbols(symbols, start, end, what):
    invalid = []
    
    for tick in symbols:
        if not exists('data/pickles/{}.pickle'.format(tick)):
            invalid.append(tick)
            
    writeStocks(invalid, start, end, what)

def _initAnalysis(which, start, end, minShift, maxShift):
    if isinstance(which, str):
        tickers = loadTickers(which)
    else:
        tickers = which    
    fp = 'results/{}_{}_{}_{}_{}_{}.json'.format(start.date(), end.date(), which, 
                                                 len(tickers), minShift, maxShift)
    printMessage('Init Info')
    print('Start Time:', dt.now(), '\nTotal Tickers:', len(tickers), '\nFile:', fp)
    
    return tickers, fp

if __name__ == '__main__':
    start = dt(2014, 1, 1)
    end  = dt(2018, 12, 20)
    which = 'iex'
    minShift = 1
    maxShift = 1
    overwrite = False
    
    tickers, fp = _initAnalysis(which, start, end, minShift, maxShift)
    
    performAnalysis(tickers=tickers, start=start, end=end, minShift=minShift, 
                    maxShift=maxShift, fp=fp, overwrite=overwrite)
