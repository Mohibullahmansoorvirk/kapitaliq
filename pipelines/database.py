from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from pipelines.base import Base

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

from pipelines.models import StockPrice
from pipelines.models import NewsArticle

#one time manual call to create tables directly from SQLAlchemy models.Later transfered to Alembic for migration tracking
if __name__ == "__main__":
    print(f"Tables known to Base: {Base.metadata.tables.keys()}")
    Base.metadata.create_all(engine)
