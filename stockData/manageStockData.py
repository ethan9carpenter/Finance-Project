from iexfinance.stocks import get_historical_data
import pandas as pd
from managers import loadJSON
from correlations import printMessage
from os import path

#To load data from the proper folder
dataFolder = path.dirname(path.abspath(__file__)) + '/data' 

def validateSymbols(symbols, start, end, what, fileType):
    """
    Validates that all stocks in 'symbols' have data written locally.
    If the stock does not have a local file, one will be written.
    
    @param symbols: A list of stock symbols
    @param start: The start date to load the data if the stock 
        does not have any written data.
    @param end: The end date to load the data if the stock 
        does not have any written data.
    @param what: What type of data to write from ['open', 'high',
        'low', 'close']
    @param fileType: The type of file to load, and write if the
        file does not exist.
    """
    invalid = []
    
    for tick in symbols:
        if not path.exists('{}/{}/{}.{}'.format(dataFolder, fileType, tick, fileType)):
            invalid.append(tick) 
    writeStocks(invalid, start, end, what=what, fileType=fileType)

def getData(ticker, start, end, what='close'):
    """
    Gets historical data for 'ticker' from 'start' to 'end'.
    
    @param ticker: The ticker of the company to get data of
    @param start: Start of the period to get data
    @param end: The of the period to get data
    @param what: What type of data to return from ['open', 'high',
        'low', 'close']
    
    @return: A Series of historical data for 'ticker' from
        'start' to 'end'.
    """
    data = get_historical_data(ticker, start, end, output_format='pandas')
    data = data[what]
    data.name = ticker
    return data

def writeStocks(tickers, start, end, fileType, what='close'):
    """
    Writes data for all of the stocks in 'tickers'
    
    @param tickers: List of tickers to write data for
    @param start: Start of the period to write data
    @param end: End of the period to write data
    @param fileType: Type/format of file to save data.  Options are
        'json' and 'pickle'
    @param what: What type of data to return from ['open', 'high',
        'low', 'close']
    """
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
    """
    Loads the stocks in 'tickers' from 'start' to 'end'.
    
    @param tickers: List of tickers to load
    @param fileType: The file type to load the stocks from.  Options are
        'json' and 'pickle'.
    @param start: Start of the period to load data
    @param end: End of the period to load data
    
    @return: A single pandas object with the stock data of all companies
        in 'tickers'.
    """
    if isinstance(tickers, str):
        if fileType == 'json':
            data = pd.read_json('{}/{}/{}.{}'.format(dataFolder, fileType, tickers, fileType), orient='index')
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
    