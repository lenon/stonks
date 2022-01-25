from pytest import fixture
import pandas as pd
from pathlib import Path


def fixture_path(fixture):
    return Path(__file__).parent.joinpath("fixtures", fixture).resolve()


@fixture
def confirmations():
    return pd.read_csv(
        fixture_path("confirmations.csv"),
        parse_dates=["date"],
        index_col=["date", "broker"],
    )


@fixture
def confirmations_with_volume_and_costs():
    return pd.read_csv(
        fixture_path("confirmations-with-costs.csv"),
        parse_dates=["date"],
        index_col=["date", "broker"],
    )


@fixture
def trades():
    return pd.read_csv(
        fixture_path("trades.csv"),
        parse_dates=["date"],
        index_col=["date", "broker"],
    )


@fixture
def trades_with_costs():
    return pd.read_csv(
        fixture_path("trades-with-costs.csv"),
        parse_dates=["date"],
        index_col=["date", "broker"],
    )


@fixture
def subscriptions():
    return pd.read_csv(
        fixture_path("subscriptions.csv"),
        parse_dates=["date", "start", "end", "settlement", "issue_date"],
    )


@fixture
def subscriptions_with_net_amount():
    return pd.read_csv(
        fixture_path("subscriptions-with-net-amount.csv"),
        parse_dates=["date", "start", "end", "settlement", "issue_date"],
    )
