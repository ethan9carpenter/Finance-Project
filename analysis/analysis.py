import os
from buildData.manageResults import asDF, neatToDF
import cProfile

def moveDirUp(fileName, levels=1):
    baseDir = os.getcwd()
    for _ in range(levels):
        baseDir = baseDir[:baseDir.rfind('/')]
    
    return baseDir + '/' + fileName

def sortedDF(fp, dropSelf, ascending=False, minCorr=-1, maxCorr=1, mainCompany=None, secondCompany=None, dayShift=None):
    data = asDF(fp, dropSelf=dropSelf)

    if mainCompany is not None:
        data = data.xs(mainCompany, level='mainCompany')
    if secondCompany is not None:
        data = data.xs(secondCompany, level='secondCompany')
    if dayShift is not None:
        data = data[data['dayShift'] == dayShift]
        
    data = data.sort_values('correlation', ascending=ascending)
    data = data[minCorr <= data['correlation']]
    data = data[data['correlation'] <= maxCorr]

    return data

fp = moveDirUp('buildData/results/2018-01-01_2018-12-20_4-fangs_4-fangs_1-1.json')

cProfile.run("""
df = sortedDF(fp, dropSelf=True, mainCompany='aapl')
print(df)
""", sort='cumtime')