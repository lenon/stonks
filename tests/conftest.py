import pandas as pd
from pytest import fixture
from .helpers import fixture_path


@fixture
def confirmations_df():
    return pd.read_csv(
        fixture_path("confirmations.csv"),
        parse_dates=["date"],
        index_col=["date", "broker"],
    )


@fixture
def confirmations_costs_df():
    return pd.read_csv(
        fixture_path("confirmations-costs.csv"),
        parse_dates=["date"],
        index_col=["date", "broker"],
    )


@fixture
def confirmations_with_costs_df(confirmations_df, confirmations_costs_df):
    return confirmations_df.combine_first(confirmations_costs_df)


@fixture
def trades_df():
    return pd.read_csv(
        fixture_path("trades.csv"),
        parse_dates=["date"],
        index_col=["date", "broker"],
    )


@fixture
def trades_costs_df():
    return pd.read_csv(
        fixture_path("trades-costs.csv"),
        parse_dates=["date"],
        index_col=["date", "broker"],
    )


@fixture
def subscriptions_df():
    return pd.read_csv(
        fixture_path("subscriptions.csv"),
    )


@fixture
def subscriptions_amounts_df():
    return pd.read_csv(fixture_path("subscriptions-amounts.csv"))


@fixture
def splits():
    return pd.read_csv(
        fixture_path("splits.csv"),
        parse_dates=["date"],
    )


@fixture
def mergers():
    return pd.read_csv(
        fixture_path("mergers.csv"),
        parse_dates=["date"],
    )


@fixture
def spinoffs():
    return pd.read_csv(
        fixture_path("spinoffs.csv"),
        parse_dates=["date"],
    )


@fixture
def events():
    return pd.read_csv(
        fixture_path("events.csv"),
        parse_dates=["date", "start", "end", "settlement", "issue_date"],
    )
