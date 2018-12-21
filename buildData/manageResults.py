import json
import pandas as pd
from os.path import exists
from buildData.manageFiles import loadJSON
from json.decoder import JSONDecodeError

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
    if fp and exists(fp) and not overwrite:
        try:
            results = loadJSON(fp)
        except JSONDecodeError:
            results = _handleJSONReadError(fp)
    else:        
        results = {}
    return results

def _handleJSONReadError(fp):
    with open(fp) as file:
        text = file.read()
        index = text.rfind('}')
        text = text[:index] + '}}'
    with open(fp, 'w') as file:
        file.write(text)
    with open(fp) as file:
        return loadJSON(fp)