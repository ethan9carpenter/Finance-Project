import pandas as pd
from stockData import loadStocks
from buildData.results import sortedDF
from model.labels import formatData
from datetime import datetime as dt

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

def buildFeatureDF(baseFP, start, end, primary, sigVal, dropSelf=False):
    data = {}

    for year in range(start.year, end.year+1):
        data[str(year)] = sortedDF(baseFP.format(dt(year, 1, 1).date(), dt(year, 12, 31).date()), dropSelf=dropSelf, allPositive=True)
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
    
    
    
    