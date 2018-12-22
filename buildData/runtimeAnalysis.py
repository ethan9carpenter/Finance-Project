from datetime import datetime as dt
from buildData.buildCorrelations import _initAnalysis, performAnalysis

start = dt(2014, 1, 1)
end  = dt(2018, 12, 20)
which = 'sp500'
minShift = 1
maxShift = 1
tickers, fp = _initAnalysis(which, start, end, minShift, maxShift)
loadDataType = 'pickle'

import cProfile
cProfile.run('''
performAnalysis(stocks=tickers, start=start, end=end, minShift=minShift, 
maxShift=maxShift, fp=fp, loadDataType=loadDataType, overwrite=True)''', sort='cumtime')