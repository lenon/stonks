import pandas as pd
from pandas import to_datetime as dt
from stonks.events import buy, concat_dfs
from pandas.testing import assert_frame_equal


def test_concat_dfs(trades, subscriptions, splits, mergers, spinoffs, events):
    result = concat_dfs(
        ["trade", trades.reset_index()],
        ["subscription", subscriptions],
        ["split", splits],
        ["merger", mergers],
        ["spinoff", spinoffs],
    )

    pd.testing.assert_frame_equal(result, events)


def make_positions(data):
    df = pd.DataFrame.from_records(
        data, index="symbol", columns=["symbol", "quantity", "cost", "cost_per_share"]
    )
    df.index.name = None  # reset index name otherwise df comparison fails
    return df


def make_event(data):
    return pd.Series(data)


def test_buy_new_position():
    positions = make_positions([])
    expected = make_positions(
        [{"symbol": "AAA", "quantity": 8.0, "cost": 101.4, "cost_per_share": 12.675}]
    )
    event = make_event(
        {
            "date": dt("2022-01-01"),
            "broker": "Acme",
            "symbol": "AAA",
            "type": "buy",
            "quantity": 8.0,
            "price": 12.5,
            "amount": 100,
            "costs": 1.4,
            "net_amount": 101.4,
            "event": "trade",
        }
    )

    buy(positions, event)

    assert_frame_equal(positions, expected)


def test_buy_second_time():
    positions = make_positions(
        [{"symbol": "AAA", "quantity": 8.0, "cost": 101.4, "cost_per_share": 12.675}]
    )
    expected = make_positions(
        [{"symbol": "AAA", "quantity": 16.0, "cost": 198.26, "cost_per_share": 12.39125}]
    )
    event = make_event(
        {
            "date": dt("2022-01-02"),
            "broker": "Acme",
            "symbol": "AAA",
            "type": "buy",
            "quantity": 8.0,
            "price": 12.0,
            "amount": 96.0,
            "costs": 0.86,
            "net_amount": 96.86,
            "event": "trade",
        }
    )

    buy(positions, event)

    assert_frame_equal(positions, expected)
