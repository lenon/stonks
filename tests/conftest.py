from pandas import read_csv
from pytest import fixture
from .helpers import fixture_path


@fixture
def trade_confirmations_df():
    return read_csv(
        fixture_path("trade-confirmations.csv"),
        dtype={"sales": float, "purchases": float, "traded_volume": float},
        parse_dates=["date"],
        index_col=["date", "broker"],
    )


@fixture
def trade_confirmations_costs_df():
    return read_csv(
        fixture_path("trade-confirmations-costs.csv"),
        dtype={"traded_volume": float},
        parse_dates=["date"],
        index_col=["date", "broker"],
    )


@fixture
def trade_confirmations_with_costs_df(trade_confirmations_df, trade_confirmations_costs_df):
    return trade_confirmations_df.combine_first(trade_confirmations_costs_df)


@fixture
def trades_df():
    return read_csv(
        fixture_path("trades.csv"),
        parse_dates=["date"],
        index_col=["date", "broker"],
    )


@fixture
def trades_costs_df():
    return read_csv(
        fixture_path("trades-costs.csv"),
        parse_dates=["date"],
        index_col=["date", "broker"],
    )


@fixture
def trades_with_costs_df(trades_df, trades_costs_df):
    return trades_df.combine_first(trades_costs_df)


@fixture
def rights_df():
    return read_csv(
        fixture_path("rights.csv"),
        parse_dates=["date", "start", "end", "settlement", "issue_date"],
        index_col=["date", "broker"],
    )


@fixture
def rights_amounts_df():
    return read_csv(
        fixture_path("rights-amounts.csv"), parse_dates=["date"], index_col=["date", "broker"]
    )


@fixture
def rights_with_amounts_df(rights_df, rights_amounts_df):
    return rights_df.combine_first(rights_amounts_df)


@fixture
def splits_df():
    return read_csv(fixture_path("splits.csv"), parse_dates=["date"], index_col=["date", "symbol"])


@fixture
def mergers_df():
    return read_csv(fixture_path("mergers.csv"), parse_dates=["date"], index_col=["date", "symbol"])


@fixture
def spin_offs_df():
    return read_csv(
        fixture_path("spin-offs.csv"), parse_dates=["date"], index_col=["date", "symbol"]
    )


@fixture
def stock_dividends_df():
    return read_csv(
        fixture_path("stock-dividends.csv"), parse_dates=["date"], index_col=["date", "symbol"]
    )


@fixture
def events_df():
    return read_csv(
        fixture_path("events.csv"),
        parse_dates=["date", "start", "end", "settlement", "issue_date"],
    )


@fixture
def events_filtered_df():
    return read_csv(
        fixture_path("events-filtered.csv"),
        dtype={"acquirer": object, "new_company": object},
        parse_dates=["date", "start", "end", "settlement", "issue_date"],
    )


@fixture
def positions_df():
    return read_csv(fixture_path("positions.csv"))


@fixture
def ptax_df():
    return read_csv(fixture_path("ptax.csv"), parse_dates=["date"], index_col=["date"])


@fixture
def us_trades_df():
    return read_csv(fixture_path("us-trades.csv"), parse_dates=["date"], index_col=["date"])


@fixture
def us_trades_ptax_df():
    return read_csv(fixture_path("us-trades-ptax.csv"), parse_dates=["date"], index_col=["date"])


@fixture
def us_trades_with_ptax_df(us_trades_df, us_trades_ptax_df):
    return us_trades_df.combine_first(us_trades_ptax_df)


@fixture
def us_positions_df():
    return read_csv(fixture_path("us-positions.csv"))
