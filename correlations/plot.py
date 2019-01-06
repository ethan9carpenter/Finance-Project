import matplotlib.pyplot as plt
from buildData.cleanResults import moveDirUp, sortedDF

fp = moveDirUp('correlations/results/2014-01-01_2018-12-20_505-sp500_505-sp500_1-1.json')

primary = 'aapl'
df = sortedDF(fp, dropSelf=True, allPositive=False, primary=primary, minCorr=.9)
df = df['correlation']

plt.hist(list(df), bins=10)
plt.show()