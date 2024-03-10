from pandera import Check, Column, DataFrameSchema, Index, MultiIndex, Timestamp

TradeConfirmations = DataFrameSchema(
    index=MultiIndex(
        [Index(Timestamp, name="date"), Index(str, name="broker")],
        unique=["date", "broker"],
        strict=True,
    ),
    columns={
        "sales": Column(float, Check.ge(0)),
        "purchases": Column(float, Check.ge(0)),
        "traded_volume": Column(float, Check.ge(0)),
        "clearing_fees": Column(float, Check.ge(0)),
        "trading_fees": Column(float, Check.ge(0)),
        "brokerage_fees": Column(float, Check.ge(0)),
        "income_tax": Column(float, Check.ge(0)),
        "costs": Column(float, Check.ge(0)),
        "amount": Column(float),
    },
    strict=True,
)

TradeConfirmationsPreCalc = TradeConfirmations.update_columns(
    {
        "traded_volume": {"nullable": True},
        "costs": {"nullable": True},
        "amount": {"nullable": True},
    }
)

TradeConfirmationsCalcResult = TradeConfirmations.select_columns(
    ["traded_volume", "costs", "amount"]
)

Trades = DataFrameSchema(
    index=MultiIndex([Index(Timestamp, name="date"), Index(str, name="broker")], strict=True),
    columns={
        "symbol": Column(str),
        "type": Column(str, Check.isin(["buy", "sell"])),
        "quantity": Column(float, Check.gt(0)),
        "price": Column(float, Check.ge(0)),
        "costs": Column(float, Check.ge(0)),
        "amount": Column(float),
    },
    strict=True,
)

TradesPreCalc = Trades.update_columns(
    {
        "costs": {"nullable": True},
        "amount": {"nullable": True},
    }
)

TradesCalcResult = Trades.select_columns(["costs", "amount"])

Rights = DataFrameSchema(
    index=MultiIndex([Index(Timestamp, name="date"), Index(str, name="broker")], strict=True),
    columns={
        "symbol": Column(str),
        "description": Column(str),
        "start": Column(Timestamp),
        "end": Column(Timestamp),
        "settlement": Column(Timestamp),
        "shares": Column(float, Check.gt(0)),
        "exercised": Column(float, Check.gt(0)),
        "price": Column(float, Check.gt(0)),
        "amount": Column(float, Check.gt(0)),
        "issue_date": Column(Timestamp, nullable=True),
    },
    strict=True,
)

RightsPreCalc = Rights.update_columns(
    {
        "amount": {"nullable": True},
    }
)

RightsCalcResult = Rights.select_columns(["amount"])

Splits = DataFrameSchema(
    index=MultiIndex(
        [Index(Timestamp, name="date"), Index(str, name="symbol")],
        unique=["date", "symbol"],
        strict=True,
    ),
    columns={
        "ratio": Column(str, Check.str_matches(r"^[\d,]+:[\d]+$")),
    },
    strict=True,
)

Mergers = DataFrameSchema(
    index=MultiIndex(
        [Index(Timestamp, name="date"), Index(str, name="symbol")],
        unique=["date", "symbol"],
        strict=True,
    ),
    columns={
        "acquirer": Column(str),
        "ratio": Column(str, Check.str_matches(r"^[\d,]+:[\d]+$")),
    },
    strict=True,
)

SpinOffs = DataFrameSchema(
    index=MultiIndex(
        [Index(Timestamp, name="date"), Index(str, name="symbol")],
        unique=["date", "symbol"],
        strict=True,
    ),
    columns={
        "new_company": Column(str),
        "ratio": Column(str, Check.str_matches(r"^[\d,]+:[\d]+$")),
        "cost_basis": Column(float, Check.gt(0)),
    },
    strict=True,
)

StockDividends = DataFrameSchema(
    index=MultiIndex(
        [Index(Timestamp, name="date"), Index(str, name="symbol")],
        unique=["date", "symbol"],
        strict=True,
    ),
    columns={
        "quantity": Column(float, Check.gt(0)),
        "cost": Column(float, Check.gt(0)),
    },
    strict=True,
)

PositionsCalcResult = DataFrameSchema(
    index=Index(int),
    columns={
        "symbol": Column(str, unique=True),
        "quantity": Column(float, Check.gt(0)),
        "cost": Column(float, Check.gt(0)),
        "cost_per_share": Column(float, Check.gt(0)),
    },
    strict=True,
)

PTAX = DataFrameSchema(
    index=Index(Timestamp, name="date", unique=True),
    columns={"buying_rate": Column(float, Check.gt(0)), "selling_rate": Column(float, Check.gt(0))},
    strict=True,
)

USTrades = DataFrameSchema(
    index=MultiIndex([Index(Timestamp, name="date")], strict=True),
    columns={
        "symbol": Column(str),
        "type": Column(str, Check.isin(["buy", "sell"])),
        "quantity": Column(float, Check.gt(0)),
        "price": Column(float, Check.ge(0)),
        "commission": Column(float, Check.ge(0)),
        "reg_fee": Column(float, Check.ge(0)),
        "costs": Column(float, Check.ge(0)),
        "amount": Column(float, Check.ge(0)),
        "ptax": Column(float, Check.gt(0)),
        "price_brl": Column(float, Check.gt(0)),
        "amount_brl": Column(float, Check.gt(0)),
    },
    strict=True,
)

USTradesPreCalc = USTrades.update_columns(
    {
        "costs": {"nullable": True, "coerce": True},
        "ptax": {"nullable": True},
        "price_brl": {"nullable": True},
        "amount_brl": {"nullable": True},
    }
)

USTradesCalcResult = USTrades.select_columns(["costs", "ptax", "price_brl", "amount_brl"])

USPositionsCalcResult = PositionsCalcResult.add_columns(
    {
        "cost_brl": Column(float, Check.gt(0)),
        "cost_per_share_brl": Column(float, Check.gt(0)),
    }
)

USDividends = DataFrameSchema(
    index=Index(Timestamp, name="date"),
    columns={
        "symbol": Column(str),
        "amount": Column(float, Check.gt(0)),
        "taxes": Column(float, Check.ge(0)),
        "total": Column(float, Check.ge(0)),
        "ptax": Column(float, Check.ge(0)),
        "amount_brl": Column(float, Check.ge(0)),
        "taxes_brl": Column(float, Check.ge(0)),
        "total_brl": Column(float, Check.ge(0)),
    },
    strict=True,
)

USDividendsPreCalc = USDividends.update_columns(
    {
        "total": {"nullable": True, "coerce": True},
        "ptax": {"nullable": True, "coerce": True},
        "amount_brl": {"nullable": True, "coerce": True},
        "taxes_brl": {"nullable": True, "coerce": True},
        "total_brl": {"nullable": True, "coerce": True},
    }
)

USDividendsCalcResult = USDividends.select_columns(
    ["total", "ptax", "amount_brl", "taxes_brl", "total_brl"]
)
