import pandas as pd
import pytest
from pandas import to_datetime as dt
from datetime import datetime, timedelta
from .helpers import make_event, make_position, make_positions_df
from stonks.errors import UnknownEventError, PositionNotOpenError
from stonks.events import (
    buy,
    sell,
    right,
    split,
    merger,
    event_fn,
    spin_off,
    concat_events,
    filter_by_date,
    stock_dividend,
)
from pandas.testing import assert_frame_equal


def test_concat_events(
    trades_with_costs_df,
    rights_with_amounts_df,
    splits_df,
    mergers_df,
    spin_offs_df,
    events_df,
    stock_dividends_df,
):
    result = concat_events(
        ["trade", trades_with_costs_df.reset_index()],
        ["right", rights_with_amounts_df],
        ["split", splits_df],
        ["merger", mergers_df],
        ["spin_off", spin_offs_df],
        ["stock_dividend", stock_dividends_df],
    )

    assert_frame_equal(result, events_df)


def test_filter_by_date(events_df, events_filtered_df):
    result = filter_by_date(events=events_df, date="2022-02-15")

    assert_frame_equal(result, events_filtered_df)


def test_buy_new_position():
    positions = make_positions_df([])
    expected = make_positions_df(
        [make_position("AAA", quantity=8.0, cost=101.4, cost_per_share=12.675)]
    )
    event = make_event(
        date=dt("2022-01-01"),
        broker="Acme",
        symbol="AAA",
        type="buy",
        quantity=8.0,
        price=12.5,
        amount=100,
        costs=1.4,
        net_amount=101.4,
        event="trade",
    )

    buy(positions, event)

    assert_frame_equal(positions, expected)


def test_buy_second_time():
    positions = make_positions_df(
        [make_position("AAA", quantity=8.0, cost=101.4, cost_per_share=12.675)]
    )
    expected = make_positions_df(
        [make_position("AAA", quantity=16.0, cost=198.26, cost_per_share=12.39125)]
    )
    event = make_event(
        date=dt("2022-01-02"),
        broker="Acme",
        symbol="AAA",
        type="buy",
        quantity=8.0,
        price=12.0,
        amount=96.0,
        costs=0.86,
        net_amount=96.86,
        event="trade",
    )

    buy(positions, event)

    assert_frame_equal(positions, expected)


def test_sell_position():
    positions = make_positions_df(
        [make_position("AAA", quantity=16.0, cost=198.26, cost_per_share=12.39125)]
    )
    expected = make_positions_df(
        # cost per share shouldn't change
        [make_position("AAA", quantity=11.0, cost=136.30375, cost_per_share=12.39125)]
    )
    event = make_event(
        date=dt("2022-01-03"),
        broker="Acme",
        symbol="AAA",
        type="sell",
        quantity=5.0,
        price=20.0,
        amount=100.0,
        costs=1.07,
        net_amount=98.93,
        event="trade",
    )

    sell(positions, event)

    assert_frame_equal(positions, expected)


def test_sell_closing_position():
    positions = make_positions_df(
        [
            make_position("AAA", quantity=8.0, cost=80.0, cost_per_share=10.0),
            make_position("BBB", quantity=10.0, cost=200.0, cost_per_share=20.0),
        ]
    )
    expected = make_positions_df(
        [make_position("BBB", quantity=10.0, cost=200.0, cost_per_share=20.0)]
    )
    event = make_event(
        date=dt("2022-01-03"),
        broker="Acme",
        symbol="AAA",
        type="sell",
        quantity=8.0,
        price=20.0,
        amount=160.0,
        costs=2.0,
        net_amount=158.0,
        event="trade",
    )

    sell(positions, event)

    assert_frame_equal(positions, expected)


def test_sell_without_an_open_position():
    positions = make_positions_df(
        [make_position("AAA", quantity=8.0, cost=80.0, cost_per_share=10.0)]
    )
    event = make_event(
        date=dt("2022-01-03"),
        broker="Acme",
        symbol="BBB",
        type="sell",
        quantity=8.0,
        price=20.0,
        amount=160.0,
        costs=2.0,
        net_amount=158.0,
        event="trade",
    )

    with pytest.raises(PositionNotOpenError, match="position not open: BBB"):
        sell(positions, event)


def test_right_with_new_position():
    positions = make_positions_df([])
    expected = make_positions_df(
        [make_position("ABC", quantity=90.0, cost=4509.0, cost_per_share=50.1)]
    )
    event = make_event(
        date=dt("2022-01-01"),
        broker="Acme",
        symbol="ABC",
        price=50.1,
        net_amount=4509.0,
        event="right",
        description="4th subs",
        start=dt("2022-01-01"),
        end=dt("2022-01-02"),
        settlement=dt("2022-01-03"),
        shares=100.0,
        exercised=90.0,
        issue_date=dt("2022-01-10"),
    )

    right(positions, event)

    assert_frame_equal(positions, expected)


def test_right_for_existing_position():
    positions = make_positions_df(
        [make_position("ABC", quantity=90.0, cost=4509.0, cost_per_share=50.1)]
    )
    expected = make_positions_df(
        [make_position("ABC", quantity=140.0, cost=5034.0, cost_per_share=35.957143)]
    )
    event = make_event(
        date=dt("2022-01-10"),
        broker="Acme",
        symbol="ABC",
        price=10.5,
        net_amount=525.0,
        event="right",
        description="5th subs",
        start=dt("2022-01-10"),
        end=dt("2022-01-11"),
        settlement=dt("2022-01-12"),
        shares=50.0,
        exercised=50.0,
        issue_date=dt("2022-01-13"),
    )

    right(positions, event)

    assert_frame_equal(positions, expected)


