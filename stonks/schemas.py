from pandera import Check, Index, Column, Timestamp, MultiIndex, DataFrameSchema

TradeConfirmations = DataFrameSchema(
    index=MultiIndex(
        [Index(Timestamp, name="date"), Index(str, name="broker")], unique=["date", "broker"]
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

TradeConfirmationsWithNullable = TradeConfirmations.update_columns(
    {
        "traded_volume": {"nullable": True},
        "costs": {"nullable": True},
        "net_amount": {"nullable": True},
    }
)

Trades = DataFrameSchema(
    index=MultiIndex([Index(Timestamp, name="date"), Index(str, name="broker")]),
    columns={
        "symbol": Column(str),
        "type": Column(str, Check.isin(["buy", "sell"])),
        "quantity": Column(float, Check.gt(0)),
        "price": Column(float, Check.ge(0)),
        "amount": Column(float, Check.ge(0), nullable=True),
        "costs": Column(float, Check.ge(0), nullable=True),
        "net_amount": Column(float, nullable=True),
    },
    strict=True,
)

Rights = DataFrameSchema(
    index=MultiIndex([Index(Timestamp, name="date"), Index(str, name="broker")]),
    columns={
        "symbol": Column(str),
        "description": Column(str),
        "start": Column(Timestamp),
        "end": Column(Timestamp),
        "settlement": Column(Timestamp),
        "shares": Column(float, Check.gt(0)),
        "exercised": Column(float, Check.gt(0)),
        "price": Column(float, Check.gt(0)),
        "net_amount": Column(float, Check.gt(0), nullable=True),
        "issue_date": Column(Timestamp, nullable=True),
    },
    strict=True,
)

Splits = DataFrameSchema(
    index=MultiIndex([Index(Timestamp, name="date"), Index(str, name="symbol")]),
    columns={
        "ratio": Column(str, Check.str_matches(r"^[\d,]+:[\d]+$")),
    },
    strict=True,
)

Mergers = DataFrameSchema(
    index=MultiIndex([Index(Timestamp, name="date"), Index(str, name="symbol")]),
    columns={
        "acquirer": Column(str),
        "ratio": Column(str, Check.str_matches(r"^[\d,]+:[\d]+$")),
    },
    strict=True,
)

SpinOffs = DataFrameSchema(
    index=MultiIndex([Index(Timestamp, name="date"), Index(str, name="symbol")]),
    columns={
        "new_company": Column(str),
        "ratio": Column(str, Check.str_matches(r"^[\d,]+:[\d]+$")),
        "cost_basis": Column(float, Check.gt(0)),
    },
    strict=True,
)

StockDividends = DataFrameSchema(
    index=MultiIndex([Index(Timestamp, name="date"), Index(str, name="symbol")]),
    columns={
        "quantity": Column(float, Check.gt(0)),
        "cost": Column(float, Check.gt(0)),
    },
    strict=True,
)
