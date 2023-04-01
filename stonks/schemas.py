from pandera import Check, Index, Column, Timestamp, MultiIndex, DataFrameSchema

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
        "net_amount": Column(float),
    },
    strict=True,
)

TradeConfirmationsPreCalc = TradeConfirmations.update_columns(
    {
        "traded_volume": {"nullable": True},
        "costs": {"nullable": True},
        "net_amount": {"nullable": True},
    }
)

TradeConfirmationsCalcResult = TradeConfirmations.select_columns(
    ["traded_volume", "costs", "net_amount"]
)

Trades = DataFrameSchema(
    index=MultiIndex([Index(Timestamp, name="date"), Index(str, name="broker")], strict=True),
    columns={
        "symbol": Column(str),
        "type": Column(str, Check.isin(["buy", "sell"])),
        "quantity": Column(float, Check.gt(0)),
        "price": Column(float, Check.ge(0)),
        "amount": Column(float, Check.ge(0)),
        "costs": Column(float, Check.ge(0)),
        "net_amount": Column(float),
    },
    strict=True,
)

TradesPreCalc = Trades.update_columns(
    {
        "amount": {"nullable": True},
        "costs": {"nullable": True},
        "net_amount": {"nullable": True},
    }
)

TradesCalcResult = Trades.select_columns(["amount", "costs", "net_amount"])

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
        "net_amount": Column(float, Check.gt(0)),
        "issue_date": Column(Timestamp, nullable=True),
    },
    strict=True,
)

RightsPreCalc = Rights.update_columns(
    {
        "net_amount": {"nullable": True},
    }
)

RightsCalcResult = Rights.select_columns(["net_amount"])

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
        "amount": Column(float, Check.ge(0)),
        "ptax": Column(float, Check.gt(0)),
        "price_brl": Column(float, Check.gt(0)),
        "amount_brl": Column(float, Check.gt(0)),
    },
    strict=True,
)

USTradesPreCalc = USTrades.update_columns(
    {
        "ptax": {"nullable": True, "coerce": True},
        "price_brl": {"nullable": True, "coerce": True},
        "amount_brl": {"nullable": True, "coerce": True},
    }
)

USTradesCalcResult = USTrades.select_columns(["ptax", "price_brl", "amount_brl"])
