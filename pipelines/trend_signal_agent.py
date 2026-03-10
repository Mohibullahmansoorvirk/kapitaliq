import pandas as pd
import logging
logger = logging.getLogger(__name__)
from pipelines.stock_fetcher import StockFetcher
from pipelines.data_cleaner import DataCleaner

class TrendSignalAgent:
    def __init__ (self, ticker: str) -> None:
        self.ticker = ticker
        logger.info(f"Ticker Name: {self.ticker}")

    def _calculate_ma20(self, cleaned_data: pd.DataFrame) -> float:
        logger.info(f"Calculating the MA20")
        print("MA20 is",float((cleaned_data["Close"].iloc[-20:]).mean()))
        return float((cleaned_data["Close"].iloc[-20:]).mean()) # last 20 days including today

    def _extract_todays_price(self, cleaned_data: pd.DataFrame) -> float:
        logger.info(f"Extracting todays price")
        print("Todays price is",float(cleaned_data["Close"].iloc[-1]))
        return float(cleaned_data["Close"].iloc[-1])

    def run(self, cleaned_data: pd.DataFrame) -> str:
        logger.info(f"Final decision")
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
    
    fetcher = StockFetcher("SAP.DE")
    data = fetcher.fetch()

    cleaner = DataCleaner(data)
    clean_data = cleaner.clean()

    agent= TrendSignalAgent("SAP.DE")
    agent_decision= agent.run(clean_data)
    print(agent_decision)