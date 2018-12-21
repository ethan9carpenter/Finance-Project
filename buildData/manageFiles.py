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