from sqlalchemy import Column, Integer, Text, TIMESTAMP, BigInteger, Float, SmallInteger, Boolean, Date
from database import Base

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

class DimSource(Base):
    __tablename__ = "dim_source"
    __table_args__ = {"schema": "stock_dw"}

    source_key = Column(Integer, primary_key=True, index=True)
    source_name = Column(Text, nullable=False, unique=True, index=True)
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
class FactBalanceSheet(Base):
    __tablename__ = "fact_balance_sheet"
    __table_args__ = {"schema": "stock_dw"}

    balance_sheet_key = Column(Integer, primary_key=True, index=True)
    date_key = Column(Integer, nullable=False, index=True)
    stock_key = Column(Integer, nullable=False, index=True)
    source_key = Column(Integer, nullable=False)
    reporting_period = Column(Text)

    bal_csti = Column(Float)
    bal_trec = Column(Float)
    bal_tinv = Column(Float)
    bal_oca = Column(Float)
    bal_tca = Column(Float)
    bal_netl = Column(Float)
    bal_nppe = Column(Float)
    bal_gint = Column(Float)
    bal_lti = Column(Float)
    bal_otha = Column(Float)
    bal_tota = Column(Float)

    bal_accp = Column(Float)
    bal_tdep = Column(Float)
    bal_ocl = Column(Float)
    bal_tcl = Column(Float)
    bal_tltd = Column(Float)
    bal_tdeb = Column(Float)
    bal_dit = Column(Float)
    bal_mint = Column(Float)
    bal_othl = Column(Float)
    bal_totl = Column(Float)

    bal_coms = Column(Float)
    bal_apic = Column(Float)
    bal_rtne = Column(Float)
    bal_oeq = Column(Float)
    bal_teq = Column(Float)
    bal_tlse = Column(Float)

    bal_tcso = Column(Float)
    bal_tpso = Column(Text)
    bal_nca = Column(Float)
    bal_ca = Column(Float)
    bal_ncl = Column(Float)
    bal_dta = Column(Float)

    load_ts = Column(TIMESTAMP)


class FactCashflow(Base):
    __tablename__ = "fact_cashflow"
    __table_args__ = {"schema": "stock_dw"}

    cashflow_key = Column(Integer, primary_key=True, index=True)
    date_key = Column(Integer, nullable=False, index=True)
    stock_key = Column(Integer, nullable=False, index=True)
    source_key = Column(Integer, nullable=False)
    reporting_period = Column(Text)

    caf_ciwc = Column(Float)
    caf_cfoa = Column(Float)
    caf_cexp = Column(Float)
    caf_cfia = Column(Float)
    caf_tcdp = Column(Float)
    caf_cffa = Column(Float)
    caf_fee = Column(Text)
    caf_ncic = Column(Float)
    caf_fcf = Column(Float)

    load_ts = Column(TIMESTAMP)


class FactIncome(Base):
    __tablename__ = "fact_income"
    __table_args__ = {"schema": "stock_dw"}

    income_key = Column(Integer, primary_key=True, index=True)
    date_key = Column(Integer, nullable=False, index=True)
    stock_key = Column(Integer, nullable=False, index=True)
    source_key = Column(Integer, nullable=False)
    reporting_period = Column(Text)

    q_inc_trev = Column(Float)
    q_inc_raw = Column(Text)
    q_inc_pfc = Column(Text)
    q_inc_epc = Column(Text)
    q_inc_sga = Column(Text)
    q_inc_ope = Column(Float)
    q_inc_ebi = Column(Float)
    q_inc_dep = Column(Float)
    q_inc_pbi = Column(Float)
    q_inc_ioi = Column(Float)
    q_inc_pbt = Column(Float)
    q_inc_toi = Column(Float)
    q_inc_ninc = Column(Float)
    q_inc_eps = Column(Float)
    q_inc_dps = Column(Text)
    q_inc_pyr = Column(Text)

    load_ts = Column(TIMESTAMP)


class FactKeyRatios(Base):
    __tablename__ = "fact_key_ratios"
    __table_args__ = {"schema": "stock_dw"}

    key_ratios_key = Column(Integer, primary_key=True, index=True)
    date_key = Column(Integer, nullable=False, index=True)
    stock_key = Column(Integer, nullable=False, index=True)
    source_key = Column(Integer, nullable=False)

    risk = Column(Float)
    letter_3mavgvol = Column(Float)
    letter_4wpct = Column(Float)
    letter_52whigh = Column(Float)
    letter_52wlow = Column(Float)
    letter_52wpct = Column(Float)
    beta = Column(Float)
    bps = Column(Float)
    div_yield = Column(Float)
    eps = Column(Float)
    inddy = Column(Float)
    indpb = Column(Float)
    indpe = Column(Float)
    market_cap = Column(Float)
    mrkt_cap_rank = Column(SmallInteger)
    pb = Column(Float)
    pe = Column(Float)
    roe = Column(Float)
    n_shareholders = Column(Integer)
    last_price = Column(Float)
    ttm_pe = Column(Float)
    market_cap_label = Column(Text)
    letter_12mvol = Column(Float)
    mrkt_capf = Column(Float)
    apef = Column(Float)
    pbr = Column(Float)
    etf_liq = Column(Float)
    etf_liq_label = Column(Text)
    expense_ratio = Column(Text)
    track_err = Column(Text)
    ind_expense_ratio = Column(Text)
    ind_track_err = Column(Text)
    asst_under_man = Column(Text)

    load_ts = Column(TIMESTAMP)


class FactRecommendations(Base):
    __tablename__ = "fact_recommendations"
    __table_args__ = {"schema": "stock_dw"}

    recommendation_key = Column(Integer, primary_key=True, index=True)
    date_key = Column(Integer, nullable=False, index=True)
    stock_key = Column(Integer, nullable=False, index=True)
    source_key = Column(Integer, nullable=False)
    recommendation_period = Column(TIMESTAMP)

    strong_buy = Column(SmallInteger)
    buy = Column(SmallInteger)
    hold = Column(SmallInteger)
    sell = Column(SmallInteger)
    strong_sell = Column(SmallInteger)

    load_ts = Column(TIMESTAMP)