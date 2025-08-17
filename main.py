from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime
from sqlalchemy import and_

from .database import get_db
from . import models, schemas

app = FastAPI()

@app.get("/db-test")
async def db_test(db: AsyncSession = Depends(get_db)):
    """Run a lightweight query to verify DB connectivity and dependency wiring."""
    result = await db.execute(text("SELECT 1"))
    value = result.scalar()
    return {"ok": True, "result": value}

@app.get("/stocks-list", response_model=List[str])
async def list_stocks(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """List stocks (read-only) with pagination."""
    result = await db.execute(select(models.DimStock.nk_symbol).limit(limit).offset(offset))
    stocks = result.scalars().all()
    return stocks

@app.get("/stock-info/{symbol}", response_model=schemas.StockOut)
async def get_stock_by_symbol(symbol: str, db: AsyncSession = Depends(get_db)):
    """Fetch a single stock by its symbol (read-only)."""
    result = await db.execute(select(models.DimStock).where(models.DimStock.nk_symbol == symbol))
    stock = result.scalars().first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

@app.get("/stock-ohlcv", response_model=schemas.OhlcvList)
async def get_ohlcv(
    symbol: str,
    start_date: int | None = None,  # YYYYMMDD integer
    end_date: int | None = None,
    limit: int = Query(1000, ge=1, le=10000),
    db: AsyncSession = Depends(get_db),
):
    """Return OHLCV for a symbol between date_key range.

    start_date and end_date are integers in YYYYMMDD format matching dim_date.date_key.
    """
    # resolve symbol -> stock_key
    res = await db.execute(select(models.DimStock.stock_key).where(models.DimStock.nk_symbol.ilike(symbol.strip())))
    stock_key = res.scalar_one_or_none()
    if not stock_key:
        raise HTTPException(status_code=404, detail="Stock not found")

    stmt = select(models.FactOhlcv).where(models.FactOhlcv.stock_key == stock_key)
    if start_date:
        stmt = stmt.where(models.FactOhlcv.date_key >= start_date)
    if end_date:
        stmt = stmt.where(models.FactOhlcv.date_key <= end_date)
    stmt = stmt.order_by(models.FactOhlcv.date_key).limit(limit)

    result = await db.execute(stmt)
    rows = result.scalars().all()

    # Convert to list of OhlcvOut dicts
    data = [
        {
            "date_key": datetime.strptime(str(r.date_key), '%Y%m%d'),
            "open_price": r.open_price,
            "high_price": r.high_price,
            "low_price": r.low_price,
            "close_price": r.close_price,
            "volume": r.volume,
        }
        for r in rows
    ]

    return {"symbol": symbol.strip(), "data": data}

@app.get("/ohlcv/latest", response_model=schemas.OhlcvOut)
async def get_ohlcv_latest(symbol: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(models.DimStock.stock_key).where(models.DimStock.nk_symbol.ilike(symbol.strip())))
    stock_key = res.scalar_one_or_none()
    if not stock_key:
        raise HTTPException(status_code=404, detail="Stock not found")

    stmt = select(models.FactOhlcv).where(models.FactOhlcv.stock_key == stock_key).order_by(models.FactOhlcv.date_key.desc()).limit(1)
    result = await db.execute(stmt)
    r = result.scalars().first()
    if not r:
        raise HTTPException(status_code=404, detail="OHLCV not found")
    return {
        "date_key": int(r.date_key),
        "open_price": r.open_price,
        "high_price": r.high_price,
        "low_price": r.low_price,
        "close_price": r.close_price,
        "volume": r.volume,
    }
