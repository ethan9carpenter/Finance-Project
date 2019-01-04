from iexfinance.stocks import get_historical_data
import pandas as pd
from managers import loadJSON
from buildData import printMessage
from os import path


dataFolder = path.dirname(path.abspath(__file__)) + '/data' 

def validateSymbols(symbols, start, end, what, fileType):
    invalid = []
    
    for tick in symbols:
        if not path.exists('{}/{}/{}.{}'.format(dataFolder, fileType, tick, fileType)):
            invalid.append(tick) 
    writeStocks(invalid, start, end, what=what, fileType=fileType)

def getData(ticker, start, end, what='close'):
    data = get_historical_data(ticker, start, end, output_format='pandas')
    data = data[what]
    data.name = ticker
    return data

def writeStocks(tickers, start, end, fileType, what='close'):
    printMessage('Writing Stocks')
    for i, tick in enumerate(tickers):
        df = pd.DataFrame(getData(tick, start, end, what))
        if fileType == 'pickle':
            df.to_pickle('{}/pickle/{}.pickle'.format(dataFolder, tick))
        elif fileType == 'json':
            df.to_json('{}/json/{}.json'.format(dataFolder, tick), orient='index')
        print(i+1, '/', len(tickers))

def loadStocks(tickers, fileType, start, end):
    #===========================================================================
    # ADD SOMETHING TO CHECK THAT STOCKS CONTAIN DATES
    #===========================================================================
    if isinstance(tickers, str):
        if fileType == 'json':
            return pd.read_json('{}/{}/{}.{}'.format(dataFolder, fileType, tickers, fileType), orient='index')
        elif fileType == 'pickle':
            data = pd.read_pickle('{}/{}/{}.{}'.format(dataFolder, fileType, tickers, fileType))
            data = data.loc[start:end]
            return data
    else:
        printMessage('Loading Stocks')
        stockData = pd.DataFrame()
        for tick in tickers:
            data = loadStocks(tick, fileType, start=start, end=end)
            stockData[tick] = data[tick]
        stockData = stockData.loc[start:end]
        return stockData
    
if __name__ == '__main__':
    df = pd.read_pickle('data/pickle/aapl.pickle')
    print(df)