from pandas import DataFrame
import numpy as np
    
def formatData(stockData, how, typ, asNumpy=False, minChange=0):
    """
    -stockData should be a series of a single stock that is the label
    
    how:
    -'regress' (data is returned as values)
    -'classify' (data becomes True/False based on whether it is an increase over the previous day)
    
    typ:
    -'percent': percent change
    -'price': dollar values
    """    
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
    df = DataFrame(stockData)
    if typ == 'percent':
        df = df.pct_change()
    
    return df

def _classifyData(stockData, typ, minChange):
    df = DataFrame(stockData)
    
    if typ == 'percent':
        df = df.pct_change()
    elif typ == 'value':
        df = df.diff()
    
    for col in df.columns:
        df[col] = df[col] > minChange
    
    return df
    