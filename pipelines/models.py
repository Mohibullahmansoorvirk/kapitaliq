"""
models.py serves as the base of defining models/tables for the database
"""
from sqlalchemy import Column, Integer, String, Float, BigInteger, Date
from pgvector.sqlalchemy import Vector
from pipelines.base import Base 


class StockPrice(Base):
    __tablename__ = "stock_prices"
    
    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float, nullable=False)
    volume = Column(BigInteger)
    sentiment_score = Column(Float, nullable=True)

    #__repr__ returns the printable representation of the object  - useful for debugging
    def __repr__(self) -> str:
         return f"StockPrice(ticker='{self.ticker}', close={self.close})"


class NewsArticle(Base):
    __tablename__ = "news_articles"
    
    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    published_date = Column(Date, nullable=False)
    article_url = Column(String, nullable=False)
    news_source = Column(String, nullable=False)
    chunk_text = Column(String, nullable=False)
    index_within_chunk = Column(Integer, nullable=False)
    embedding_vector = Column(Vector(768), nullable=True) # vector for similarity search. 768 dimensions for embedding model -> nomic-embed-text.
    #Nullable true above to have flexibility of having chunks but no vectors

    #__repr__ returns the printable representation of the object  - useful for debugging
    def __repr__(self) -> str:
         return f"NewsArticle(ticker='{self.ticker}', embedding_vector={self.embedding_vector})"