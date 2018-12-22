import json
import pandas as pd
from os.path import exists
from buildData.manageFiles import loadPickle, savePickle

def toPanel(fp):
    with open(fp, 'r') as file:
        data = json.load(file)
        
    panel = {}
        
    for tick in data:
        df = pd.DataFrame.from_dict(data[tick], orient='index')
        panel[tick] = df
    
    panel = pd.Panel.from_dict(panel)
    
    return panel

def loadResults(fp):
    if exists(fp):
        results = loadPickle(fp)
    else:        
        results = {}
    return results
    
def saveProgress(fp, tickResults, tick):
    results = loadResults(fp)
    results[tick] = tickResults #to prevent incomplete writing
    savePickle(fp, results)
    
    