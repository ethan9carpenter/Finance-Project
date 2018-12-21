from buildData.manageFiles import loadJSON
from pprint import pprint as print
from operator import itemgetter
import os

def moveDirUp():
    baseDir = os.getcwd()
    baseDir = baseDir[:baseDir.rfind('/')]
    os.chdir(baseDir)

moveDirUp()
data = loadJSON('buildData/results/2014-01-01_2018-12-20_fangs_4_0_10.json')
results = {}
ordered = {}
howMany = 5
afterNDays = 1

for mainComp in data:
    results[mainComp] = []
    for secondComp in data[mainComp]:
        for i, value in enumerate(data[mainComp][secondComp]):
            results[mainComp].append([value, i, secondComp])

for company in results:
    listed = results[company]
    ordered[company] = sorted(listed, key=itemgetter(1))[:howMany]

print(ordered)



