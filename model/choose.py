import pandas as pd
from stockData import loadStocks
from correlations.results import sortedDF
from model import formatData
from datetime import datetime as dt
from managers import saveJSON
from os import path

#To load data from the proper folder
__fileFolder = path.dirname(path.abspath(__file__)) + '/data' 

def _trimToSig(data, sigCols, sigVal):
    for col in sigCols:
        data = data[data[col] > sigVal]
    
    return data
    
def _merge(data):
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
    data = {}

    for year in range(start.year, end.year+1):
        data[str(year)] = sortedDF(yearlessFP.format(dt(year, 1, 1).date(), dt(year, 12, 31).date()), 
                                   dropSelf=dropSelf, allPositive=True)
    df = _merge(data)
    df = _trimToSig(df, sigCols=df.columns[:-1], sigVal=sigVal)
    df = _buildSelectionDF(_selectSignificant(df), primary, start=start, end=end)

    return df

def splitXY(featureDF, xHow, xTyp, yHow, yTyp, labelColumn=-1):
    X = featureDF.drop(featureDF.columns[labelColumn], axis=1)
    y = featureDF[featureDF.columns[labelColumn]]

    X = formatData(X, how=xHow, typ=xTyp)
    y = formatData(y, how=yHow, typ=yTyp)
    X, y = _handleNaN(X, y)
    
    return X, y
    
def _handleNaN(X, y):
    X.dropna(inplace=True)
    y.dropna(inplace=True)
    
    if len(y) > len(X):
        y = y.loc[X.index[0]:X.index[-1]]
    elif len(y) < len(X):
        X = X.loc[y.index[0]:y.index[-1]]
        
    return X, y

def writeSignificant(yearlessFP, start, end, sigVal=0, allPositive=False):
    data = {}

    for year in range(start.year, end.year+1):
        data[str(year)] = sortedDF(yearlessFP.format(dt(year, 1, 1).date(), dt(year, 12, 31).date()), 
                                   allPositive=allPositive)
    df = _merge(data)
    df = _trimToSig(df, sigCols=df.columns[:-1], sigVal=sigVal)
    
    df.reset_index(inplace=True)
    primary = set(list(df['primary']))

    sigDict = {}
    for company in primary:
        sig = df[df['primary'] == company]
        sig = list(zip(df[['secondary', 'dayShift']]))
        sigDict[company] = sig
        
    writeFP = 'significantPairs/significant_' + yearlessFP.format(start.year, end.year)
    
    saveJSON(__fileFolder, writeFP, data=sigDict)
    
    return sigDict
    
    