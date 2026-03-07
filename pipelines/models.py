from sqlalchemy import Column, Integer, String, Float, BigInteger, Date
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

    #__repr__ returns the printable representation of the object
    def __repr__(self):
         return f"StockPrice(ticker='{self.ticker}', close={self.close})"