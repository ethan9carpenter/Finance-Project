import json
import pandas as pd
from os.path import exists
from managers import saveJSON, loadJSON
from buildData.results import asDF
from datetime import datetime

def loadResults(fpInfo, returnType='json'):
    #===========================================================================
    # MAKE A BETTER WAY TO ENTER fp OR each fp keyword
    #===========================================================================
    if 'fp' in fpInfo:
        fp = fpInfo['fp']
    else:
        fp = formatFP(fpInfo['start'], fpInfo['end'], fpInfo['tickList'], fpInfo['againstTL'], 
                      fpInfo['minShift'], fpInfo['maxShift'], fpInfo['saveType'])
    if exists(fp):
        if returnType == 'json':
            results = loadJSON(fp)
        elif returnType == 'df':
            results = asDF(fp)
    else:        
        results = {}
    return results

def formatFP(start, end, tickList, againstTL, minShift, maxShift, saveType):
    baseFormat = 'dynamicResults/{}_{}_{}-{}_{}-{}_{}-{}.{}' 
    start, end = _handleFP(start, end)
    
    
    fp = baseFormat.format(start, end, 
                           len(tickList), tickList, 
                           len(againstTL), againstTL, 
                           minShift, maxShift, 
                           saveType)
    return fp

def _handleFP(start, end):
    if not isinstance(start, datetime):
        start = '{}'
    else:
        start = start.date()
    if not isinstance(end, datetime):
        end = '{}'
    else:
        end = end.date()
    return start, end
                
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
    data = loadJSON(fp)
    fileName = fp[fp.find('/')+1:]
    fp = 'backupResults/{}'.format(fileName)
    saveJSON(fp, data)

if __name__ == '__main__':
    backupResults('results/2014-01-01_2018-12-20_iex-8719_iex-8719_1_1.json')

    