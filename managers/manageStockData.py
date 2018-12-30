from datetime import datetime
from iexfinance.stocks import get_historical_data
import pandas as pd
from managers import loadJSON#, convertData
from buildData.monitors import printMessage
from buildData.exchangeObjects import TickerList

def getData(ticker, start, end, what='close'):
    data = get_historical_data(ticker, start, end, output_format='pandas')
    data = data[what]
    data.name = ticker
    return data

def writeStocks(tickers, start, end, what, fileType):
    printMessage('Writing Stocks')
    for i, tick in enumerate(tickers):
        df = pd.DataFrame(getData(tick, start, end, what))
        if fileType == 'pickle':
            df.to_pickle('data/pickle/{}.pickle'.format(tick))
        elif fileType == 'json':
            df.to_json('data/json/{}.json'.format(tick), orient='index')
        print(i+1, '/', len(tickers))

def loadStocks(tickers, fileType, start, end, convert=False):
    #===========================================================================
    # ADD SOMETHING TO CHECK THAT STOCKS CONTAIN DATES
    #===========================================================================
    if isinstance(tickers, str):
        if fileType == 'json':
            return pd.read_json('data/{}/{}.{}'.format(fileType, tickers, fileType), orient='index')
        elif fileType == 'pickle':
            data = pd.read_pickle('data/{}/{}.{}'.format(fileType, tickers, fileType))
            data = data.loc[start:end]
            return data
    else:
        printMessage('Loading Stocks')
        stockData = pd.DataFrame()
        for tick in tickers:
            stockData[tick] = loadStocks(tick, fileType, start=start, end=end)
        if convert:
            convertData(stockData)
        print(stockData)
        stockData = stockData.loc[start:end]
        return stockData

def loadTickers(which):
    if which == 'iex':
        tickers = loadJSON('tickerLists/iexSymbols.json')['valid']
    elif which == 'sp500':
        tickers = loadJSON('tickerLists/sp500tickers.json')
    elif which == 'fangs':
        tickers = ['fb', 'aapl', 'googl', 'nflx']
    else:
        tickers = which
    tickers = TickerList(tickers, name= which if isinstance(which, str) else None)
        
    return tickers