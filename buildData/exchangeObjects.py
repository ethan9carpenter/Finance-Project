

class TickerList():
    def __init__(self, tickers, name=None):
        self.tickers = [tick.lower() for tick in set(tickers)]
        if name is None:
            name = 'custom'
        self.name = name
        
    def __len__(self):
        return len(self.tickers)
    
    def __getitem__(self, key):
        return self.tickers[key]
    
    def __str__(self):
        return self.name