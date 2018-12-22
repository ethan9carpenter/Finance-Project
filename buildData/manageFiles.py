import json
import pickle
from json.decoder import JSONDecodeError

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
        pickle.dump(data, file)
  
"""      
def j():
    a = pd.read_json('data/json/{}.json'.format('aapl'), typ='series')
    b = pd.read_json('data/json/{}.json'.format('amzn'), typ='series')
    a.corr(b)
def p(): 
    a = pd.read_pickle('data/pickles/{}.pickle'.format('aapl'))
    b = pd.read_pickle('data/pickles/{}.pickle'.format('amzn'))
    a.corr(b)

import pandas as pd
import timeit
print(timeit.timeit(j, number = 1000))
print(timeit.timeit(p, number = 1000))
"""