import pandas as pd
from stockData import loadStocks
from buildData.results import sortedDF
from model.labels import LabelType

def _trimToSig(data, sigCols, sigVal):
    for col in sigCols:
        data = data[data[col] > sigVal]
    
    return data
    
def _merge(data):
    df = pd.DataFrame()
    for period, corrs in data.items():
        df[str(period)] = corrs['correlation']
    return df

def _selectSignificant(data):
    df = data.reset_index()

    stocks = set(df['primary'])
    sigPairs = {}
    for stock in stocks:
        stockData = df[df['primary'] == stock]
        sigPairs[stock] = list(zip(stockData['secondary'], stockData['dayShift']))

    return sigPairs

def _buildSelectionDF(sigData, stock, start, end):
    #if stock in sigData:
    data = sigData[stock]
    #else:
    #   data = pd.DataFrame()
    #===========================================================================
    # HANDLE ERRORS IN A GOOD WAY
    #===========================================================================
    toLoad = [stock] + list(dict(data).keys())
    stockData = loadStocks(toLoad, start=start, end=end, fileType='pickle')
    selectionDF = pd.DataFrame()
    
    for otherTick, shift in data:
        name = '{}-{}'.format(otherTick, shift)
        selectionDF[name] = stockData[otherTick].shift(shift)
    
    selectionDF[stock] = stockData[stock]
    
    return selectionDF

def buildFeatureDF(baseFP, start, end, primary, sigVal, dropSelf=False):
    data = {}

    for year in range(start.year, end.year+1):
        data[str(year)] = sortedDF(baseFP.format(year, year), dropSelf=dropSelf, allPositive=True)
    df = _merge(data)
    df = _trimToSig(df, sigCols=df.columns[:-1], sigVal=sigVal)
    df = _buildSelectionDF(_selectSignificant(df), primary, start=start, end=end)
    
    return df

def splitXY(featureDF, labelType, labelColumn=-1):
    X = featureDF.drop(featureDF.columns[labelColumn], axis=1)
    y = featureDF[featureDF.columns[labelColumn]]
    X = np.array(X)
    y = labelType.formatY(y)
    
    return X, y
    
if __name__ == '__main__':
    from datetime import datetime as dt
    from sklearn.neural_network import MLPRegressor, MLPClassifier
    import numpy as np
    from sklearn.model_selection import train_test_split
    from managers import moveDirUp
    #===========================================================================
    # build to handle lower and uppercase tickers
    #===========================================================================
    
    
    
    ticker = 'aapl'
    sigVal = 0.6
    typ = 'classify'
    start = 2015
    end = 2018
    
    fp = moveDirUp('buildData/dynamicResults/{}-01-01_{}-12-31_505-sp500_505-sp500_1-1.json', levels=1)
    df = buildFeatureDF(fp, dt(start, 1, 1), dt(end, 12, 31), primary=ticker, sigVal=sigVal, dropSelf=False)

    df.dropna(inplace=True)
    X, y = splitXY(df, LabelType(typ, changeType=1))
    xTrain, xTest, yTrain, yTest = train_test_split(X, y, test_size=1/(end-start+1), shuffle=False)

    def actualReturn():
        _, data = splitXY(df, LabelType('regress'))
        *_, data = train_test_split(X, data, test_size=1/(end-start+1), shuffle=False)
        actualRet = (data.iloc[-1] - data.iloc[0]) / data.iloc[0]
        return actualRet  
    
    clf = MLPClassifier()
    clf.fit(xTrain, yTrain)

    if clf.score(xTrain, yTrain) > .5:
        score = clf.score(xTest, yTest)
    else:
        score = 1 - clf.score(xTest, yTest)
        print('switch')
    ret = 2 * (score - .5)
    actualRet = actualReturn()
    

    print('Significant Companies', len(df.columns))
    print('Train Score:', max(1-clf.score(xTrain, yTrain), clf.score(xTrain, yTrain)))
    print('Return:', '{:.3}%'.format(100*ret))
    print('Actual Return:', '{:.3}%'.format(100*actualRet))
    print('Difference:', '{:.3}%'.format(100*(ret-actualRet)))
