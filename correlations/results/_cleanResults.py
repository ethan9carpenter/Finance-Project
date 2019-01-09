import numpy as np
from pandas.api.types import CategoricalDtype
import pandas as pd
#from correlations.results import loadResults
from os import path
from correlations.results._manageResults import _asList

__folder = path.dirname(path.abspath(__file__)) + '/'

def sortedDF(fp, dropSelf, ascending=False, minCorr=-1, maxCorr=1, primary=None, secondary=None, 
             dayShift=None, allPositive=False):

    data = asDF(fp, dropSelf=dropSelf)
    
    if primary is not None:
        data = data.xs(primary, level='primary')
    if secondary is not None:
        data = data.xs(secondary, level='secondary')
    if dayShift is not None:
        data = data.xs(dayShift, level='secondary')
    if allPositive:
        data['correlation'] = np.abs(data['correlation'])
        
    data = data.sort_values('correlation', ascending=ascending)
    data = data[minCorr <= data['correlation']]
    data = data[data['correlation'] <= maxCorr]
    return data

def writeDF(fp, dropSelf):
    df = asDF(fp, dropSelf)
    fileName = fp[fp.find('/')+1:]
    fp = 'dfResults/{}'.format(fileName)
    df.reset_index().to_json(fp)
    
def readDF(fp):
    df = pd.read_json(__folder+fp)
    df.set_index(['primary', 'secondary', 'dayShift'], inplace=True)
    
    return df

def asDF(fp, dropSelf, allPositive=False):
    data = _asList(fp)
    
    types = {'primary': None,
                'secondary': None,
                'dayShift': 'int',
                'correlation': 'float64'}
    df = pd.DataFrame(data, columns=types.keys())
    
    tickerCategories = set(df['primary']) | set(df['secondary'])
    tickerCategories = CategoricalDtype(categories=tickerCategories)
    types['primary'] = tickerCategories
    types['secondary'] = tickerCategories

    for col in df.columns:
        df[col] = df[col].astype(types[col])
    if dropSelf:
        df = df[df['primary'] != df['secondary']]
    df.set_index(['primary', 'secondary', 'dayShift'], inplace=True)
    
    if allPositive:
        data['correlation'] = np.abs(data['correlation'])

    return df

if __name__ == '__main__':
    for i in range(2015, 2019):
        writeDF('dynamicResults/{}-01-01_{}-12-31_505-sp500_505-sp500_1-1.json'.format(i, i), dropSelf=False)
        print(i)
    
    
