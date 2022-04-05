import pandas as pd
from stonks.costs import (
    calc_trades_costs,
    sum_confirmations_costs,
    calc_subscriptions_net_amounts,
)


def test_sum_confirmations_costs(confirmations_df, confirmations_costs_df):
    results = sum_confirmations_costs(confirmations_df)

    pd.testing.assert_frame_equal(results, confirmations_costs_df)


def test_calc_trades_costs(confirmations_with_costs_df, trades_df, trades_costs_df):
    results = calc_trades_costs(trades_df, confirmations_with_costs_df)

    pd.testing.assert_frame_equal(results, trades_costs_df)


def test_calc_subscriptions_net_amounts(subscriptions_df, subscriptions_amounts_df):
    results = calc_subscriptions_net_amounts(subscriptions_df)

    pd.testing.assert_frame_equal(results, subscriptions_amounts_df)
