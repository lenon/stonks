import pandas as pd
from .helpers import fixture_path
from pandas.testing import assert_frame_equal
from stonks.positions import calc_positions


def test_calc_positions():
    input_xlsx = pd.ExcelFile(fixture_path("br-sample.xlsx"))

    actual = calc_positions(input_xlsx)
    expected = pd.read_csv(
        fixture_path("positions.csv"),
    )

    assert_frame_equal(actual, expected)
