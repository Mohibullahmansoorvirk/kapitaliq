import pandas as pd
import logging
logger = logging.getLogger(__name__)


# Unlike DataCleaner where data is locked in at creation time (__init__) - which requires to create the object at every instance.
# TrendSignalAgent is a long-lived object. used later in other objects/loops. Hence, Data is passed into run() method
# so the same initial instance (once created) can analyze fresh data every day without recreation.

class TrendSignalAgent:
    def __init__ (self, ticker: str) -> None:
        self.ticker = ticker
        logger.info(f"Ticker Name: {self.ticker}")

    def _calculate_ma20(self, cleaned_data: pd.DataFrame) -> float:
        logger.info(f"Calculating the MA20")
        return float((cleaned_data["Close"].iloc[-20:]).mean()) # last 20 days including today

    def _extract_todays_price(self, cleaned_data: pd.DataFrame) -> float:
        logger.info(f"Extracting todays price")
        return float(cleaned_data["Close"].iloc[-1])

    def run(self, cleaned_data: pd.DataFrame) -> str:
        logger.info(f"Final decision")
        # BULLISH = price trending up -> Buy or Hold, BEARISH = price trending down -> Sell
        if self._calculate_ma20(cleaned_data) < self._extract_todays_price(cleaned_data):
            return f"BULLISH"
        else:
            return f"BEARISH"
        
    #__repr__ returns the printable representation of the object - useful for debugging
    def __repr__(self) -> str:
         return f"TrendSignalAgent(ticker='{self.ticker}')"
    

if __name__ == "__main__":
    #configuring logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    
    from pipelines.stock_fetcher import StockFetcher
    from pipelines.data_cleaner import DataCleaner

    fetcher = StockFetcher("SAP.DE")
    data = fetcher.fetch()

    cleaner = DataCleaner(data)
    clean_data = cleaner.clean()

    agent= TrendSignalAgent("SAP.DE")
    agent_decision= agent.run(clean_data)
    print(agent_decision)