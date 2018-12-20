import pandas as pd
from datetime import datetime as dt
import os
from manageFiles import loadJSON, saveJSON, loadPickle
from manageData import toPanel, writeStocks

def getCorrelations(data, otherData, dayShift, shiftFactor=1):
    correlations = []
    otherDF = pd.DataFrame(otherData)
    df = data.join(otherDF)

    name = df.columns[0]
    for i in range(dayShift+1):
        if i > 0:
            df[name] = df[name].shift(shiftFactor)
        corr = df.corr()
        corr = corr.iloc[1, 0]
        correlations.append(corr)
    return correlations

def performAnalysis(tickers, start, end=dt.now(), dayShift=1, shiftFactor=1, fp=None, 
                    overwrite=False, returnType='panel'):    
    if fp and os.path.exists(fp) and not overwrite:
        results = loadJSON(fp)
    else:        
        results = {}

    for i, tick in enumerate(tickers):
        tickData = loadPickle('data/{}.pickle'.format(tick))
        tickData = pd.DataFrame(tickData)
        results[tick] = {}
        for otherTick in tickers:
            if otherTick is not tick:
                otherData = loadPickle('data/{}.pickle'.format(otherTick))
                correlations = getCorrelations(tickData, otherData, dayShift, shiftFactor)
                results[tick][otherTick] = correlations
        if fp is not None:
            saveJSON(fp, results)
            print(i+1, 'out of', len(tickers))
    print('Done')
    
    if returnType == 'dict':
        return results
    elif returnType == 'panel':
        return toPanel(fp)
    
def _validateSymbols(symbols, fp=None):
    if fp is not None and os.path.exists(fp):
        results = loadJSON(fp)
        for symb in results['valid']+results['invalid']:
            symbols.remove(symb)
    else:
        results = {'valid': [],
                   'invalid': []}

    """
    for i, symb in enumerate(symbols):
        try:
            get_historical_data(symb)
            results['valid'].append(symb)
        except:
            results['invalid'].append(symb)
        
        if fp is not None and i % 10 == 0:
            print(i / len(symbols))
            _saveJSON(fp, results)
    """   
    
    if fp is not None:
        saveJSON(fp, results)
    print('Invalid:', results['invalid'])
    print('Total Invalid:', len(results['invalid']))
    return results['valid']

if __name__ == '__main__':
    tickers = loadJSON('iexSymbols.json')['valid']
    print(len(tickers), 'total tickers')
    #tickers = ['aapl', 'a', 'amzn', 'hd', 'low', 'nflx']
    start = dt(2014, 1, 1)
    end  = dt.now()
    writeStocks(tickers, start, end, 'close')

    performAnalysis(tickers, start, end, dayShift=1, fp='allIEXStocks.json', overwrite=False)
