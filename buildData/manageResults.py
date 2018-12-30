import json
import pandas as pd
from os.path import exists
from managers import loadPickle, savePickle, saveJSON, loadJSON
from contextlib import suppress
from pandas.api.types import CategoricalDtype

def loadResults(fp):
    if exists(fp):
        results = loadJSON(fp)
    else:        
        results = {}
    return results

def _tidyDictResults(fp):
    data = loadResults(fp)
    for mainCompany in data:
        for _ in data[mainCompany]:
            try:
                data[mainCompany] = json.loads(data[mainCompany])
            except TypeError:
                pass   
    return data

def asDF(fp, dropSelf):
    data = _asList(fp)
    columns = {'mainCompany': None,
                'secondCompany': None,
                'dayShift': 'int',
                'correlation': 'float64'}
    df = pd.DataFrame(data, columns=columns.keys())
    
    tickerCategories = CategoricalDtype(categories=list(set(df['mainCompany']) | set(df['secondCompany'])))
    columns['mainCompany'] = tickerCategories
    columns['secondCompany'] = tickerCategories
    
    for col, typ in columns.items():
        df[col] = df[col].astype(typ)
    if dropSelf:
        df = df[df['mainCompany'] != df['secondCompany']]
    df.set_index(['mainCompany', 'secondCompany'], inplace=True)
    print(df.dtypes)

    return df
    
def _asList(fp):
    data = _tidyDictResults(fp)
    dataList = []
    for mainCompany in data:
        for shift in data[mainCompany]:
            for secondCompany, corr in data[mainCompany][shift].items():
                dataList.append([mainCompany, secondCompany, shift, corr])
    
    return dataList

def neatToDF(fp, dropSelf):
    data = loadJSON(fp)
    dataList = []
    with suppress(TypeError):
        for mainCompany in data:
            for shift in data[mainCompany]:
                for secondCompany in data[mainCompany][shift]:
                    corr = data[mainCompany][shift][secondCompany]
                    dataList.append([mainCompany, secondCompany, shift, corr])
    data = dataList
    columns = {'mainCompany': 'str',
                'secondCompany': 'str',
                'dayShift': 'int',
                'correlation': 'float64'}
    df = pd.DataFrame(data, columns=columns.keys())
    for col, typ in columns.items():
        df[col] = df[col].astype(typ)
    if dropSelf:
        df = df[df['mainCompany'] != df['secondCompany']]
    df.set_index(['mainCompany', 'secondCompany'], inplace=True)
    print(df)
    return df
    
    
                
def saveProgress(fp, tickResults, tick):
    tickResults = pd.Series.to_json(tickResults)
    if exists(fp):
        with open (fp, mode="r+") as file:
            file.seek(0, 2) # move cursor to end
            position = file.tell() - 1 #move back one
            file.seek(position) # move cursor
            file.write( ",\n{}{}{}{}".format(json.dumps(tick), ': ', json.dumps(tickResults), '}'))
    else:
        saveJSON(fp, {tick: tickResults})

def backupResults(fp):
    data = _tidyDictResults(fp)
    fileName = fp[fp.find('/')+1:]
    fp = 'backupResults/{}'.format(fileName)
    saveJSON(fp, data)

if __name__ == '__main__':
    backupResults('results/2014-01-01_2018-12-20_sp500_505_1_10.json')

    