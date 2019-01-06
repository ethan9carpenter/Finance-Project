from datetime import datetime as dt
from buildData.buildCorrelations import performAnalysis
import cProfile

start = dt(2014, 1, 1)
end  = dt(2018, 12, 20)
which = 'sp500'
minShift = 1
maxShift = 1
saveType = 'json'
against = 'fangs'
loadDataType = 'pickle'
overwrite = True

cProfile.run('''
performAnalysis(stocks=which, against=against, 
                         start=start, end=end, 
                         minShift=minShift, maxShift=maxShift, 
                         saveType=saveType, loadDataType=loadDataType, 
                         overwrite=overwrite)
''', sort='cumtime')