import os
from buildData.manageResults import asDF
import cProfile

def moveDirUp(fileName):
    baseDir = os.getcwd()
    baseDir = baseDir[:baseDir.rfind('/')] + '/'
    
    return baseDir + fileName

def sortedDF(fp, dropSelf, ascending=False, minCorr=-1, maxCorr=1, mainCompany=None, secondCompany=None, dayShift=None):
    data = asDF(fp, dropSelf=dropSelf)
    
    if mainCompany is not None:
        data = data.xs(mainCompany, level='mainCompany')
    if secondCompany is not None:
        data = data.xs(secondCompany, level='secondCompany')
    if dayShift is not None:
        data = data[dayShift]
        
    data = data.sort_values('correlation', ascending=ascending)
    data = data[minCorr <= data['correlation']]
    data = data[data['correlation'] <= maxCorr]
    
    return data

fp = moveDirUp('buildData/results/2014-01-01_2018-12-20_sp500_505_1_10.json')
cProfile.run("""
df = sortedDF(fp, dropSelf=True, secondCompany='VZ', dayShift=10)
print(df)
""")