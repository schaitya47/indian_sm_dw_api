from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class StockBase(BaseModel):
    nk_symbol: str
    company_name: Optional[str] = None
    industry: Optional[str] = None
    isin_code: Optional[str] = None
    yfin_symbol: Optional[str] = None


class StockOut(StockBase):
    stock_key: int


    class Config:
        orm_mode = True

class OhlcvOut(BaseModel):
    date_key: datetime
    open_price: Optional[float]
    high_price: Optional[float]
    low_price: Optional[float]
    close_price: Optional[float]
    volume: Optional[int]

    class Config:
        orm_mode = True

class OhlcvList(BaseModel):
    symbol: str
    data: List[OhlcvOut]
