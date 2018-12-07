import requests
from pprint import pprint
import json
from datetime import datetime
from iexfinance.stocks import get_historical_data
import pandas as pd

with open('/Users/footballnerd12/apiKeys.json') as file:
    data = json.load(file)
    apiKey = data['alpha vantage']
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey={}&outputsize=full'.format(apiKey)

#data = requests.get(url)
#pprint(data.json())

df = pd.DataFrame({'b': list(range(100))})
df1 = pd.DataFrame({'a': list(range(100))})
df = df.join(df1)
df['a'] = df['a'].shift(-1)
#print(df)

with open('sp500results.json', 'r') as file:
    l = json.load(file)
    pprint(l)