from datetime import datetime as dt
from buildData.buildCorrelations import _initAnalysis, performAnalysis
import cProfile

start = dt(2014, 1, 1)
end  = dt(2018, 12, 20)
which = 'sp500'
minShift = 1
maxShift = 1
saveType = 'json'
tickers, fp = _initAnalysis(which, start, end, minShift, maxShift, saveType)
loadDataType = 'pickle'
overwrite = True

cProfile.run('''
performAnalysis(stocks=tickers, start=start, end=end, minShift=minShift, 
maxShift=maxShift, fp=fp, loadDataType=loadDataType, overwrite=overwrite)''', sort='cumtime')