from pandera import Check, Index, Column, Timestamp, MultiIndex, DataFrameSchema

TradeConfirmations = DataFrameSchema(
    columns={
        "sells": Column(float, Check.ge(0)),
        "buys": Column(float, Check.ge(0)),
        "volume": Column(float, Check.ge(0)),
        "clearing_fees": Column(float, Check.ge(0)),
        "trading_fees": Column(float, Check.ge(0)),
        "brokerage_fees": Column(float, Check.ge(0)),
        "income_tax": Column(float, Check.ge(0)),
        "costs": Column(float, Check.ge(0)),
        "net_amount": Column(float),
    },
    index=MultiIndex([Index(Timestamp, name="date"), Index(str, name="broker")]),
    strict=True,
)

Trades = DataFrameSchema(
    columns={
        "symbol": Column(str),
        "type": Column(str, Check.isin(["buy", "sell"])),
        "quantity": Column(float, Check.gt(0)),
        "price": Column(float, Check.ge(0)),
        "amount": Column(float, Check.ge(0)),
        "costs": Column(float, Check.ge(0)),
        "net_amount": Column(float),
    },
    index=MultiIndex([Index(Timestamp, name="date"), Index(str, name="broker")]),
    strict=True,
)

Rights = DataFrameSchema(
    columns={
        "date": Column(Timestamp),
        "broker": Column(str),
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

Splits = DataFrameSchema(
    columns={
        "date": Column(Timestamp),
        "symbol": Column(str),
        "ratio": Column(str, Check.str_matches(r"^[\d,]+:[\d]+$")),
    },
    strict=True,
)

Mergers = DataFrameSchema(
    columns={
        "date": Column(Timestamp),
        "symbol": Column(str),
        "acquirer": Column(str),
        "ratio": Column(str, Check.str_matches(r"^[\d,]+:[\d]+$")),
    },
    strict=True,
)

SpinOffs = DataFrameSchema(
    columns={
        "date": Column(Timestamp),
        "symbol": Column(str),
        "new_company": Column(str),
        "ratio": Column(str, Check.str_matches(r"^[\d,]+:[\d]+$")),
        "cost_basis": Column(float, Check.gt(0)),
    },
    strict=True,
)

StockDividends = DataFrameSchema(
    columns={
        "date": Column(Timestamp),
        "symbol": Column(str),
        "quantity": Column(float, Check.gt(0)),
        "cost": Column(float, Check.gt(0)),
    },
    strict=True,
)
