from datetime import datetime as dt
from os.path import exists
from buildData.manageStockData import loadTickers, writeStocks, loadStocks
from buildData.manageResults import loadResults, saveProgress
from buildData.monitors import printMessage

def getCorrelations(data, otherData, maxShift, minShift=0, shiftFactor=1, neg=True):
    correlations = []

    data = data.shift(minShift-1)
    
    for _ in range(1+maxShift-minShift):
        data = data.shift(shiftFactor)
        corr = data.corr(otherData)
        if not neg and corr < 0:
            corr = -corr
        correlations.append(corr)
    return correlations

def _removeCompleted(fp, tickers, overwrite):
    results = loadResults(fp, overwrite)
    numComplete = 0
    if not overwrite:
        for tick in results:
            if tick in tickers:
                numComplete += 1
                tickers.remove(tick)
    return numComplete

def performAnalysis(stocks, fp, start, end, maxShift, minShift=1, shiftFactor=1, overwrite=False):
    totalToAnalyze = len(stocks)
    _validateSymbols(stocks, start, end, 'close')
    numComplete = _removeCompleted(fp, stocks, overwrite)
    
    printMessage('Loading Stocks')
    stocks = loadStocks(stocks)
    printMessage('Done')
    printMessage('Calculating Correlations')
    
    for i, tick in enumerate(stocks.columns):
        tickResults = {}
        for other in stocks.columns:
            if other is not tick:
                tickResults[other] = getCorrelations(stocks[tick], stocks[other], 
                                                         maxShift, minShift, shiftFactor)
        saveProgress(fp, overwrite, tickResults, tick)
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
    which = 'fangs'
    minShift = 1
    maxShift = 1
    overwrite = False
    
    tickers, fp = _initAnalysis(which, start, end, minShift, maxShift)
    
    performAnalysis(stocks=tickers, start=start, end=end, minShift=minShift, 
                    maxShift=maxShift, fp=fp, overwrite=overwrite)
