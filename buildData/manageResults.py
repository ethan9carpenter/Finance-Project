import json
import pandas as pd
from os.path import exists
from buildData.manageFiles import loadPickle, savePickle, saveJSON, loadJSON
from pprint import pprint
    
def toPanel(fp):
    with open(fp, 'r') as file:
        data = json.load(file)
        
    panel = {}
        
    for tick in data:
        df = pd.DataFrame.from_dict(data[tick], orient='index')
        panel[tick] = df
    
    panel = pd.Panel.from_dict(panel)
    
    return panel

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
    columns = {'mainCompany': 'category',
                'secondCompany': 'category',
                'dayShift': 'int',
                'correlation': 'float64'}
    df = pd.DataFrame(data, columns=columns.keys())
    for col, typ in columns.items():
        df[col] = df[col].astype(typ)
    if dropSelf:
        df = df[df['mainCompany'] != df['secondCompany']]
    df.set_index(['mainCompany', 'secondCompany'], inplace=True)

    return df
    
def _asList(fp):
    data = _tidyDictResults(fp)
    dataList = []
    for mainCompany in data:
        for shift in data[mainCompany]:
            for secondCompany, corr in data[mainCompany][shift].items():
                dataList.append([mainCompany, secondCompany, shift, corr])
    
    return dataList
                
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
    pass

if __name__ == '__main__':
    print(toDF('results/2014-01-01_2018-12-20_fangs_4_1_10.json'))

    