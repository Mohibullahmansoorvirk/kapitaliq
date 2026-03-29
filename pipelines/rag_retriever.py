from pipelines.models import NewsArticle
from sqlalchemy import select
from pipelines.embedder import Embedder
from pipelines.database import SessionLocal
from datetime import date, timedelta

def retrieve_relevant_chunks(user_query: str, ticker: str, k: int = 3) -> list[str]:
    embedder = Embedder()
    embedded_vector_query = embedder.model.embed_query(user_query)
    db= SessionLocal()
    result = db.execute(
    select(NewsArticle.chunk_text)
    .where(
        NewsArticle.ticker == ticker,
        NewsArticle.published_date >= date.today() - timedelta(days=7) #filtering to only retreive chunks that are for the last 7 days (updated news only)
        )
    .order_by(NewsArticle.embedding_vector.cosine_distance(embedded_vector_query))
    .limit(k)
        )
    
    rows = result.fetchall()
    return [row[0] for row in rows]


if __name__ == "__main__":
    chunks = retrieve_relevant_chunks("SAP earnings performance", "SAP.DE", k=3)
    for chunk in chunks:
        print(chunk)
