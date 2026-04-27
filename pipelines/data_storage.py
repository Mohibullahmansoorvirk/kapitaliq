from pipelines.database import SessionLocal
from pipelines.models import StockPrice
from pipelines.stock_fetcher import StockFetcher
from pipelines.data_cleaner import DataCleaner
import logging
import pandas as pd
from sqlalchemy.dialects.postgresql import insert
logger = logging.getLogger(__name__)


def save_stock_data(ticker: str, cleaned_data: pd.DataFrame) -> None:

    db= SessionLocal()

    try:
        for i, row in enumerate(cleaned_data.itertuples(), 1):
            #stock=StockPrice(
            #    ticker = ticker,
            #    date = row.Index,
            #    open = row.Open,
            #    high = row.High,
            #    low = row.Low,
            #    close = row.Close,
            #    volume = row.Volume
            #                    )
            
            #db.add(stock)
            """
            Instead of normally making a python object in the logic above.
            We are using an SQL INSERT statement. this has more control and supports conflict handling
            To make sure there are no duplicate rows in the DB and if data fetched again the same day update the row with the latest data
            """
            ###UPSERT logic

            #Normal case: SQL Insert statement
            stmt = insert(StockPrice).values( #  all columns
                ticker=ticker,
                date=row.Index,
                open=row.Open,
                high=row.High,
                low=row.Low,
                close=row.Close,
                volume=row.Volume
                )

                #Conflict case: Insert the updated row if a conflict is found based on constraints defined in models.py
            upsert_stmt = stmt.on_conflict_do_update(
                index_elements=['ticker', 'date'],  # the constraints to watch
                set_={ #what to update on conflict -  everything except conflict keys -> ticker and date. only runs when a conflict detected
                    "open": row.Open,
                    "high": row.High,
                    "low": row.Low,
                    "close": row.Close,
                    "volume": row.Volume
                    }  
                )
            logger.info(f"saving row no {i}")
            db.execute(upsert_stmt)

        logger.info(f"total rows: {i} saved")
        db.commit() #commit only after all rows saved. partial data in case of failure is catastrophic for analysis

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save data: {e}")
        raise
        
    finally:
        db.close()

if __name__ == "__main__":
    tickers = [ #for project taken top 5 DAX stocks. Easily extendable to full DAX portfolio
    "SAP.DE","SIE.DE","DTE.DE","ALV.DE","AIR.DE"]
    for ticker in tickers:
        fetcher = StockFetcher(ticker)
        data = fetcher.fetch()
        cleaner = DataCleaner(data)
        clean_data = cleaner.clean()
        save_stock_data(ticker, clean_data)