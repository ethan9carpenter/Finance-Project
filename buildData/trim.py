from buildData.results import writeDF, readDF
import time
    
def trim():    
    from scipy import stats
    from sklearn.linear_model import LinearRegression
    import numpy as np
    import pandas as pd
    from buildData.results import sortedDF
    
    fp = 'results/{}-01-01_{}-12-31_505-sp500_505-sp500_1-100.json'
    df = pd.DataFrame()
    for year in range(2015, 2019):
        data = sortedDF(fp.format(year, year), dropSelf=True, allPositive=True, primary=None)
        #print(data)
        df[str(year)] = data['correlation']
    
    print(df.sort_values('2018', ascending=False))
    critVal = -1
    
    df = df[df['2015'] > critVal]
    df = df[df['2016'] > critVal]
    #df = df[df['2017'] > critVal]
    
    
    df['geomean'] = stats.gmean(df.iloc[:,0:1], axis=1)
    #df = df[df['geomean'] > critVal]
    df.sort_values('2017', ascending=False, inplace=True)
    
    df.dropna(inplace=True)
    
    clf = LinearRegression()
    clf.fit(X=np.array(df[['2015', '2016']]), y=np.array(df['2017']))
    
    print(df.describe()) 
    print(clf.score(X=np.array(df[['2015', '2016']]), y=np.array(df['2017'])))


def printPartial(fp, numChars=10000):
    with open(fp, 'r') as file:
        cont = file.read()
        print(cont[:numChars])