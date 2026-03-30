from apscheduler.schedulers.background import BackgroundScheduler #runs in a background
from pipelines.stock_fetcher import StockFetcher
from pipelines.data_cleaner import DataCleaner
from pipelines.data_storage import save_stock_data
from pipelines.news_storage import save_news_articles
from sqlalchemy import delete
from datetime import date, timedelta
from pipelines.models import StockPrice, NewsArticle
from pipelines.database import SessionLocal
import logging
logging.basicConfig(level=logging.WARNING) #all logs regarding Warnings
logging.getLogger(__name__).setLevel(logging.INFO) 
logger = logging.getLogger(__name__)


tickers = [ # for project taken top 5 DAX stocks. Easily extendable to full DAX portfolio
    "SAP.DE","SIE.DE","DTE.DE","ALV.DE","AIR.DE"]

def refresh_stock_data(ticker):

    fetcher = StockFetcher(ticker)
    data = fetcher.fetch()
    cleaner = DataCleaner(data)
    clean_data = cleaner.clean()
    save_stock_data(ticker, clean_data)

def refresh_news_data(ticker):

    save_news_articles(ticker)
    

def run_daily_refresh():

    for ticker in tickers:
        try:
            logger.info(f"Starting stock data refresh for {ticker}")
            refresh_stock_data(ticker)
            logger.info(f"Stock data refresh complete for {ticker}")
        except Exception as e:
            logger.error(f"Stock Data refresh failed on {ticker}: {e}")
            pass # pass and not continue so it doesnt skip the next try-except block

        try:
            logger.info(f"Starting news data refresh for {ticker}")
            refresh_news_data(ticker)
            logger.info(f"news data refresh complete for {ticker}")
        except Exception as e:
            logger.error(f"News Data refresh failed on {ticker}: {e}")
            pass #pass and continue behave same

def cleanup_old_data():
     
    db= SessionLocal()

    try:
        # delete rows from the model -> stock_prices, older than 30 days
        db.execute(delete(StockPrice).where(StockPrice.date < date.today() - timedelta(days=30)))
        # delete rows from the model -> news_articles, older than 30 days
        db.execute(delete(NewsArticle).where(NewsArticle.published_date < date.today() - timedelta(days=30)))

        db.commit()
    
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete rows data: {e}")
        raise
        
    finally:
        db.close()

def schedule_daily_refresh():
    scheduler = BackgroundScheduler()
    #cron lets you schedule and trigger the job at the specific time of the day
    scheduler.add_job(run_daily_refresh, 'cron', hour=9, minute=30) #hour = 9am , minute = 30 - this means every day at 9:30am - DAX opens at 9am
    scheduler.add_job(cleanup_old_data, 'cron', hour=9, minute=0) # running cleanup func at 9am , 30 minutes before the refresh of data
    scheduler.start()

if __name__ == "__main__":

    schedule_daily_refresh()
    import time
    while True: # keeps the background-scheduler alives in the background
        time.sleep(60)