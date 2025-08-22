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
    traded_date: datetime
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


class BalanceSheetOut(BaseModel):
    date_key: int
    reporting_period: Optional[str]
    cash_and_short_term_investments: Optional[float]
    total_receivables: Optional[float]
    total_inventory: Optional[float]
    other_current_assets: Optional[float]
    total_current_assets: Optional[float]
    net_loans: Optional[float]
    net_property_plant_and_equipment: Optional[float]
    goodwill_and_intangibles: Optional[float]
    long_term_investments: Optional[float]
    other_assets: Optional[float]
    total_assets: Optional[float]

    accounts_payable: Optional[float]
    total_deposits: Optional[float]
    other_current_liabilities: Optional[float]
    total_current_liabilities: Optional[float]
    total_long_term_debt: Optional[float]
    total_debt: Optional[float]
    deferred_income_taxes: Optional[float]
    minority_interest: Optional[float]
    other_liabilities: Optional[float]
    total_liabilities: Optional[float]

    common_stock: Optional[float]
    additional_paid_in_capital: Optional[float]
    retained_earnings: Optional[float]
    other_equity: Optional[float]
    total_equity: Optional[float]
    total_liabilities_and_shareholders_equity: Optional[float]

    total_common_shares_outstanding: Optional[float]
    total_preferred_shares_outstanding: Optional[str]
    net_current_assets: Optional[float]
    current_assets: Optional[float]
    net_current_liabilities: Optional[float]
    deferred_tax_assets: Optional[float]

    class Config:
        orm_mode = True


class CashflowOut(BaseModel):
    date_key: int
    reporting_period: Optional[str]
    change_in_working_capital: Optional[float]
    cash_flow_from_operating_activities: Optional[float]
    capital_expenditures: Optional[float]
    cash_flow_from_investing_activities: Optional[float]
    total_cash_dividends_paid: Optional[float]
    cash_flow_from_financing_activities: Optional[float]
    fee_or_expense_explanation: Optional[str]
    net_change_in_cash_and_cash_equivalents: Optional[float]
    free_cash_flow: Optional[float]

    class Config:
        orm_mode = True


class IncomeOut(BaseModel):
    date_key: int
    reporting_period: Optional[str]
    total_revenue: Optional[float]
    raw_material_costs: Optional[str]
    profit_from_core: Optional[str]
    earnings_per_core: Optional[str]
    selling_general_admin_expenses: Optional[str]
    operating_expenses: Optional[float]
    earnings_before_interest: Optional[float]
    depreciation: Optional[float]
    profit_before_interest: Optional[float]
    income_from_other_investments: Optional[float]
    profit_before_tax: Optional[float]
    total_operating_income: Optional[float]
    net_income: Optional[float]
    earnings_per_share: Optional[float]
    dividends_per_share: Optional[str]
    payout_ratio: Optional[str]

    class Config:
        orm_mode = True


class KeyRatiosOut(BaseModel):
    date_key: int
    risk: Optional[float]
    three_month_average_volume: Optional[float]
    four_week_price_change_pct: Optional[float]
    fifty_two_week_high: Optional[float]
    fifty_two_week_low: Optional[float]
    fifty_two_week_price_change_pct: Optional[float]
    beta: Optional[float]
    book_value_per_share: Optional[float]
    dividend_yield: Optional[float]
    earnings_per_share: Optional[float]
    industry_dividend_yield: Optional[float]
    industry_price_to_book: Optional[float]
    industry_price_to_earnings: Optional[float]
    market_cap: Optional[float]
    market_cap_rank: Optional[int]
    price_to_book: Optional[float]
    price_to_earnings: Optional[float]
    return_on_equity: Optional[float]
    number_of_shareholders: Optional[int]
    last_traded_price: Optional[float]
    trailing_twelve_month_pe: Optional[float]
    market_cap_label: Optional[str]
    twelve_month_volume: Optional[float]
    market_cap_float: Optional[float]
    adjusted_pe_forward: Optional[float]
    price_to_book_redundant: Optional[float]
    etf_liquidity: Optional[float]
    etf_liquidity_label: Optional[str]
    expense_ratio: Optional[str]
    tracking_error: Optional[str]
    industry_expense_ratio: Optional[str]
    industry_tracking_error: Optional[str]
    assets_under_management: Optional[str]

    class Config:
        orm_mode = True


class RecommendationsOut(BaseModel):
    date_key: int
    recommendation_period: Optional[datetime]
    strong_buy: Optional[int]
    buy: Optional[int]
    hold: Optional[int]
    sell: Optional[int]
    strong_sell: Optional[int]

    class Config:
        orm_mode = True


class SourceOut(BaseModel):
    source_key: int
    source_name: str

    class Config:
        orm_mode = True
