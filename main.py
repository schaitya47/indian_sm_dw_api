from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime
from sqlalchemy import and_

from database import get_db
import models, schemas

app = FastAPI()

@app.get("/db-test")
async def db_test(db: AsyncSession = Depends(get_db)):
    """Run a lightweight query to verify DB connectivity and dependency wiring."""
    result = await db.execute(text("SELECT 1"))
    """
    Sample URL: http://localhost:8000/db-test
    """
    value = result.scalar()
    return {"ok": True, "result": value}

@app.get("/stocks-list", response_model=List[str])
async def list_stocks(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """List stocks (read-only) with pagination."""
    """
    Sample URL: http://localhost:8000/stocks-list?limit=50&offset=0
    """
    result = await db.execute(select(models.DimStock.nk_symbol).limit(limit).offset(offset))
    stocks = result.scalars().all()
    return stocks

@app.get("/stock-info/{symbol}", response_model=schemas.StockOut)
async def get_stock_by_symbol(symbol: str, db: AsyncSession = Depends(get_db)):
    """Fetch a single stock by its symbol (read-only)."""
    """
    Sample URL: http://localhost:8000/stock-info/RELIANCE
    """
    result = await db.execute(select(models.DimStock).where(models.DimStock.nk_symbol == symbol))
    stock = result.scalars().first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

@app.get("/stock-ohlcv", response_model=schemas.OhlcvList)
async def get_ohlcv(
    symbol: str,
    source: str,
    start_date: int | None = None,  # YYYYMMDD integer
    end_date: int | None = None,
    limit: int = Query(1000, ge=1, le=10000),
    db: AsyncSession = Depends(get_db),
):
    """Return OHLCV for a symbol between date_key range.

    start_date and end_date are integers in YYYYMMDD format matching dim_date.date_key.
    """
    """
    Sample URL: http://localhost:8000/stock-ohlcv?symbol=RELIANCE&source=YFIN&start_date=20220101&end_date=20221231&limit=100
    """
    stock_key, source_key = await resolve_stock_and_source(db, symbol, source)

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
            "traded_date": datetime.strptime(str(r.date_key), '%Y%m%d'),
            "open_price": r.open_price,
            "high_price": r.high_price,
            "low_price": r.low_price,
            "close_price": r.close_price,
            "volume": r.volume,
        }
        for r in rows
    ]

    return {"symbol": symbol.strip(), "data": data}

@app.get("/stock-ohlcv/latest/{symbol}", response_model=schemas.OhlcvOut)
async def get_ohlcv_latest(symbol: str, db: AsyncSession = Depends(get_db)):
    stock_key = await resolve_stock(db, symbol)

    stmt = select(models.FactOhlcv).where(models.FactOhlcv.stock_key == stock_key).order_by(models.FactOhlcv.date_key.desc()).limit(1)
    result = await db.execute(stmt)
    r = result.scalars().first()
    if not r:
        raise HTTPException(status_code=404, detail="OHLCV not found")
    """
    Sample URL: http://localhost:8000/stock-ohlcv/latest/RELIANCE
    """
    return {
        "traded_date": datetime.strptime(str(r.date_key), '%Y%m%d'),
        "open_price": r.open_price,
        "high_price": r.high_price,
        "low_price": r.low_price,
        "close_price": r.close_price,
        "volume": r.volume,
    }


@app.get("/sources", response_model=List[schemas.SourceOut])
async def list_sources(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.DimSource))
    rows = result.scalars().all()
    """
    Sample URL: http://localhost:8000/sources
    """
    return rows


def _resolve_symbol_and_source(db: AsyncSession, symbol: str, source: str):
    """Helper to resolve stock_key and source_key; returns tuple(stock_key, source_key) or raises HTTPException."""
    # kept for backward compatibility but not used; use the async helpers below instead.
    return None


