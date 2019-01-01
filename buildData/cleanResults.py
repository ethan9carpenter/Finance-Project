from managers import moveDirUp, loadJSON
import cProfile
import numpy as np
from pandas.api.types import CategoricalDtype
import pandas as pd

def sortedDF(fp, dropSelf, ascending=False, minCorr=-1, maxCorr=1, mainCompany=None, secondCompany=None, 
             dayShift=None, allPositive=False):
    data = asDF(fp, dropSelf=dropSelf)
    
    if mainCompany is not None:
        data = data.xs(mainCompany, level='mainCompany')
    if secondCompany is not None:
        data = data.xs(secondCompany, level='secondCompany')
    if dayShift is not None:
        data = data[data['dayShift'] == dayShift]
    if allPositive:
        data['correlation'] = np.abs(data['correlation'])
        
    data = data.sort_values('correlation', ascending=ascending)
    data = data[minCorr <= data['correlation']]
    data = data[data['correlation'] <= maxCorr]

    return data

def asDF(fp, dropSelf):
    data = _asList(fp)
    columns = ['mainCompany', 'secondCompany', 'dayShift', 'correlation']
    types = {'mainCompany': None,
                'secondCompany': None,
                'dayShift': 'int',
                'correlation': 'float64'}
    df = pd.DataFrame(data, columns=columns)
    
    tickerCategories = CategoricalDtype(categories=list(set(df['mainCompany']) | set(df['secondCompany'])))
    types['mainCompany'] = tickerCategories
    types['secondCompany'] = tickerCategories

    for col in df.columns:
        df[col] = df[col].astype(types[col])
    if dropSelf:
        df = df[df['mainCompany'] != df['secondCompany']]
    df.set_index(['mainCompany', 'secondCompany'], inplace=True)

    return df
    
def _asList(fp):
    data = loadJSON(fp)
    dataList = []
    for mainCompany in data:
        for shift in data[mainCompany]:
            for secondCompany, corr in data[mainCompany][shift].items():
                dataList.append([mainCompany, secondCompany, shift, corr])
    
    return dataList
    
if __name__ == '__main__':
    fp = moveDirUp('buildData/results/2014-01-01_2018-12-20_505-sp500_505-sp500_1-1.json')
    
    cProfile.run("""
df = sortedDF(fp, dropSelf=True)
print(df)
    """, sort='cumtime')