import json
import pickle
from json.decoder import JSONDecodeError
import os

def saveJSON(*fp, data=''):
    """
    Saves 'data' as a json file to 'fp'.
    Default will save an empty file to 'fp'. 
    
    @param fp: List that forms the file path to save the data to
    @param data: A json object that can be saved to a .json format
    """
    fp = ''.join(fp)
    with open(fp, 'w') as file:
        json.dump(data, file)

def loadJSON(*fp):
    """
    Loads a json object from 'fp'.  If there is an error reading the file,
    loadJSON will return a json with the last element removed.  This prevents
    erros from exiting during iterative processes and easily handles problems
    that arise from terminating a process mid-writing. 
    
    @param fp: A list of strings that will be joined to form the file path
                that a json will be loaded from
        
    @return: The object stored in 'fp'
    """
    fp = ''.join(fp)
    try:
        with open(fp) as file:
            results = json.load(file)
    except JSONDecodeError:
        print('error loading', fp)
        _handleJSONReadError(fp)
        results = loadJSON(fp)
    
    return results

def _handleJSONReadError(*fp):
    """
    Handles JSONDecodeErrors that arise from incomplete
    writing of a json object.  Rewrites the json with
    the last item removed to allow loadJSON to function
    properly.
    
    @attention: Object stored in 'fp' must be a dictionary
    
    @param fp: The file path that produced an error while reading and will
                be read by the function.
    """
    with open(fp) as file:
        text = file.read()
        index = text.rfind('}')
        text = text[:index] + '}}'
    with open(fp, 'w') as file:
        file.write(text)

def loadPickle(*fp):
    """
    Loads a pickle file from 'fp'

    @param fp: The file path to load the pickle
        
    @return: The object stored in 'fp'
    """
    fp = ''.join(fp)
    with open(fp, 'rb') as file:
        results = pickle.load(file)
    return results

def savePickle(*fp, data):
    """
    Saves 'data' to a pickle at the specifiec location
    
    @param fp: Strings that form the file path to save 'data' to
    @param data: The data to save
    """
    fp = ''.join(fp)
    with open(fp, 'wb') as file:
        pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)

def deleteFile(*fp, writeEmpty=False):
    """
    Deletes the file at 'fp'
    
    @param fp: Strings that form the file path to save 'data' to
    @param writeEmpty: If True, write an empty file to 'fp'
    """
    fp = ''.join(fp)
    if os.path.exists(fp):
        os.remove(fp)
    if writeEmpty:
        with open(fp, 'w') as file:
            file.write('')
        
def pickleToJSON(*fp):
    """
    Loads a pickle file from 'fp' and saves the stored data as a json
    to an identical file name with the extension .json
    
    @param fp: Strings that form the file path to load and then save 
    """
    fp = ''.join(fp)
    pick = loadPickle(fp)
    fp = fp[:fp.rfind('.')] + '.json'
    saveJSON(fp, pick)

    