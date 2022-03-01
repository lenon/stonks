import pandas as pd
from pytest import fixture
from .helpers import fixture_path
from pandas.testing import assert_frame_equal
from stonks.positions import calc_positions


@fixture
def positions():
    return pd.read_csv(fixture_path("positions.csv"))


def test_calc_positions(
    positions, confirmations, trades, subscriptions, splits, mergers, spinoffs, events
):
    xlsx = pd.ExcelFile(fixture_path("br-sample.xlsx"))

    (
        actual_positions,
        actual_confirmations,
        actual_trades,
        actual_subscriptions,
        actual_splits,
        actual_mergers,
        actual_spinoffs,
        actual_events,
    ) = calc_positions(xlsx)

    assert_frame_equal(actual_positions, positions)
    assert_frame_equal(actual_confirmations, confirmations)
    assert_frame_equal(actual_trades, trades)
    assert_frame_equal(actual_subscriptions, subscriptions)
    assert_frame_equal(actual_splits, splits)
    assert_frame_equal(actual_mergers, mergers)
    assert_frame_equal(actual_spinoffs, spinoffs)
    assert_frame_equal(actual_events, events)
