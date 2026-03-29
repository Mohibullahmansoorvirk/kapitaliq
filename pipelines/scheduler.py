from apscheduler.schedulers.background import BackgroundScheduler #runs in a background
from pipelines.stock_fetcher import StockFetcher
from pipelines.data_cleaner import DataCleaner
from pipelines.data_storage import save_stock_data
from pipelines.news_storage import save_news_articles
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



def schedule_daily_refresh():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_daily_refresh, 'cron', hour=9, minute=30) #hour = 9am , minute = 30 - this means every day at 9:30am - DAX opens at 9am
    scheduler.start()

if __name__ == "__main__":

    schedule_daily_refresh()
    import time
    while True: # keeps the background-scheduler alives in the background
        time.sleep(60)