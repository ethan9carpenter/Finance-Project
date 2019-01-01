import json
import pandas as pd
from os.path import exists
from managers import saveJSON, loadJSON
#from buildData.cleanResults import _tidyDictResults

def loadResults(fp):
    if exists(fp):
        results = loadJSON(fp)
    else:        
        results = {}
    return results
                
def saveProgress(fp, tickResults, tick):
    tickResults = pd.Series.to_json(tickResults)
    if exists(fp):
        with open (fp, mode="r+") as file:
            file.seek(0, 2) # move cursor to end
            position = file.tell() - 1 # move back one
            file.seek(position) # move cursor
            file.write(",\n{}{}{}{}".format(json.dumps(tick), ': ', tickResults, '}'))
    else:
        with open (fp, mode="w") as file:
            file.write((5*"{}").format('{', json.dumps(tick), ': ', tickResults, '}'))

def backupResults(fp):
    data = _tidyDictResults(fp)
    fileName = fp[fp.find('/')+1:]
    fp = 'backupResults/{}'.format(fileName)
    saveJSON(fp, data)

if __name__ == '__main__':
    backupResults('results/2014-01-01_2018-12-20_iex-8719_iex-8719_1_1.json')

    