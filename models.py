from sqlalchemy import Column, Integer, Text, TIMESTAMP, BigInteger, Float
from .database import Base

class DimStock(Base):
    __tablename__ = "dim_stock"
    __table_args__ = {"schema": "stock_dw"}

    stock_key = Column(Integer, primary_key=True, index=True)
    nk_symbol = Column(Text, nullable=False, unique=True, index=True)
    company_name = Column(Text)
    industry = Column(Text)
    series = Column(Text)
    isin_code = Column(Text)
    yfin_symbol = Column(Text)
    load_ts = Column(TIMESTAMP)

class FactOhlcv(Base):
    __tablename__ = "fact_ohlcv"
    __table_args__ = {"schema": "stock_dw"}

    ohlcv_key = Column(Integer, primary_key=True, index=True)
    date_key = Column(BigInteger, nullable=False, index=True)
    stock_key = Column(BigInteger, nullable=False, index=True)
    source_key = Column(BigInteger, nullable=False)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(BigInteger)
    dividends = Column(Float)
    stock_splits = Column(Float)
    load_ts = Column(TIMESTAMP)