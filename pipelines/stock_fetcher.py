#Python library that lets you download stock market data from Yahoo Finance for free with no API key
import yfinance as yf
import logging
import pandas as pd
logger = logging.getLogger(__name__)

class StockFetcher:
    def __init__(self,ticker: str) -> None:
        self.ticker = ticker
        self._data = None # no data

    def fetch(self, period: str ="1mo") -> pd.DataFrame:
        logger.info(f"Fetching {self.ticker} data for {period}")
        stock = yf.Ticker(self.ticker)
        # try fetching data from yfinance - "circuit breaker"
        try:
            self._data = stock.history(period)
        except Exception as e:
             # log the failure and stop immediately and dont let system hang
            logger.error(f"yfinance failed for {self.ticker}: {e}")
             # raise stops execution and tells exactly what went wrong
            raise ConnectionError(f"Data source unavailable for {self.ticker}")
        # circuit breaker -ended
        
        if self._data.empty:
            logger.error(f"No data found for ticker: {self.ticker}")
            raise ValueError("could not find any data")
        
        rows=len(self._data)
        logger.info(f"Successfully fetched {rows} rows for {self.ticker}")
        return self._data

    def latest_price(self) -> float:
        if self._data is None:  # fetch() not called
            self.fetch()        # call it 

        if self._data.empty:
            raise ValueError("could not find any data")
        return float(self._data["Close"].iloc[-1])

if __name__ == "__main__":  # this only runs when this file is executed directly
    #configuring logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    fetcher = StockFetcher("SAP.DE")
    try:
        print(fetcher.fetch())
        print(fetcher.latest_price())
    except ValueError as e:
        print(f"Could not fetch data: {e}")
    