from pathlib import Path

import pandas as pd


def fixture_path(fixture):
    return Path(__file__).parent.joinpath("fixtures", fixture).resolve()


def make_event(**data):
    return pd.Series(data)
