from datetime import date
from pandas.testing import assert_frame_equal
from stonks.calculations import (
    calc_positions,
    calc_us_trades,
    calc_trades_costs,
    calc_us_positions,
    calc_rights_amounts,
    calc_trade_confirmations_costs,
)


def test_calc_trade_confirmations_costs(trade_confirmations_df, trade_confirmations_costs_df):
    results = calc_trade_confirmations_costs(trade_confirmations_df)

    assert_frame_equal(results, trade_confirmations_costs_df)


def test_calc_trades_costs(trade_confirmations_with_costs_df, trades_df, trades_costs_df):
    results = calc_trades_costs(trades_df, trade_confirmations_with_costs_df)

    assert_frame_equal(results, trades_costs_df)


def test_calc_rights_amounts(rights_df, rights_amounts_df):
    results = calc_rights_amounts(rights_df)

    assert_frame_equal(results, rights_amounts_df)


def test_calc_positions(
    positions_df,
    trades_with_costs_df,
    rights_with_amounts_df,
    splits_df,
    mergers_df,
    spin_offs_df,
    stock_dividends_df,
):
    actual_positions = calc_positions(
        date=date.today(),
        trades=trades_with_costs_df,
        rights=rights_with_amounts_df,
        splits=splits_df,
        mergers=mergers_df,
        spin_offs=spin_offs_df,
        stock_dividends=stock_dividends_df,
    )

    assert_frame_equal(actual_positions, positions_df)


def test_calc_us_trades(us_trades_df, ptax_df, us_trades_ptax_df):
    results = calc_us_trades(us_trades_df, ptax_df)

    assert_frame_equal(results, us_trades_ptax_df)


def test_calc_us_positions(
    us_positions_df,
    us_trades_with_ptax_df,
):
    actual_positions = calc_us_positions(
        date=date.today(),
        trades=us_trades_with_ptax_df,
    )

    assert_frame_equal(actual_positions, us_positions_df)
