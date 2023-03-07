import pandas as pd
from pathlib import Path


def fixture_path(fixture):
    return Path(__file__).parent.joinpath("fixtures", fixture).resolve()


def make_event(**data):
    return pd.Series(data)
