import os
from buildData.manageResults import asDF, neatToDF
import cProfile
import numpy as np

def moveDirUp(fileName, levels=1):
    baseDir = os.getcwd()
    for _ in range(levels):
        if '/' in baseDir:
            baseDir = baseDir[:baseDir.rfind('/')]
            slash = '/'
        else:
            baseDir = baseDir[:baseDir.rfind('\\')]
            slash = '\\'
    
    return baseDir + slash + fileName

def sortedDF(fp, dropSelf, ascending=False, minCorr=-1, maxCorr=1, mainCompany=None, secondCompany=None, 
             dayShift=None, allPositive=False):
    data = asDF(fp, dropSelf=dropSelf)

    if mainCompany is not None:
        data = data.xs(mainCompany, level='mainCompany')
    if secondCompany is not None:
        data = data.xs(secondCompany, level='secondCompany')
    if dayShift is not None:
        data = data[data['dayShift'] == dayShift]
    if allPositive:
        data['correlation'] = np.abs(data['correlation'])
        
    data = data.sort_values('correlation', ascending=ascending)
    data = data[minCorr <= data['correlation']]
    data = data[data['correlation'] <= maxCorr]

    return data

fp = moveDirUp('buildData/results/2014-01-01_2018-12-20_iex-8719_iex-8719_1-1.json')

#cProfile.run("""
df = sortedDF(fp, dropSelf=True)
print(df)
#""", sort='cumtime')