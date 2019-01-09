# Independent Financial Algorithm Project

Construction of a trading algorithm based on a to-be-determined machine learning algorithm.  The foundation of the algorithm rests on data selection based on correlation coefficients between various stocks.

## Correlations

The correlations for the stocks are calculated to determine how well a stock can 'predict' the value of another stock with a linear model in order to gain a rough approximation of the significance of the pair.  

### Day Shifts

Correlations are calculated for each day shift from 1 to n.  The day shift for a correlation indicates how far in advance the correlations are being calculated.  For example, a day shift of 2 for the correlation of stock B's with stock A will consist of the correlation of stock A's prices on day N with stock B's prices on day N-2.

Day shift correlations serve two purposes.  First, it allows for a reduction in insigificant data in the construction of the model, thus ratinalizing the inclusion of each feature--"Gargage in, garbage out".  Secondly, by shifting prices, additional significant features can be added to the model.  A stock sometimes does not significantly match another one week or month in advance, but rather several months in advance.  Such discoveries can add otherwise unused data to the model.

[Interactive visual demonstration of day shift correlations](https://www.linkedin.com/in/ethan-c-90870a11b/)

## Running the tests

Explain how to run the automated tests for this system

## Built With

* [Pandas](https://pandas.pydata.org/) - Used for data analysis
* [Investors Exchange (IEX)](https://rometools.github.io/rome/) - Financial data source
* [iexfinance](https://addisonlynch.github.io/iexfinance/stable/) - Python wrapper for IEX

## Authors

* **Ethan Carpenter**
* [GitHub](https://github.com/ethan9carpenter)
* [LinkedIn](https://www.linkedin.com/in/ethan-c-90870a11b/)
