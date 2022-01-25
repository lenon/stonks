import pandas as pd
from pytest import fixture
from stonks.costs import (
    sum_confirmation_volume_and_costs,
    calc_trade_amount_and_costs,
    calc_subscription_net_amount,
)


def test_sum_confirmation_volume_and_costs(
    confirmations, confirmations_with_volume_and_costs
):
    results = sum_confirmation_volume_and_costs(confirmations)

    pd.testing.assert_frame_equal(results, confirmations_with_volume_and_costs)


def test_calc_trade_amount_and_costs(
    confirmations_with_volume_and_costs, trades, trades_with_costs
):
    results = calc_trade_amount_and_costs(confirmations_with_volume_and_costs, trades)

    pd.testing.assert_frame_equal(results, trades_with_costs)


def test_calc_subscription_net_amount(subscriptions, subscriptions_with_net_amount):
    results = calc_subscription_net_amount(subscriptions)

    pd.testing.assert_frame_equal(results, subscriptions_with_net_amount)
