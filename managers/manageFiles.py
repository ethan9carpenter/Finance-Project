import json
import pickle
from json.decoder import JSONDecodeError
import os

def saveJSON(fp, data):
    with open(fp, 'w') as file:
        json.dump(data, file)

def loadJSON(fp):
    try:
        with open(fp) as file:
                results = json.load(file)
    except JSONDecodeError:
        print('error loading', fp)
        results = _handleJSONReadError(fp)
    
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

def loadPickle(fp):
    with open(fp, 'rb') as file:
        results = pickle.load(file)
    return results

def savePickle(fp, data):
    with open(fp, 'wb') as file:
        pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)

def deleteFile(fp):
    if os.path.exists(fp):
        os.remove(fp)
        
def pickleToJSON(fp):
    pick = loadPickle(fp)
    fp = fp[:fp.rfind('.')] + '.json'
    saveJSON(fp, pick)
    