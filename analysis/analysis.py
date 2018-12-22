from buildData.manageFiles import loadJSON
from pprint import pprint as print
from operator import itemgetter
import os
import pandas as pd

def moveDirUp():
    baseDir = os.getcwd()
    baseDir = baseDir[:baseDir.rfind('/')]
    os.chdir(baseDir)

def convertToList(corrDict, minShift):
    results = {}
    for mainComp in corrDict:
        results[mainComp] = []
        for secondComp in corrDict[mainComp]:
            for i, value in enumerate(corrDict[mainComp][secondComp]):
                results[mainComp].append([value, i+minShift, secondComp])
    
    return results

def toDF(data):
    formatted = []
    for key in data:
        for i, pair in enumerate(data[key]):
            pair = [key] + pair + [i]
            formatted.append(pair)
    return pd.DataFrame(formatted, columns=['mainCompany', 'corr', 'dayShift', 'secondCompany', 'rank'])
    
    

moveDirUp()
data = loadJSON('buildData/results/2014-01-01_2018-12-20_fangs_4_35_200.json')
minShift = 35
results = convertToList(data, minShift)
ordered = {}
howMany = 4

for company in results:
    listed = results[company]
    ordered[company] = sorted(listed, key=itemgetter(0), reverse=True)[:howMany]
df = toDF(ordered)

print(df)