async def resolve_stock(db: AsyncSession, symbol: str) -> int:
    """Resolve a stock symbol to stock_key or raise HTTPException(404).

    Symbol matching is case-insensitive and strips whitespace.
    """
    res = await db.execute(select(models.DimStock.stock_key).where(models.DimStock.nk_symbol.ilike(symbol.strip())))
    stock_key = res.scalar_one_or_none()
    if not stock_key:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock_key


async def resolve_stock_and_source(db: AsyncSession, symbol: str, source: str) -> tuple[int, int]:
    """Resolve symbol -> stock_key and source -> source_key; raise 404 if either missing."""
    stock_key = await resolve_stock(db, symbol)
    res = await db.execute(select(models.DimSource.source_key).where(models.DimSource.source_name.ilike(source.strip())))
    source_key = res.scalar_one_or_none()
    if not source_key:
        raise HTTPException(status_code=404, detail="Source not found")
    return stock_key, source_key


@app.get("/stock-balance-sheet", response_model=List[schemas.BalanceSheetOut])
async def get_balance_sheet(
    symbol: str,
    source: str,
    start_date: int | None = None,
    end_date: int | None = None,
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    """
    Sample URL: http://localhost:8000/stock-balance-sheet?symbol=RELIANCE&source=YFIN&start_date=20220101&limit=10
    """
    stock_key, source_key = await resolve_stock_and_source(db, symbol, source)

    stmt = select(models.FactBalanceSheet).where(models.FactBalanceSheet.stock_key == stock_key, models.FactBalanceSheet.source_key == source_key)
    if start_date:
        stmt = stmt.where(models.FactBalanceSheet.date_key >= start_date)
    if end_date:
        stmt = stmt.where(models.FactBalanceSheet.date_key <= end_date)
    stmt = stmt.order_by(models.FactBalanceSheet.date_key.desc()).limit(limit)

    result = await db.execute(stmt)
    rows = result.scalars().all()

    def map_row(r: models.FactBalanceSheet):
        return {
            "date_key": r.date_key,
            "reporting_period": r.reporting_period,
            "cash_and_short_term_investments": r.bal_csti,
            "total_receivables": r.bal_trec,
            "total_inventory": r.bal_tinv,
            "other_current_assets": r.bal_oca,
            "total_current_assets": r.bal_tca,
            "net_loans": r.bal_netl,
            "net_property_plant_and_equipment": r.bal_nppe,
            "goodwill_and_intangibles": r.bal_gint,
            "long_term_investments": r.bal_lti,
            "other_assets": r.bal_otha,
            "total_assets": r.bal_tota,
            "accounts_payable": r.bal_accp,
            "total_deposits": r.bal_tdep,
            "other_current_liabilities": r.bal_ocl,
            "total_current_liabilities": r.bal_tcl,
            "total_long_term_debt": r.bal_tltd,
            "total_debt": r.bal_tdeb,
            "deferred_income_taxes": r.bal_dit,
            "minority_interest": r.bal_mint,
            "other_liabilities": r.bal_othl,
            "total_liabilities": r.bal_totl,
            "common_stock": r.bal_coms,
            "additional_paid_in_capital": r.bal_apic,
            "retained_earnings": r.bal_rtne,
            "other_equity": r.bal_oeq,
            "total_equity": r.bal_teq,
            "total_liabilities_and_shareholders_equity": r.bal_tlse,
            "total_common_shares_outstanding": r.bal_tcso,
            "total_preferred_shares_outstanding": r.bal_tpso,
            "net_current_assets": r.bal_nca,
            "current_assets": r.bal_ca,
            "net_current_liabilities": r.bal_ncl,
            "deferred_tax_assets": r.bal_dta,
        }

    return [map_row(r) for r in rows]


@app.get("/stock-cashflow", response_model=List[schemas.CashflowOut])
async def get_cashflow(
    symbol: str,
    source: str,
    start_date: int | None = None,
    end_date: int | None = None,
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    """
    Sample URL: http://localhost:8000/stock-cashflow?symbol=RELIANCE&source=YFIN&start_date=20220101&limit=10
    """
    stock_key, source_key = await resolve_stock_and_source(db, symbol, source)

    stmt = select(models.FactCashflow).where(models.FactCashflow.stock_key == stock_key, models.FactCashflow.source_key == source_key)
    if start_date:
        stmt = stmt.where(models.FactCashflow.date_key >= start_date)
    if end_date:
        stmt = stmt.where(models.FactCashflow.date_key <= end_date)
    stmt = stmt.order_by(models.FactCashflow.date_key.desc()).limit(limit)

    result = await db.execute(stmt)
    rows = result.scalars().all()

    def map_row(r: models.FactCashflow):
        return {
            "date_key": r.date_key,
            "reporting_period": r.reporting_period,
            "change_in_working_capital": r.caf_ciwc,
            "cash_flow_from_operating_activities": r.caf_cfoa,
            "capital_expenditures": r.caf_cexp,
            "cash_flow_from_investing_activities": r.caf_cfia,
            "total_cash_dividends_paid": r.caf_tcdp,
            "cash_flow_from_financing_activities": r.caf_cffa,
            "fee_or_expense_explanation": r.caf_fee,
            "net_change_in_cash_and_cash_equivalents": r.caf_ncic,
            "free_cash_flow": r.caf_fcf,
        }

    return [map_row(r) for r in rows]


@app.get("/stock-income", response_model=List[schemas.IncomeOut])
async def get_income(
    symbol: str,
    source: str,
    start_date: int | None = None,
    end_date: int | None = None,
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    """
    Sample URL: http://localhost:8000/stock-income?symbol=RELIANCE&source=YFIN&start_date=20220101&limit=10
    """
    stock_key, source_key = await resolve_stock_and_source(db, symbol, source)

    stmt = select(models.FactIncome).where(models.FactIncome.stock_key == stock_key, models.FactIncome.source_key == source_key)
    if start_date:
        stmt = stmt.where(models.FactIncome.date_key >= start_date)
    if end_date:
        stmt = stmt.where(models.FactIncome.date_key <= end_date)
    stmt = stmt.order_by(models.FactIncome.date_key.desc()).limit(limit)

    result = await db.execute(stmt)
    rows = result.scalars().all()

    def map_row(r: models.FactIncome):
        return {
            "date_key": r.date_key,
            "reporting_period": r.reporting_period,
            "total_revenue": r.q_inc_trev,
            "raw_material_costs": r.q_inc_raw,
            "profit_from_core": r.q_inc_pfc,
            "earnings_per_core": r.q_inc_epc,
            "selling_general_admin_expenses": r.q_inc_sga,
            "operating_expenses": r.q_inc_ope,
            "earnings_before_interest": r.q_inc_ebi,
            "depreciation": r.q_inc_dep,
            "profit_before_interest": r.q_inc_pbi,
            "income_from_other_investments": r.q_inc_ioi,
            "profit_before_tax": r.q_inc_pbt,
            "total_operating_income": r.q_inc_toi,
            "net_income": r.q_inc_ninc,
            "earnings_per_share": r.q_inc_eps,
            "dividends_per_share": r.q_inc_dps,
            "payout_ratio": r.q_inc_pyr,
        }

    return [map_row(r) for r in rows]


@app.get("/stock-key-ratios", response_model=List[schemas.KeyRatiosOut])
async def get_key_ratios(
    symbol: str,
    source: str,
    start_date: int | None = None,
    end_date: int | None = None,
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    """
    Sample URL: http://localhost:8000/stock-key-ratios?symbol=RELIANCE&source=YFIN&start_date=20220101&limit=10
    """
    stock_key, source_key = await resolve_stock_and_source(db, symbol, source)

    stmt = select(models.FactKeyRatios).where(models.FactKeyRatios.stock_key == stock_key, models.FactKeyRatios.source_key == source_key)
    if start_date:
        stmt = stmt.where(models.FactKeyRatios.date_key >= start_date)
    if end_date:
        stmt = stmt.where(models.FactKeyRatios.date_key <= end_date)
    stmt = stmt.order_by(models.FactKeyRatios.date_key.desc()).limit(limit)

    result = await db.execute(stmt)
    rows = result.scalars().all()

    def map_row(r: models.FactKeyRatios):
        return {
            "date_key": r.date_key,
            "risk": r.risk,
            "three_month_average_volume": r.letter_3mavgvol,
            "four_week_price_change_pct": r.letter_4wpct,
            "fifty_two_week_high": r.letter_52whigh,
            "fifty_two_week_low": r.letter_52wlow,
            "fifty_two_week_price_change_pct": r.letter_52wpct,
            "beta": r.beta,
            "book_value_per_share": r.bps,
            "dividend_yield": r.div_yield,
            "earnings_per_share": r.eps,
            "industry_dividend_yield": r.inddy,
            "industry_price_to_book": r.indpb,
            "industry_price_to_earnings": r.indpe,
            "market_cap": r.market_cap,
            "market_cap_rank": r.mrkt_cap_rank,
            "price_to_book": r.pb,
            "price_to_earnings": r.pe,
            "return_on_equity": r.roe,
            "number_of_shareholders": r.n_shareholders,
            "last_traded_price": r.last_price,
            "trailing_twelve_month_pe": r.ttm_pe,
            "market_cap_label": r.market_cap_label,
            "twelve_month_volume": r.letter_12mvol,
            "market_cap_float": r.mrkt_capf,
            "adjusted_pe_forward": r.apef,
            "price_to_book_redundant": r.pbr,
            "etf_liquidity": r.etf_liq,
            "etf_liquidity_label": r.etf_liq_label,
            "expense_ratio": r.expense_ratio,
            "tracking_error": r.track_err,
            "industry_expense_ratio": r.ind_expense_ratio,
            "industry_tracking_error": r.ind_track_err,
            "assets_under_management": r.asst_under_man,
        }

    return [map_row(r) for r in rows]


@app.get("/stock-recommendations", response_model=List[schemas.RecommendationsOut])
async def get_recommendations(
    symbol: str,
    source: str,
    start_date: int | None = None,
    end_date: int | None = None,
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    """
    Sample URL: http://localhost:8000/stock-recommendations?symbol=RELIANCE&source=YFIN&start_date=20220101&limit=10
    """
    stock_res = await db.execute(select(models.DimStock.stock_key).where(models.DimStock.nk_symbol.ilike(symbol.strip())))
    stock_key = stock_res.scalar_one_or_none()
    if not stock_key:
        raise HTTPException(status_code=404, detail="Stock not found")

    source_res = await db.execute(select(models.DimSource.source_key).where(models.DimSource.source_name.ilike(source.strip())))
    source_key = source_res.scalar_one_or_none()
    if not source_key:
        raise HTTPException(status_code=404, detail="Source not found")

    stmt = select(models.FactRecommendations).where(models.FactRecommendations.stock_key == stock_key, models.FactRecommendations.source_key == source_key)
    if start_date:
        stmt = stmt.where(models.FactRecommendations.date_key >= start_date)
    if end_date:
        stmt = stmt.where(models.FactRecommendations.date_key <= end_date)
    stmt = stmt.order_by(models.FactRecommendations.date_key.desc()).limit(limit)

    result = await db.execute(stmt)
    rows = result.scalars().all()

    def map_row(r: models.FactRecommendations):
        return {
            "date_key": r.date_key,
            "recommendation_period": r.recommendation_period,
            "strong_buy": r.strong_buy,
            "buy": r.buy,
            "hold": r.hold,
            "sell": r.sell,
            "strong_sell": r.strong_sell,
        }

    return [map_row(r) for r in rows]
