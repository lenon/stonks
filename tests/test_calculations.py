import pandas as pd
from stonks.calculations import (
    calc_trades_costs,
    calc_rights_net_amounts,
    calc_trade_confirmations_costs,
)


def test_calc_trade_confirmations_costs(trade_confirmations_df, trade_confirmations_costs_df):
    results = calc_trade_confirmations_costs(trade_confirmations_df)

    pd.testing.assert_frame_equal(results, trade_confirmations_costs_df)


def test_calc_trades_costs(trade_confirmations_with_costs_df, trades_df, trades_costs_df):
    results = calc_trades_costs(trades_df, trade_confirmations_with_costs_df)

    pd.testing.assert_frame_equal(results, trades_costs_df)


def test_calc_rights_net_amounts(rights_df, rights_amounts_df):
    results = calc_rights_net_amounts(rights_df)

    pd.testing.assert_frame_equal(results, rights_amounts_df)
