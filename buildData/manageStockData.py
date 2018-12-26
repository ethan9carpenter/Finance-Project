from datetime import datetime
from iexfinance.stocks import get_historical_data
import pandas as pd
from buildData.manageFiles import loadJSON
from buildData.monitors import printMessage
from buildData.manageMemory import convertData
from buildData.exchangeObjects import TickerList

def getData(ticker, start=datetime(2017, 1, 1), end=datetime.now(), what='close'):
    data = get_historical_data(ticker, start, end, output_format='pandas')
    data = data[what]
    data.name = ticker
    return data

def writeStocks(tickers, start, end, what, fileType):
    printMessage('Writing Stocks')
    for i, tick in enumerate(tickers):
        df = getData(tick, start, end, what)
        if fileType == 'pickle':
            df.to_pickle('data/pickle/{}.pickle'.format(tick))
        elif fileType == 'json':
            df.to_json('data/json/{}.json'.format(tick))
        print(i+1, '/', len(tickers))

def loadStocks(tickers, fileType, convert=False):
    if isinstance(tickers, str):
        if fileType == 'json':
            return pd.read_json('data/{}/{}.{}'.format(fileType, tickers, fileType))
        elif fileType == 'pickle':
            return pd.read_pickle('data/{}/{}.{}'.format(fileType, tickers, fileType))
    else:
        printMessage('Loading Stocks')
        stockData = pd.DataFrame()
        for tick in tickers:
            stockData[tick] = loadStocks(tick, fileType)
        if convert:
            convertData(stockData)
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