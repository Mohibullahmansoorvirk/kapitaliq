from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from pipelines.base import Base

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

from pipelines.models import StockPrice

if __name__ == "__main__":
    print("Starting...")
    print("StockPrice imported")
    print(f"Tables known to Base: {Base.metadata.tables.keys()}")
    Base.metadata.create_all(engine)
    print("✅ Tables created successfully")