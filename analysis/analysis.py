import os
from buildData.manageResults import asDF

def moveDirUp(fileName):
    baseDir = os.getcwd()
    baseDir = baseDir[:baseDir.rfind('/')] + '/'
    
    return baseDir + fileName

def sortedDF(fp, dropSelf, ascending=False, minCorr=-1, maxCorr=1, mainCompany=None, secondCompany=None):
    data = asDF(fp, dropSelf=dropSelf)
    data = data.sort_values('correlation', ascending=ascending)
    data = data[minCorr <= data['correlation']]
    data = data[data['correlation'] <= maxCorr]
    
    if mainCompany is not None:
        data = data.xs(mainCompany, level='mainCompany')
    if secondCompany is not None:
        data = data.xs(secondCompany, level='secondCompany')
    return data

fp = moveDirUp('buildData/results/2014-01-01_2018-12-20_sp500_505_1_1.json')
df = sortedDF(fp, dropSelf=True, mainCompany='AAPL')
print(df)