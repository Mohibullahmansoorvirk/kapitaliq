import pandas as pd
from dotenv import load_dotenv
import os
from newsapi import NewsApiClient
load_dotenv()
import logging
logger = logging.getLogger(__name__)

ticker_to_company = {
            "SAP.DE": "SAP",
            "SIE.DE": "Siemens",
            "DTE.DE": "Deutsche Telekom",
            "ALV.DE": "Allianz",
            "AIR.DE": "Airbus",
        }

class NewsFetcher:
    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def fetch(self) -> pd.DataFrame:

        NEWS_API_KEY = os.getenv("NEWS_API_KEY")

        #init - 
        news_api = NewsApiClient(api_key=NEWS_API_KEY)
        
        articles_list = []
        
        # try fetching data from NewsAPI call - "circuit breaker"
        try:
        #API end points
        # "q" arqument -> qoutes around the company name tells NewsAPI that this word is a must appear in the article
        #no date filter required because this always retreives top 10 latest news articles
            news_api_response = news_api.get_everything(q=f'"{ticker_to_company.get(self.ticker)}" stock', language="en", page_size=10) #page size is the number of articles
        
            articles = news_api_response['articles']

            
            #excluded the article content as its truncated to 200 characters for free version
            for article in articles:
                #for no descriptions articles
                if not article['description']:
                    continue
                articles_list.append({
                "Stock_Name": self.ticker,
                "Article Source": article['source']['name'],
                #"Title: {title}\nDescription: {description}" - format of the Content
                "Article_Content": f"Title: {article['title']}\nDescription: {article['description']}",
                "Article URL": article['url'],
                "Article Published Date": article['publishedAt'],
                        })
        except Exception as e:
             # log the failure and stop immediately and dont let system hang
            logger.error(f"NewsAPI failed for {self.ticker}: {e}")
             # raise stops execution and tells exactly what went wrong
            raise ConnectionError(f"news unavailable for {self.ticker}")
        # circuit breaker -ended

        return articles_list

if __name__ == "__main__":
    fetcher = NewsFetcher("SAP.DE")
    articles = fetcher.fetch()
    for article in articles:
        print(article)
        print("---")