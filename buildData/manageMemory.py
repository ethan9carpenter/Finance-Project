import pandas as pd
from buildData import manageStockData
#from buildData.manageStockData import loadTickers

def memoryUsage(pandas_obj):
    if isinstance(pandas_obj,pd.DataFrame):
        usage = pandas_obj.memory_usage(deep=True).sum()
    else: # we assume if not a df it's a series
        usage = pandas_obj.memory_usage(deep=True)
    usage = usage / 1024 ** 2 # convert bytes to megabytes
    return "{:03.2f} MB".format(usage)

def convertFloats(df):
    floats = df.select_dtypes(include=['float'])
    converted = floats.apply(pd.to_numeric,downcast='float')
    
    df[converted.columns] = converted
            
def convertInts(df):
    ints = df.select_dtypes(include=['int'])
    converted = ints.apply(pd.to_numeric,downcast='unsigned')
    
    df[converted.columns] = converted

def convertData(df):
    df = pd.DataFrame(df)
    convertFloats(df)
    convertInts(df)
    return df

if __name__ == '__main__':    
    data = manageStockData.loadStocks(loadTickers('sp500'))
    print(memoryUsage(data))
    convertFloats(data)
    convertInts(data)
    print(memoryUsage(data))