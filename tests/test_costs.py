import pandas as pd
from pytest import fixture
from .helpers import fixture_path
from stonks.costs import (
    calc_trades_costs,
    sum_confirmations_costs,
    calc_subscriptions_net_amounts,
)


@fixture
def confirmations_pre_calc():
    return pd.read_csv(
        fixture_path("confirmations-pre-calc.csv"),
        parse_dates=["date"],
        index_col=["date", "broker"],
    )


@fixture
def trades_pre_calc():
    return pd.read_csv(
        fixture_path("trades-pre-calc.csv"),
        parse_dates=["date"],
        index_col=["date", "broker"],
    )


@fixture
def subscriptions_pre_calc():
    return pd.read_csv(
        fixture_path("subscriptions-pre-calc.csv"),
        parse_dates=["date", "start", "end", "settlement", "issue_date"],
    )


def test_sum_confirmations_costs(confirmations_pre_calc, confirmations):
    results = sum_confirmations_costs(confirmations_pre_calc)

    pd.testing.assert_frame_equal(results, confirmations)


def test_calc_trades_costs(confirmations, trades_pre_calc, trades):
    results = calc_trades_costs(confirmations, trades_pre_calc)

    pd.testing.assert_frame_equal(results, trades)


def test_calc_subscriptions_net_amounts(subscriptions_pre_calc, subscriptions):
    results = calc_subscriptions_net_amounts(subscriptions_pre_calc)

    pd.testing.assert_frame_equal(results, subscriptions)
