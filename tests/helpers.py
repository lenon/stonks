import pandas as pd
from pathlib import Path


def fixture_path(fixture):
    return Path(__file__).parent.joinpath("fixtures", fixture).resolve()


def make_position(symbol, /, quantity, cost, cost_per_share):
    return pd.Series(
        {"symbol": symbol, "quantity": quantity, "cost": cost, "cost_per_share": cost_per_share},
    )


def make_positions(data):
    df = pd.DataFrame(data, columns=["symbol", "quantity", "cost", "cost_per_share"]).set_index(
        "symbol"
    )
    df.index.name = None  # reset index name otherwise frame comparison fails
    return df


def make_event(**data):
    return pd.Series(data)
