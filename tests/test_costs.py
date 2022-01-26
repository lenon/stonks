import pandas as pd
from pytest import fixture
from stonks.costs import (
    sum_confirmations_costs,
    calc_trades_costs,
    calc_subscriptions_net_amounts,
)
from .helpers import fixture_path


@fixture
def confirmations():
    return pd.read_csv(
        fixture_path("confirmations.csv"),
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
def subscriptions():
    return pd.read_csv(
        fixture_path("subscriptions.csv"),
        parse_dates=["date", "start", "end", "settlement", "issue_date"],
    )


def test_sum_confirmations_costs(confirmations, confirmations_with_costs):
    results = sum_confirmations_costs(confirmations)

    pd.testing.assert_frame_equal(results, confirmations_with_costs)


def test_calc_trades_costs(confirmations_with_costs, trades, trades_with_costs):
    results = calc_trades_costs(confirmations_with_costs, trades)

    pd.testing.assert_frame_equal(results, trades_with_costs)


def test_calc_subscriptions_net_amounts(subscriptions, subscriptions_with_net_amount):
    results = calc_subscriptions_net_amounts(subscriptions)

    pd.testing.assert_frame_equal(results, subscriptions_with_net_amount)
