import pandas as pd
from stockData import loadStocks
from correlations.results import asDF
from datetime import datetime as dt
from managers import saveJSON
from os import path
from correlations.results._cleanResults import readDF

#To load data from the proper folder
__fileFolder = path.dirname(path.abspath(__file__)) + '/' 

def _trimToSig(data, sigCols, sigVal):
    for col in sigCols:
        data = data[data[col] > sigVal]
    
    return data
    
def __merge(data):
    df = pd.DataFrame()
    for period, corrs in data.items():
        df[str(period)] = corrs['correlation']
    return df

def _selectSignificant(data):
    df = data.reset_index()

    stocks = set(df['primary'])
    sigPairs = {}
    for stock in stocks:
        stockData = df[df['primary'] == stock]
        sigPairs[stock] = list(zip(stockData['secondary'], stockData['dayShift']))

    return sigPairs

def _buildSelectionDF(sigData, stock, start, end):
    #if stock in sigData:
    data = sigData[stock]
    #else:
    #   data = pd.DataFrame()
    #===========================================================================
    # HANDLE ERRORS IN A GOOD WAY
    #===========================================================================
    toLoad = [stock] + list(dict(data).keys())
    stockData = loadStocks(toLoad, start=start, end=end, fileType='pickle')
    selectionDF = pd.DataFrame()
    
    for otherTick, shift in data:
        name = '{}-{}'.format(otherTick, shift)
        selectionDF[name] = stockData[otherTick].shift(shift)
    
    selectionDF[stock] = stockData[stock]
    
    return selectionDF

def buildFeatureDF(yearlessFP, start, end, primary, sigVal, dropSelf=False):
    df = _correlationsByYear(yearlessFP, dropSelf, sigVal)
    df = _buildSelectionDF(_selectSignificant(df), primary, start=start, end=end)

    return df

def _correlationsByYear(yearlessFP, dropSelf=False, sigVal=-1, colToKeep=-1):
    data = {}
    yearlessFP = 'dfResults/' + yearlessFP
    for year in range(start.year, end.year+1):
        data[str(year)] = readDF(yearlessFP.format(dt(year, 1, 1).date(), dt(year, 12, 31).date()))
        print(year)
    df = __merge(data)
    df = _trimToSig(df, sigCols=df.columns[:-1], sigVal=sigVal)
    
    return df

def saveSignificant(yearlessFP, start, end, sigVal=0, dropSelf=False):
    df = _correlationsByYear(yearlessFP, dropSelf, sigVal)
    
    df.reset_index(inplace=True)
    primary = set(df['primary'])

    sigDict = {}
    for i, company in enumerate(primary):
        sig = df[df['primary'] == company]
        secondary = set(sig['secondary'])

        sigDict[company] = {}
        for other in secondary:
            shifts = sig[sig['secondary'] == other]
            shifts = shifts['dayShift']
            sigDict[company][other] = sorted(shifts)
            
        print(i, '/', len(primary))
    
    
    writeFP = 'significantPairs/significant_{}_'.format(sigVal) + yearlessFP.format(start.year, end.year)
    saveJSON(__fileFolder, writeFP, data=sigDict)
    
    return sigDict

if __name__ == '__main__':
    fp = '{}_{}_505-sp500_505-sp500_1-1.json'
    start = dt(2015, 1, 1)
    end = dt(2018, 12, 31)
    sigVal = 0.5
    sig = saveSignificant(fp, start, end, sigVal, dropSelf=True)
    from pprint import pprint
    print(sig)
    
    
    