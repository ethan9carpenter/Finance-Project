from datetime import datetime as dt
from managers import deleteFile
from stockData import loadStocks
from correlations.results import loadResults, saveProgress, backupResults, formatFP
from correlations import printMessage, TickerList
from time import time as currentTime
import pandas as pd
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
    """
    Removes companies who have already had their correlations calculated
    and saved from the TickerList used in the analysis.
    
    @param fp: The file path of the saved progress for the correlation calculations
    @param tickers: The list of tickers in the analysis
    
    @return: The number of companies who already have been completed
    """  
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
    """
    Initializes the correlation analysis with pertinent information and pre-analysis
    actions.  
    -Loads the tickers for 'which' and 'against'.
    -Formats the file path based on the parameters for the analysis
    
    @param which: Specifies which companies are the primary targets for analysis.  Either a
    list of companies or a string that is a single company or a string that specifies a
    ticker pack for TickerList to load.
    @param start: Start date for the analysis (datetime)
    @param end: End date for the analysis (datetime)
    @param minshift: Minimum shift for the other stock in days
    @param maxShift: Maximum shift for the other stock in days   
    @param saveType: The type of file to save the analysis results to.
    @param against: The stocks that 'which' will have correlations calculated against.  Default
    'self' or None will set 'against' to 'which'
    
    @return: TickerList object for 'which'
    @return: TickerList object for 'against'
    @return: The file path that the analysis will be saved to
    """
    if against == 'self' or against is None:
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
    which = 'fangs'
    against = 'self'
    minShift = 1
    maxShift = 1
    saveType = 'json'
    #===========================================================================
    # Fix manageStockData so that you can load JSON files to use instead of pickle
    #===========================================================================
    loadDataType = 'pickle'
    overwrite = True
    for i in range(2015, 2016):
        start = dt(i, 1, 1)
        end = dt(i, 12, 31)
        fp = performAnalysis(stocks=which, against=against, 
                         start=start, end=end, 
                         minShift=minShift, maxShift=maxShift, 
                         saveType=saveType, loadDataType=loadDataType, 
                         overwrite=overwrite)
    #pprint(loadJSON(fp))
