from datetime import datetime as dt
from managers import deleteFile, loadJSON
from stockData import loadStocks
from buildData.results import loadResults, saveProgress, backupResults, formatFP
from buildData import printMessage
from time import time as currentTime
import pandas as pd
from buildData.tickers import TickerList
from stockData.manageStockData import validateSymbols


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
    results = loadResults(fpInfo={'fp': fp})
    numComplete = 0
    for tick in results:
        if tick in tickers:
            numComplete += 1
            tickers.remove(tick)
    return numComplete

def _calculateAllCorr(numComplete, against, totalToAnalyze, stocks, fp, maxShift, minShift, shiftFactor):
    printMessage('Calculating Correlations')
    for i, tick in enumerate(stocks.columns):
        start = currentTime()
        tickResults = pd.DataFrame()
        tickData = stocks[tick].shift(minShift)
        
        for day in range(minShift, maxShift+1):
            tickData = tickData.shift(shiftFactor)
            tickResults[day] = against.corrwith(tickData)
        print(i+1+numComplete, 'out of', totalToAnalyze, currentTime()-start)
        
        saveProgress(fp, tickResults, tick)

def performAnalysis(stocks, start, end, maxShift, loadDataType, saveType, 
                    minShift=1, shiftFactor=1, overwrite=False, against='self', backupSize=10**6):
    
    stocks, against, fp = _initAnalysis(stocks, start, end, minShift, maxShift, saveType, against)

    if overwrite:
        deleteFile(fp)
        
    totalToAnalyze = len(stocks)
    allStocks = set(stocks) | set(against)
    validateSymbols(allStocks, start, end, 'close', fileType=loadDataType)
    numComplete = _removeCompleted(fp, stocks)
    allStocks = loadStocks(allStocks, loadDataType, start, end)
    stocks = allStocks[list(stocks)]
    against = allStocks[list(against)]
    del allStocks
    
    _calculateAllCorr(numComplete, against, totalToAnalyze, stocks, fp, maxShift, minShift, shiftFactor)
    
    if len(stocks) * len(against) * (maxShift - minShift) > backupSize:
        backupResults(fp)
    
    return fp
    
def _initAnalysis(which, start, end, minShift, maxShift, saveType, against='self'):
    if against == 'self':
        against = which
    tickList = TickerList(which)
    againstTL = TickerList(against)
    fp = formatFP(start, end, tickList, againstTL, minShift, maxShift, saveType)
    printMessage('Init Info')
    print('Start Time:', dt.now(), '\nTotal Tickers:', len(tickList), '\nFile:', fp)
    
    return tickList, againstTL, fp

if __name__ == '__main__':
    from pprint import pprint

    start = dt(2015, 1, 1)
    end  = dt(2018, 12, 31)
    which = 'sp500'
    against = 'self'
    minShift = 1
    maxShift = 1
    saveType = 'json'
    #===========================================================================
    # Fix manageStockData so that you can load JSON files to use instead of pickle
    #===========================================================================
    loadDataType = 'pickle'
    overwrite = False
    for i in range(2015, 2019):
        start = dt(i, 1, 1)
        end = dt(i, 12, 31)
        fp = performAnalysis(stocks=which, against=against, 
                         start=start, end=end, 
                         minShift=minShift, maxShift=maxShift, 
                         saveType=saveType, loadDataType=loadDataType, 
                         overwrite=overwrite)
    #pprint(loadJSON(fp))
