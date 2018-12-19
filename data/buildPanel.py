import pandas as pd
from datetime import datetime
from iexfinance.stocks import get_historical_data, Stock
from iexfinance import get_available_symbols
import json
from datetime import datetime as dt
import os, time

def getCorrelations(data, otherData, dayShift, shiftFactor=1, limitDecimals=False):
    correlations = []
    df = pd.DataFrame(data)
    otherDF = pd.DataFrame(otherData)
    df = df.join(otherDF)

    name = df.columns[0]
    
    for shift in range(dayShift+1):
        shift *= shiftFactor
        dfCopy = df.copy(deep=False)
        dfCopy[name] = dfCopy[name].shift(shift)
        corr = df.corr()
        corr = corr.iloc[1, 0]
        if limitDecimals:
            corr = '{0:.3}'.format(corr)
            corr = float(corr)
        correlations.append(corr)
    return correlations

def getData(ticker, start=datetime(2017, 1, 1), end=datetime.now(), type='close'):
    try:
        data = get_historical_data(ticker, start, end, output_format='pandas')
        data = data[type]
        data.name = ticker
        return data
    except Exception as error:
        print(error)
        raise Exception(ticker)

def _saveJSON(fp, data):
    with open(fp, 'w') as file:
        json.dump(data, file)

def _loadJSON(fp):
    with open(fp) as file:
            results = json.load(file)
    
    return results
    
def toPanel(fp):
    with open(fp, 'r') as file:
        data = json.load(file)
        
    panel = {}
        
    for tick in data:
        df = pd.DataFrame.from_dict(data[tick], orient='index')
        panel[tick] = df
    
    panel = pd.Panel.from_dict(panel)
    
    return panel

def _shouldCompare(otherTick, tick, results):
    sameTick  = otherTick is  tick 
    needToAnalyze  = otherTick not in results[tick]
    
    return not sameTick and needToAnalyze

def performAnalysis(tickers, start, end=dt.now(), dayShift=1, shiftFactor=1, fp=None, 
                    overwrite=False, returnType='panel'):
    tickers = _validateSymbols(tickers, fp='iexSymbols.json')
    
    if fp and os.path.exists(fp) and not overwrite:
        results = _loadJSON(fp)
    else:        
        results = {}

    for i, tick in enumerate(tickers):
        tickData = getData(tick, start, end)
        results[tick] = {}
        for otherTick in tickers:
            if _shouldCompare(otherTick, tick, results):
                otherData = getData(otherTick, start, end)
                correlations = getCorrelations(tickData, otherData, dayShift, shiftFactor)
                results[tick][otherTick] = correlations
        if fp is not None:
            _saveJSON(fp, results)
            print(i+1, 'out of', len(tickers))
            
    print('Done')
    
    if returnType == 'dict':
        return results
    elif returnType == 'panel':
        return toPanel(fp)
    
def _validateSymbols(symbols, fp=None):
    if fp is not None and os.path.exists(fp):
        results = _loadJSON(fp)
        for symb in results['valid']+results['invalid']:
            symbols.remove(symb)
    else:
        results = {'valid': [],
                   'invalid': []}

    for i, symb in enumerate(symbols):
        try:
            get_historical_data(symb)
            results['valid'].append(symb)
        except:
            results['invalid'].append(symb)
        
        if fp is not None and i % 10 == 0:
            print(i / len(symbols))
            _saveJSON(fp, results)
        
    
    if fp is not None:
        _saveJSON(fp, results)
    print('Invalid:', results['invalid'])
    print('Total Invalid:', len(results['invalid']))
    return results['valid']

if __name__ == '__main__':
    symbols = get_available_symbols()
    tickers = [tick['symbol'] for tick in symbols]
    print(len(tickers), 'total tickers')
    #tickers = ['aapl', 'a', 'amzn', 'hd', 'low', 'nflx']
    start = dt(2014, 1, 1)
    end  = dt.now()
    performAnalysis(tickers, start, end, dayShift=7, fp='allIEXStocks.json', overwrite=False)
