import pandas as pd
from pathlib import Path


def fixture_path(fixture):
    return Path(__file__).parent.joinpath("fixtures", fixture).resolve()


def make_positions(data):
    df = pd.DataFrame.from_records(
        data, index="symbol", columns=["symbol", "quantity", "cost", "cost_per_share"]
    )
    df.index.name = None  # reset index name otherwise frame comparison fails
    return df


def make_event(data):
    return pd.Series(data)
