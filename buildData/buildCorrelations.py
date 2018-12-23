from datetime import datetime as dt
from os.path import exists
from buildData.manageStockData import loadTickers, writeStocks, loadStocks
from buildData.manageResults import loadResults, saveProgress
from buildData.monitors import printMessage
from buildData.manageFiles import deleteFile
from time import time as currentTime
import pandas as pd

def getCorrelations(data, otherData, maxShift, minShift=0, shiftFactor=1, neg=True):
    correlations = []
    data = data.shift(minShift-1)
    
    for _ in range(1+maxShift-minShift):
        #===========================================================================
        # Costly: shift and corr
        #===========================================================================
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


def _calculateAllCorr(numComplete, totalToAnalyze, stocks, fp, maxShift, minShift, shiftFactor):
    printMessage('Calculating Correlations')
    for i, tick in enumerate(stocks.columns):
        start = currentTime()
        tickResults = pd.DataFrame()
        tickData = stocks[tick].shift(minShift)
        
        for day in range(maxShift-minShift+1):
            tickData = stocks[tick].shift(shiftFactor)
            tickResults[day] = stocks.corrwith(tickData)
        print(i+1+numComplete, 'out of', totalToAnalyze, currentTime()-start)
        
        saveProgress(fp, tickResults, tick)

def performAnalysis(stocks, fp, start, end, maxShift, loadDataType, minShift=1, shiftFactor=1, overwrite=False):
    if overwrite:
        deleteFile(fp)
    totalToAnalyze = len(stocks)
    _validateSymbols(stocks, start, end, 'close', fileType=loadDataType)
    numComplete = _removeCompleted(fp, stocks)
    stocks = loadStocks(stocks, loadDataType, False)
    
    _calculateAllCorr(numComplete, totalToAnalyze, stocks, fp, maxShift, minShift, shiftFactor)
    
def _validateSymbols(symbols, start, end, what, fileType):
    invalid = []
    
    for tick in symbols:
        if not exists('data/{}/{}.{}'.format(fileType, tick, fileType)):
            invalid.append(tick) 
    writeStocks(invalid, start, end, what, fileType)

def _initAnalysis(which, start, end, minShift, maxShift, saveType):
    tickers = loadTickers(which)[:100]
    fp = 'results/{}_{}_{}_{}_{}_{}.{}'.format(start.date(), end.date(), which, 
                                                 len(tickers), minShift, maxShift, saveType)
    printMessage('Init Info')
    print('Start Time:', dt.now(), '\nTotal Tickers:', len(tickers), '\nFile:', fp)
    
    return tickers, fp

if __name__ == '__main__':
    start = dt(2014, 1, 1)
    end  = dt(2018, 12, 20)
    which = 'sp500'
    minShift = 1
    maxShift = 30
    saveType = 'json'
    tickers, fp = _initAnalysis(which, start, end, minShift, maxShift, saveType)
    loadDataType = 'pickle'
    overwrite = True
    
    performAnalysis(stocks=tickers, start=start, end=end, minShift=minShift, 
                    maxShift=maxShift, fp=fp, loadDataType=loadDataType, overwrite=overwrite)