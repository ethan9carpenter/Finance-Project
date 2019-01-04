from pandas import DataFrame
import numpy as np

class LabelType():
    def __init__(self, typ, minChange=0, changeType=None):
        """
        if changeType == 0:
            change type is dollars
        else:
            change type is percent change
        
        """
        self.typ = typ
        self.minChange = minChange
        self.changeType = changeType
            
        if typ == 'regress':
            self.formatter = _regress
        elif typ == 'classify':
            if changeType == 0:
                self.formatter = _classifyDollars
            else:
                self.formatter = _classifyPercent
            
        
    def __str__(self):
        return self.typ
    
    def formatY(self, stockData, asNumpy=False):
        #stockData should be a series of a single stock that is the label
        data = self.formatter(stockData, self.minChange)
        
        if asNumpy:
            data = np.array(data)
        return data
        
def _regress(stockData, *unused):
    return stockData

def _classifyPercent(stockData, minChange):
    df = DataFrame()
    df['data'] = stockData.pct_change()
    df['label'] = df['data'] > minChange
    
    return df['label']
    
def _classifyDollars(stockData, minChange):
    df = DataFrame()
    df['old'] = stockData
    df['new'] = stockData.shift(-1)
    df['label'] = df['new'] > df['old'] + minChange
    
    return df['label']
    