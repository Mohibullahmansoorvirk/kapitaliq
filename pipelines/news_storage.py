from pipelines.models import NewsArticle
from pipelines.news_fetcher import NewsFetcher
from pipelines.chunker import Chunker
from pipelines.embedder import Embedder
from pipelines.database import SessionLocal
import logging
from sqlalchemy.dialects.postgresql import insert
logger = logging.getLogger(__name__)


#simple storage function
def save_news_articles(ticker: str) -> None:

    news_fetcher = NewsFetcher(ticker)
    chunker = Chunker()
    embedder = Embedder()
    db= SessionLocal()

    articles_list = news_fetcher.fetch()
    try:
        for article in articles_list:

            chunks = chunker.chunk(article["Article_Content"])
            embedded_vectors = embedder.embed(chunks)


            for i, (chunk, embedded_vector) in enumerate(zip(chunks, embedded_vectors)):
                """
                Read the UPSERT logic details in data_storage.py
                """
                
                #vector = NewsArticle(
                #    ticker = article["Stock_Name"],
                #    published_date = article["Article Published Date"],
                #    article_url = article["Article URL"],
                #    news_source = article["Article Source"],
                #    chunk_text = chunk,
                #    index_within_chunk = i + 1,
                #    embedding_vector = embedded_vector
                #)

                #db.add(vector)


                ###UPSERT logic
                stmt = insert(NewsArticle).values( #  all columns
                ticker=article["Stock_Name"],
                published_date = article["Article Published Date"],
                article_url = article["Article URL"],
                news_source = article["Article Source"],
                chunk_text = chunk,
                index_within_chunk = i + 1,
                embedding_vector = embedded_vector
                )

                #Conflict case: Insert the updated row if a conflict is found based on constraints defined in models.py
                upsert_stmt = stmt.on_conflict_do_update(
                    index_elements=['ticker', 'published_date', 'article_url' ],  # the constraints to watch
                    set_={ # what to update on conflict -  everything except conflict keys -> ticker and date. only runs when a conflict detected
                        "news_source": article["Article Source"],
                        "chunk_text": chunk,
                        "index_within_chunk": i + 1,
                        "embedding_vector": embedded_vector
                        }  
                )
                logger.info(f"saving row no {i}")
                db.execute(upsert_stmt)

            db.commit() #commit after every article so to have partial news data in case of mid failure

    except Exception as e:
            db.rollback()
            logger.error(f"Failed to save data: {e}")
            raise
            
    finally:
        db.close()


if __name__ == "__main__":
    tickers = [# for project taken top 5 DAX stocks. Easily extendable to full DAX portfolio
            "SAP.DE",
            "SIE.DE",
            "DTE.DE",
            "ALV.DE",
            "AIR.DE"]
    for ticker in tickers:
        save_news_articles(ticker)
    print("Data added in the table")