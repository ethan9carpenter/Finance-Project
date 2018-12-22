import json
import pandas as pd
from os.path import exists
from buildData.manageFiles import loadJSON, saveJSON

def toPanel(fp):
    with open(fp, 'r') as file:
        data = json.load(file)
        
    panel = {}
        
    for tick in data:
        df = pd.DataFrame.from_dict(data[tick], orient='index')
        panel[tick] = df
    
    panel = pd.Panel.from_dict(panel)
    
    return panel

def loadResults(fp, overwrite):
    if exists(fp) and not overwrite:
        results = loadJSON(fp)
    else:        
        results = {}
    return results


    
def saveProgress(fp, overwrite, tickResults, tick):
    results = loadResults(fp, overwrite)
    results[tick] = tickResults #to prevent incomplete writing
    saveJSON(fp, results)
    
    