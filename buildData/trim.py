from scipy import stats
from buildData.results import sortedDF
from buildData.choose import merge, choose
    
def trim(fp, years=range(2015, 2019), ascending=True, dropSelf=False, allPositive=False,
         primary=None, secondary=None, dayShift=None):
    
    data = {}
    for year in years:
        data[str(year)] = sortedDF(fp.format(year, year), dropSelf=dropSelf, allPositive=allPositive, 
                                   primary=primary, secondary=secondary, dayShift=dayShift)
    df = merge(data)
    
    return choose(df, sigCols=df.columns[:-1], sigVal=.5)
    exit()
    df.dropna(inplace=True)

    for year in years[:-1]:
        df = df[df[str(year)] > 0.5]
    
    df['geo'] = stats.gmean(df.iloc[:,0:3], axis=1)
    df.sort_values('geo', ascending=False, inplace=True)
    print(df.head(10))
    
    #df.sort_values('2017', ascending=False, inplace=True)
    
    #df.dropna(inplace=True)
    print(df.describe()['2018']) 


def printPartial(fp, numChars=10000):
    with open(fp, 'r') as file:
        cont = file.read()
        print(cont[:numChars])
        
if __name__ == '__main__':
    fp = 'dynamicResults/{}-01-01_{}-12-31_4-fangs_4-fangs_1-100.json'
    trim(fp=fp, allPositive=True, dropSelf=True)