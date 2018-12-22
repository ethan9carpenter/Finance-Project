from buildData.manageFiles import loadJSON
from pprint import pprint as print
from operator import itemgetter
import os

def moveDirUp():
    baseDir = os.getcwd()
    baseDir = baseDir[:baseDir.rfind('/')]
    os.chdir(baseDir)

moveDirUp()
data = loadJSON('buildData/results/2014-01-01_2018-12-20_sp500_505_1_1.json')
results = {}
ordered = {}
howMany = 1
afterNDays = 1


for mainComp in data:
    results[mainComp] = []
    for secondComp in data[mainComp]:
        for i, value in enumerate(data[mainComp][secondComp]):
            results[mainComp].append([value, i, secondComp])

for company in results:
    listed = results[company]
    ordered[company] = sorted(listed, key=itemgetter(0), reverse=True)[:howMany]

print(ordered)



