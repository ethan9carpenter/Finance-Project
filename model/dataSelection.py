import pandas as pd
import numpy as np

def _formatData(stockData, how, typ, asNumpy=False, minChange=0):
    """
    -stockData should be a series of a single stock that is the label
    
    how:
    -'regress': data is returned as values
    -'classify': data becomes True/False based on whether it is an increase over the previous day
    
    typ:
    -'percent': percent change
    -'price': dollar values
    """
    __handleInput(how, typ)
    
    if how == 'regress':
        data = _regressData(stockData, typ)
    elif how == 'classify':
        data = _classifyData(stockData, typ, minChange)
    """
    Get rid of class and make everything use format data, deciding whether price/percent change and
    then choose whether you want it as 'regress' or 'classify'
    """
    
    if asNumpy:
        data = np.array(data)
    return data

def _regressData(stockData, typ):
    df = pd.DataFrame(stockData)
    if typ == 'percent':
        df = df.pct_change()
    elif typ == 'price':
        pass
    
    return df

def _classifyData(stockData, typ, minChange):
    df = pd.DataFrame(stockData)
    
    if typ == 'percent':
        df = df.pct_change()
    elif typ == 'price':
        df = df.diff()
    
    for col in df.columns:
        df[col] = df[col] > minChange
    
    return df

def __handleInput(how, typ):
    if how not in ['classify', 'regress']:
        raise Exception()
    elif typ not in ['price', 'percent']:
        raise Exception()
    
def splitXY(featureDF, xHow, xTyp, yHow, yTyp, labelColumn=-1):
    X = featureDF.drop(featureDF.columns[labelColumn], axis=1)
    y = featureDF[featureDF.columns[labelColumn]]

    X = _formatData(X, how=xHow, typ=xTyp)
    y = _formatData(y, how=yHow, typ=yTyp)
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