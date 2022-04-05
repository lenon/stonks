from pandas.testing import assert_frame_equal
from stonks.positions import calc_positions


def test_calc_positions(
    positions_df,
    trades_with_costs_df,
    subscriptions_with_amounts_df,
    splits_df,
    mergers_df,
    spinoffs_df,
):
    actual_positions = calc_positions(
        trades=trades_with_costs_df,
        subscriptions=subscriptions_with_amounts_df,
        splits=splits_df,
        mergers=mergers_df,
        spinoffs=spinoffs_df,
    )

    assert_frame_equal(actual_positions, positions_df)
