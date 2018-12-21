from datetime import datetime
from iexfinance.stocks import get_historical_data
import json
import pandas as pd
from manageFiles import loadJSON, saveJSON

def getData(ticker, start=datetime(2017, 1, 1), end=datetime.now(), what='close'):
    data = get_historical_data(ticker, start, end, output_format='pandas')
    data = data[what]
    data.name = ticker
    return data

def writeStocks(tickers, start, end, what):
    for i, tick in enumerate(tickers):
        df = getData(tick, start, end, what)
        df.to_pickle('data/pickles/{}.pickle'.format(tick))
        print(i+1, '/', len(tickers))
        
def toPanel(fp):
    with open(fp, 'r') as file:
        data = json.load(file)
        
    panel = {}
        
    for tick in data:
        df = pd.DataFrame.from_dict(data[tick], orient='index')
        panel[tick] = df
    
    panel = pd.Panel.from_dict(panel)
    
    return panel

def loadTickers(which):
    if which == 'iex':
        tickers = loadJSON('tickerLists/iexSymbols.json')['valid']
    elif which == 'sp500':
        tickers = loadJSON('tickerLists/sp500tickers.json')
    elif which == 'fangs':
        tickers = ['fb', 'aapl', 'googl', 'nflx']
    else:
        tickers = []
        
    return tickers