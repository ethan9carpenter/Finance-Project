import json
import pickle

def saveJSON(fp, data):
    with open(fp, 'w') as file:
        json.dump(data, file)

def loadJSON(fp):
    with open(fp) as file:
            results = json.load(file)
    
    return results

def loadPickle(fp):
    with open(fp, 'rb') as file:
        results = pickle.load(file)
        
    return results

def savePickle(fp, data):
    with open(fp, 'wb') as file:
        pickle.dump(data, file)