def test_right_without_issue_date():
    positions = make_positions_df(
        [make_position("ABC", quantity=90.0, cost=4509.0, cost_per_share=50.1)]
    )
    expected = make_positions_df(
        [make_position("ABC", quantity=90.0, cost=4509.0, cost_per_share=50.1)]
    )
    event = make_event(
        date=dt("2022-01-10"),
        broker="Acme",
        symbol="ABC",
        price=10.5,
        net_amount=525.0,
        event="right",
        description="5th subs",
        start=dt("2022-01-10"),
        end=dt("2022-01-11"),
        settlement=dt("2022-01-12"),
        shares=50.0,
        exercised=50.0,
        issue_date=None,
    )

    right(positions, event)

    assert_frame_equal(positions, expected)


def test_right_with_future_issue_date():
    positions = make_positions_df(
        [make_position("ABC", quantity=90.0, cost=4509.0, cost_per_share=50.1)]
    )
    expected = make_positions_df(
        [make_position("ABC", quantity=90.0, cost=4509.0, cost_per_share=50.1)]
    )
    event = make_event(
        date=dt("2022-01-10"),
        broker="Acme",
        symbol="ABC",
        price=10.5,
        net_amount=525.0,
        event="right",
        description="5th subs",
        start=dt("2022-01-10"),
        end=dt("2022-01-11"),
        settlement=dt("2022-01-12"),
        shares=50.0,
        exercised=50.0,
        issue_date=datetime.now() + timedelta(days=10),
    )

    right(positions, event)

    assert_frame_equal(positions, expected)


def test_merger():
    positions = make_positions_df(
        [make_position("ABC", quantity=10.0, cost=109.0, cost_per_share=10.9)]
    )
    expected = make_positions_df(
        [make_position("NEWCO", quantity=5, cost=109.0, cost_per_share=21.8)]
    )
    event = make_event(
        date=dt("2022-01-10"),
        symbol="ABC",
        event="merger",
        ratio="2:1",
        acquirer="NEWCO",
    )

    merger(positions, event)

    assert_frame_equal(positions, expected)


def test_merger_without_open_position():
    positions = make_positions_df([])
    event = make_event(
        date=dt("2022-01-10"),
        symbol="ABC",
        event="merger",
        ratio="2:1",
        acquirer="NEWCO",
    )

    with pytest.raises(PositionNotOpenError, match="position not open: ABC"):
        merger(positions, event)


def test_split():
    positions = make_positions_df(
        [make_position("ABC", quantity=10.0, cost=109.0, cost_per_share=10.9)]
    )
    expected = make_positions_df(
        [make_position("ABC", quantity=100.0, cost=109.0, cost_per_share=1.09)]
    )
    event = make_event(date=dt("2022-01-05"), symbol="ABC", event="split", ratio="10:1")

    split(positions, event)

    assert_frame_equal(positions, expected)


def test_split_without_open_position():
    positions = make_positions_df([])
    event = make_event(date=dt("2022-01-05"), symbol="ABC", event="split", ratio="10:1")

    with pytest.raises(PositionNotOpenError, match="position not open: ABC"):
        split(positions, event)


def test_spin_off():
    positions = make_positions_df(
        [make_position("ABC", quantity=100.0, cost=1090.0, cost_per_share=10.9)]
    )
    expected = make_positions_df(
        [
            make_position("ABC", quantity=100.0, cost=654.0, cost_per_share=6.54),
            make_position("NEWCO", quantity=50.0, cost=436.0, cost_per_share=8.72),
        ]
    )
    event = make_event(
        date=dt("2022-03-01"),
        symbol="ABC",
        event="spin_off",
        ratio="2:1",
        new_company="NEWCO",
        cost_basis=0.4,
    )

    spin_off(positions, event)

    assert_frame_equal(positions, expected)


def test_spin_off_without_open_position():
    positions = make_positions_df([])
    event = make_event(
        date=dt("2022-03-01"),
        symbol="ABC",
        event="spin_off",
        ratio="2:1",
        new_company="NEWCO",
        cost_basis=0.4,
    )

    with pytest.raises(PositionNotOpenError, match="position not open: ABC"):
        spin_off(positions, event)


def test_stock_dividend():
    positions = make_positions_df(
        [make_position("ABC", quantity=10.0, cost=109.0, cost_per_share=10.9)]
    )
    expected = make_positions_df(
        [make_position("ABC", quantity=20.0, cost=109.0, cost_per_share=5.45)]
    )
    event = make_event(date=dt("2022-01-05"), symbol="ABC", event="stock_dividend", quantity=10)

    stock_dividend(positions, event)

    assert_frame_equal(positions, expected)


def test_stock_dividend_without_open_position():
    positions = make_positions_df([])
    event = make_event(date=dt("2022-01-05"), symbol="ABC", event="stock_dividend", quantity=10)

    with pytest.raises(PositionNotOpenError, match="position not open: ABC"):
        stock_dividend(positions, event)


def test_event_fn():
    event_trade_buy = pd.Series({"event": "trade", "type": "buy"})
    event_trade_sell = pd.Series({"event": "trade", "type": "sell"})
    event_right = pd.Series({"event": "right"})
    event_merger = pd.Series({"event": "merger"})
    event_split = pd.Series({"event": "split"})
    event_spin_off = pd.Series({"event": "spin_off"})
    event_unknown = pd.Series({"event": "foo"})

    assert event_fn(event_trade_buy) == buy
    assert event_fn(event_trade_sell) == sell
    assert event_fn(event_right) == right
    assert event_fn(event_merger) == merger
    assert event_fn(event_split) == split
    assert event_fn(event_spin_off) == spin_off

    with pytest.raises(UnknownEventError, match="unknown event type: foo"):
        event_fn(event_unknown)
