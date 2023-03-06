from datetime import date
from pandas.testing import assert_frame_equal
from stonks.positions import calc_positions


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
