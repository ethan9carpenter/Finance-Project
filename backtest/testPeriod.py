import pandas as pd

def test(actualData, buySell):
    df = pd.DataFrame(actualData)
    df['buy'] = pd.Series(buySell, index=df.index)
    