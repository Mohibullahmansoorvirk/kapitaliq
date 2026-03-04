#Python library that lets you download stock market data from Yahoo Finance for free with no API key
import yfinance as yf 

class StockFetcher:
    def __init__(self,ticker):
        self.ticker = ticker
        self._data = None # no data

    def fetch(self, period="1mo"):
        stock = yf.Ticker(self.ticker)
        self._data = stock.history(period)
        if self._data.empty:
            raise ValueError("could not find any data")
        return self._data

    def latest_price(self):
        if self._data is None:  # nobody called fetch() yet
            self.fetch()        # call it automatically

        if self._data.empty:
            raise ValueError("could not find any data")
        return float(self._data["Close"].iloc[-1])

"""
data = StockFetcher("SAP.DE")
#data.fetch()        # uses "1mo" by default
data.fetch("5d")    # uses "5d"
print(f"{data.latest_price():.2f}")
"""