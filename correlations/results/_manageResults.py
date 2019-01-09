import json
import pandas as pd
from os import path
from managers import saveJSON, loadJSON
from datetime import datetime

__dataFolder = path.dirname(path.abspath(__file__)) + '/'

def loadResults(fp, returnType='json'):
    #===========================================================================
    # MAKE A BETTER WAY TO ENTER fp OR each fp keyword
    #===========================================================================
    if isinstance(fp, str):
        fp = ''.join([__dataFolder, fp])
    elif isinstance(fp, dict):
        fp = formatFP(fp['start'], fp['end'], fp['tickList'], fp['againstTL'], 
                      fp['minShift'], fp['maxShift'], fp['saveType'])
    if path.exists(fp):
        if returnType == 'json':
            results = loadJSON(fp)
        #elif returnType == 'df':
            #results = asDF(fp)
    else:        
        results = {}

    return results

def formatFP(start, end, tickList, againstTL, minShift, maxShift, saveType):
    baseFormat = __dataFolder + 'dynamicResults/{}_{}_{}-{}_{}-{}_{}-{}.{}' 

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
    if path.exists(fp):
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
    saveJSON(__dataFolder, fp, data=data)

def _asList(fp):
    data = loadResults(fp)
    
    dataList = []
    for primary in data:
        for shift in data[primary]:
            for secondary, corr in data[primary][shift].items():
                dataList.append([primary, secondary, shift, corr])
    
    return dataList