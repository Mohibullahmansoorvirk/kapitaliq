from pipelines.models import NewsArticle
from pipelines.news_fetcher import NewsFetcher
from pipelines.chunker import Chunker
from pipelines.embedder import Embedder
from pipelines.database import SessionLocal
import logging
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
                vector = NewsArticle(
                    ticker = article["Stock_Name"],
                    published_date = article["Article Published Date"],
                    article_url = article["Article URL"],
                    news_source = article["Article Source"],
                    chunk_text = chunk,
                    index_within_chunk = i + 1,
                    embedding_vector = embedded_vector
                )

                db.add(vector)

            db.commit()

    except Exception as e:
            db.rollback()
            logger.error(f"Failed to save data: {e}")
            raise
            
    finally:
        db.close()


if __name__ == "__main__":
    save_news_articles("SAP.DE")
    print("Data added in the table")