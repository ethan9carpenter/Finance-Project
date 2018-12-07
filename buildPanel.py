from pprint import pprint
import pandas as pd
from datetime import datetime
from iexfinance.stocks import get_historical_data
import json

def getCorrelations(tickData, otherData, dayShift, shiftFactor=1, numDecimals=2):
    correlations = []
    tickDF = pd.DataFrame(tickData)
    otherDF = pd.DataFrame(otherData)
    df = tickDF.join(otherDF)

    tick = df.columns[0]
    
    for shift in range(dayShift+1):
        shift *= shiftFactor
        dfCopy = df.copy(deep=False)
        dfCopy[tick] = dfCopy[tick].shift(shift)
        corr = df.corr()
        corr = corr.iloc[1, 0]
        corr = '{0:.3}'.format(corr)
        correlations.append(corr)
    return correlations

def getData(ticker, start=datetime(2017, 1, 1), end=datetime.now()):
    data = get_historical_data(ticker, start, end, output_format='pandas')
    data = data['close']
    data.name = ticker
    return data

def loadTickers():
    with open('sp500tickers.json', 'r') as file:
        tickers = ('AMZN', 'AAPL', 'FB', 'NKE', 'UA', 'GOOGL', 'DIS')
        #tickers = json.load(file)[0:10]
    return tickers



def performAnalysis(writeData=False):
    masterCorrelationMap = {}

    for tick in tickers:
        tickData = getData(tick, start, end)
        masterCorrelationMap[tick] = {}
        for otherTick in tickers:
            if otherTick is not tick:
                otherData = getData(otherTick, start, end)
                correlations = getCorrelations(tickData, otherData, dayShift)
                masterCorrelationMap[tick][otherTick] = correlations
                
    if writeData:
        with open('sp500results.json', 'w') as file:
            json.dump(masterCorrelationMap, file)
    pprint(masterCorrelationMap)

    return masterCorrelationMap

if __name__ == '__main__':
    dayShift = 1
    tickers = loadTickers()
    start = datetime(2014, 1, 1)
    end = datetime.now()
    performAnalysis()