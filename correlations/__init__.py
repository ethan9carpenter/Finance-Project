from correlations.tickers import TickerList
from correlations.buildCorrelations import getCorrelations, performAnalysis, formatFP
from correlations import results


def printMessage(message):
    """
    Prints a message to a console to clearly display a message to the user
    """
    print(20*'-', message, 20*'-')

