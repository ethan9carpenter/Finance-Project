from random import shuffle
from managers import loadJSON

class TickerList():
    def __init__(self, tickers, name=None):
        if isinstance(tickers, str):
            tickers, name = self._loadTickerPack(tickers)
        self.tickers = [tick.lower() for tick in set(tickers)]
        if len(tickers) == 1:
            name = tickers[0]
        elif name is None:
            name = 'custom'
        self.name = name
        
    def _loadTickerPack(self, which):
        if which == 'iex':
            tickers = loadJSON('tickerLists/iexSymbols.json')['valid']
        elif which == 'sp500':
            tickers = loadJSON('tickerLists/sp500tickers.json')
        elif which == 'fangs':
            tickers = ['fb', 'aapl', 'googl', 'nflx']
        else:
            tickers = [which] #assume just a single stock
            
        name = which if isinstance(which, str) else None
            
        return tickers, name
        
    def __len__(self):
        return len(self.tickers)
    
    def __getitem__(self, key):
        return self.tickers[key]
    
    def __str__(self):
        return self.name
    
    def remove(self, key):
        self.tickers.remove(key)   
    
    def trimTo(self, howMany, random=False, inplace=False):
        if random:
            tickers = shuffle(self.tickers)[:howMany]
        else:
            tickers = self.tickers[:howMany]
        
        if inplace:
            self.tickers = tickers
            return self
        else:
            return TickerList(tickers, self.name)