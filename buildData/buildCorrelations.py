from datetime import datetime as dt
from os.path import exists
from buildData.manageStockData import loadTickers, writeStocks, loadStocks
from buildData.manageResults import loadResults, saveProgress
from buildData.monitors import printMessage
from buildData.manageFiles import deleteFile, pickleToJSON
import time as TIME
#===============================================================================
# Convert to use df.corr and then shift for each stock to make more efficient
#===============================================================================
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

def _removeCompleted(fp, tickers):        
    results = loadResults(fp)
    numComplete = 0
    for tick in results:
        if tick in tickers:
            numComplete += 1
            tickers.remove(tick)
    return numComplete

def _preprocess(stocks, fp, start, end, loadDataType, overwrite):
    if overwrite:
        deleteFile(fp)
    totalToAnalyze = len(stocks)
    _validateSymbols(stocks, start, end, 'close', fileType=loadDataType)
    numComplete = _removeCompleted(fp, stocks)
    stocks = loadStocks(stocks, loadDataType, True)
    
    return totalToAnalyze, numComplete, stocks

def _calculateAllCorr(numComplete, totalToAnalyze, stocks, fp, maxShift, minShift, shiftFactor):
    printMessage('Calculating Correlations')
    for i, tick in enumerate(stocks.columns):
        time = TIME.time()
        tickResults = {}
        for other in stocks.columns:
            if other is not tick:
                tickResults[other] = getCorrelations(stocks[tick], stocks[other], 
                                                         maxShift, minShift, shiftFactor)
        saveProgress(fp, tickResults, tick)
        print(i+1+numComplete, 'out of', totalToAnalyze, TIME.time()-time)

def performAnalysis(stocks, fp, start, end, maxShift, loadDataType, minShift=1, shiftFactor=1, overwrite=False):
    totalToAnalyze, numComplete, stocks, = _preprocess(stocks, fp, start, end, loadDataType, overwrite)
    _calculateAllCorr(numComplete, totalToAnalyze, stocks, fp, maxShift, minShift, shiftFactor)
    pickleToJSON(fp)
    
def _validateSymbols(symbols, start, end, what, fileType):
    invalid = []
    
    for tick in symbols:
        if not exists('data/{}/{}.{}'.format(fileType, tick, fileType)):
            invalid.append(tick) 
    writeStocks(invalid, start, end, what, fileType)

def _initAnalysis(which, start, end, minShift, maxShift):
    tickers = loadTickers(which)   [:100] 
    fp = 'results/{}_{}_{}_{}_{}_{}.pickle'.format(start.date(), end.date(), which, 
                                                 len(tickers), minShift, maxShift)
    printMessage('Init Info')
    print('Start Time:', dt.now(), '\nTotal Tickers:', len(tickers), '\nFile:', fp)
    
    return tickers, fp

if __name__ == '__main__':
    start = dt(2014, 1, 1)
    end  = dt(2018, 12, 20)
    which = 'sp500'
    minShift = 1
    maxShift = 1
    tickers, fp = _initAnalysis(which, start, end, minShift, maxShift)
    loadDataType = 'pickle'
    overwrite = True
    
    performAnalysis(stocks=tickers, start=start, end=end, minShift=minShift, 
                    maxShift=maxShift, fp=fp, loadDataType=loadDataType, overwrite=overwrite)