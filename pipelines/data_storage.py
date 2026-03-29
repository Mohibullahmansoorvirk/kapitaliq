from pipelines.database import SessionLocal
from pipelines.models import StockPrice
import logging
import pandas as pd
logger = logging.getLogger(__name__)


def save_stock_data(ticker: str, cleaned_data: pd.DataFrame) -> None:

    db= SessionLocal()

    try:
        for i, row in enumerate(cleaned_data.itertuples(), 1):
            stock=StockPrice(
                ticker = ticker,
                date = row.Index,
                open = row.Open,
                high = row.High,
                low = row.Low,
                close = row.Close,
                volume = row.Volume
                                )
            logger.info(f"saving row no {i}")
            db.add(stock)

        logger.info(f"total rows: {i} saved")
        db.commit()

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save data: {e}")
        raise
        
    finally:
        db.close()

