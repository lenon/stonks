import pandas as pd
import pytest
from pandas import to_datetime as dt
from stonks.events import buy, sell, concat_dfs
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


def test_sell_position():
    positions = make_positions(
        [{"symbol": "AAA", "quantity": 16.0, "cost": 198.26, "cost_per_share": 12.39125}]
    )
    expected = make_positions(
        # cost per share shouldn't change
        [{"symbol": "AAA", "quantity": 11.0, "cost": 136.30375, "cost_per_share": 12.39125}]
    )
    event = make_event(
        {
            "date": dt("2022-01-03"),
            "broker": "Acme",
            "symbol": "AAA",
            "type": "sell",
            "quantity": 5.0,
            "price": 20.0,
            "amount": 100.0,
            "costs": 1.07,
            "net_amount": 98.93,
            "event": "trade",
        }
    )

    sell(positions, event)

    assert_frame_equal(positions, expected)


def test_sell_closing_position():
    positions = make_positions(
        [
            {"symbol": "AAA", "quantity": 8.0, "cost": 80.0, "cost_per_share": 10.0},
            {"symbol": "BBB", "quantity": 10.0, "cost": 200.0, "cost_per_share": 20.0},
        ]
    )
    expected = make_positions(
        [{"symbol": "BBB", "quantity": 10.0, "cost": 200.0, "cost_per_share": 20.0}]
    )
    event = make_event(
        {
            "date": dt("2022-01-03"),
            "broker": "Acme",
            "symbol": "AAA",
            "type": "sell",
            "quantity": 8.0,
            "price": 20.0,
            "amount": 160.0,
            "costs": 2.0,
            "net_amount": 158.0,
            "event": "trade",
        }
    )

    sell(positions, event)

    assert_frame_equal(positions, expected)


def test_sell_without_an_opened_position():
    positions = make_positions(
        [{"symbol": "AAA", "quantity": 8.0, "cost": 80.0, "cost_per_share": 10.0}]
    )
    event = make_event(
        {
            "date": dt("2022-01-03"),
            "broker": "Acme",
            "symbol": "BBB",
            "type": "sell",
            "quantity": 8.0,
            "price": 20.0,
            "amount": 160.0,
            "costs": 2.0,
            "net_amount": 158.0,
            "event": "trade",
        }
    )

    with pytest.raises(ValueError, match="can't sell position BBB as it is not open"):
        sell(positions, event)
