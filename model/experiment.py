from datetime import datetime as dt
from managers import moveDirUp
from model import buildFeatureDF, splitXY
from correlations import TickerList, formatFP
import pandas as pd
import numpy as np

from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.svm import LinearSVC, LinearSVR
from sklearn.model_selection import train_test_split
from sklearn.linear_model.base import LinearRegression


def actualReturn(data, ticker=None, start=None, end=None):
        if isinstance(data, pd.DataFrame):
            data = data[ticker]
        if start is None:
            start = data.index[0]
        if end is None:
            end = data.index[-1]

        data = data.loc[start:end]

        actualRet = data.iloc[-1] / data.iloc[0] - 1
        return actualRet
    
def getData(start, end, ticker, sigVal, data, against, minShift, maxShift):
    tl, tl2 = TickerList(data), TickerList(against)
    
    fp = 'correlations/' + formatFP('{}', '{}', tl, tl2, minShift, maxShift, 'json')
    fp = moveDirUp(fp)

    df = buildFeatureDF(fp, start, end, primary=ticker, sigVal=sigVal, dropSelf=False)
    
    df.dropna(inplace=True)
    
    X, y = splitXY(df, yHow='regress', yTyp='price', xHow='regress', xTyp='price')
    xTrain, xTest, yTrain, yTest = train_test_split(X, y, test_size=1/(end.year-start.year+1), shuffle=False)
    
    
    return df, xTrain, xTest, yTrain, yTest


if __name__ == '__main__':
    #===========================================================================
    # build to handle lower and uppercase tickers
    #===========================================================================
    
    data = 'fangs'
    against = 'fangs'
    minShift = 1
    maxShift = 100
    start = dt(2015, 1, 1)
    end = dt(2018, 12, 31)
    
    clf = MLPRegressor(hidden_layer_sizes=[100, 100, 100], max_iter=200)
    
    ticker = 'googl'
    sigVal = 0.7
    
    df, xTrain, xTest, yTrain, yTest = getData(start, end, ticker, sigVal, data, against, minShift, maxShift)
    
    clf.fit(xTrain, yTrain)
    trainScore = clf.score(xTrain, yTrain)

    """
    if trainScore > 0.6:
        score = clf.score(xTest, yTest)
    else:
        score = 1 - clf.score(xTest, yTest)
        trainScore = 1 - trainScore
        print('switch')
        """
        
    pred = pd.DataFrame(clf.predict(xTest), columns=['pred'], index=yTest.index)
    pred[ticker] = yTest
    error = pred[ticker] / pred['pred']
    error = np.abs(error - 1) 
    print('Mean % Error:', '{:.3}%'.format(100*error.mean()))
    
    
    score = clf.score(xTest, yTest)
    ret = 2 * (score - .5)
    actualRet = actualReturn(df, ticker, dt(end.year, 1, 1), end)
    

    print('Significant Companies', len(df.columns))
    print('Train Score:', '{:.3}'.format(trainScore))
    print('Test Score:', '{:.3}'.format(clf.score(xTest, yTest)))
    print('Return:', '{:.3}%'.format(100*ret))
    print('Actual Return:', '{:.3}%'.format(100*actualRet))
    print('Difference:', '{:.3}%'.format(100*(ret-actualRet)))
