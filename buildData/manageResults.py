import json
import pandas as pd
from os.path import exists
from buildData.manageFiles import loadPickle, savePickle, saveJSON, loadJSON
    
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
        results = loadJSON(fp)
    else:        
        results = {}
    return results

def saveProgress(fp, tickResults, tick):
    tickResults = pd.Series.to_json(tickResults)
    if exists(fp):
        with open (fp, mode="r+") as file:
            file.seek(0, 2) # move cursor to end
            position = file.tell() - 1 #move back one
            file.seek(position) # move cursor
            file.write( ",\n{}{}{}{}".format(json.dumps(tick), ': ', json.dumps(tickResults), '}'))
    else:
        saveJSON(fp, {tick: tickResults})
    

if __name__ == '__main__':
    print(loadJSON('results/2014-01-01_2018-12-20_fangs_4_1_1.json'))
    