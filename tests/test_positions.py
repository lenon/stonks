import pandas as pd
from shutil import copyfile
from .helpers import fixture_path
from functools import cache
from pandas.testing import assert_frame_equal
from stonks.positions import calc_positions


def test_calc_positions(tmp_path):
    input_fixture = fixture_path("br-sample.xlsx")
    output_fixture = fixture_path("br-sample-positions.xlsx")

    test_input_path = tmp_path.joinpath("br-sample.xlsx")
    test_output_path = tmp_path.joinpath("br-sample-positions.xlsx")

    # copy sample to the tmp folder and use it as function input
    copyfile(input_fixture, test_input_path)

    calc_positions(test_input_path)

    actual = pd.read_excel(test_output_path)
    expected = pd.read_excel(output_fixture)

    assert_frame_equal(actual, expected)
