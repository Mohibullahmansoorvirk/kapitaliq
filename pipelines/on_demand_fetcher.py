"""
On demand stocks data & news fetcher
This is triggered depending on user queries to fetch and store the latest stock and news data for a given ticker
Unlike the scheduler which runs daily at 9:30am, this runs instantly when a user needs fresh data
"""

from pipelines.scheduler import refresh_news_data, refresh_stock_data
import pandas as pd


def fetch_on_demand(ticker: str) -> None:

    refresh_stock_data(ticker)
    refresh_news_data(ticker)

