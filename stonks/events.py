import math
import pandas as pd
from pandas import Series, DataFrame
from typing import Callable
from .utils import ratio_to_float
from .errors import UnknownEventError, PositionNotOpenError
from datetime import date
from .positions import Positions


def concat_events(*dfs: tuple[str, DataFrame]) -> DataFrame:
    events = [df.assign(event=event) for event, df in dfs]

    # `ignore_index` will create a new sequential index, which will work as ID for the `sort_values` below. For events
    # with the same date, the ID will be used to differentiate between then and ensure the order of appearance is
    # respected.
    combined_dfs = pd.concat(events, ignore_index=True).rename_axis("id")
    sorted_dfs = combined_dfs.sort_values(by=["date", "id"], ignore_index=True)

    return sorted_dfs


def filter_by_date(events: DataFrame, date: date) -> DataFrame:
    return events.query(
        "(event == 'right' and issue_date <= @date) or (event != 'right' and date <= @date)"
    )


def buy(positions: Positions, event: Series) -> None:
    if positions.is_closed(event.symbol):
        # first buy, not yet in positions dataframe
        new_quantity = event.quantity
        new_cost = event.amount
        new_cost_per_share = event.amount / event.quantity
    else:
        # bought it before, let's sum quantity and update cost per share
        prev = positions.find(event.symbol)

        new_quantity = prev.quantity + event.quantity
        new_cost = prev.cost + event.amount
        new_cost_per_share = new_cost / new_quantity

    positions.update(
        event.symbol, quantity=new_quantity, cost=new_cost, cost_per_share=new_cost_per_share
    )


def sell(positions: Positions, event: Series) -> None:
    if positions.is_closed(event.symbol):
        # safeguard against incorrect data
        raise PositionNotOpenError(event.symbol)

    prev = positions.find(event.symbol)
    # sells affect quantity and total costs
    new_quantity = prev.quantity - event.quantity
    new_cost = new_quantity * prev.cost_per_share

    if new_quantity == 0:
        # sold all stocks, closing position
        positions.close(event.symbol)
    else:
        positions.update(
            event.symbol,
            quantity=new_quantity,
            cost=new_cost,
            # sells do not affect cost per share
            cost_per_share=prev.cost_per_share,
        )


def right(positions: Positions, event: Series) -> None:
    # rights not yet issued must not change current positions
    if pd.isnull(event.issue_date) or event.issue_date.date() > date.today():
        return

    if positions.is_closed(event.symbol):
        # first right, not yet in positions dataframe
        new_quantity = event.exercised
        new_cost = event.amount
        new_cost_per_share = event.amount / event.exercised
    else:
        # right for a position that is already open
        prev = positions.find(event.symbol)

        new_cost = prev.cost + event.amount
        new_cost_per_share = new_cost / (prev.quantity + event.exercised)
        new_quantity = prev.quantity + event.exercised

    positions.update(
        event.symbol, quantity=new_quantity, cost=new_cost, cost_per_share=new_cost_per_share
    )


def merger(positions: Positions, event: Series) -> None:
    if positions.is_closed(event.symbol):
        # safeguard against incorrect data
        raise PositionNotOpenError(event.symbol)

    position_to_merge = positions.find(event.symbol)
    ratio = ratio_to_float(event.ratio)

    # quantity should be truncated because fractional shares are not allowed on B3
    quantity = math.trunc(position_to_merge.quantity / ratio)
    # cost basis is not affected by the merger event
    cost = position_to_merge.cost
    cost_per_share = position_to_merge.cost / quantity

    # drop the old position and replace by acquirer company symbol
    positions.close(event.symbol)
    positions.update(event.acquirer, quantity=quantity, cost=cost, cost_per_share=cost_per_share)


def split(positions: Positions, event: Series) -> None:
    if positions.is_closed(event.symbol):
        # safeguard against incorrect data
        raise PositionNotOpenError(event.symbol)

    position_to_split = positions.find(event.symbol)
    ratio = ratio_to_float(event.ratio)

    # splits only affect quantity and cost per share
    # total cost does not change
    new_quantity = position_to_split.quantity * ratio
    new_cost_per_share = position_to_split.cost / new_quantity

    positions.update(
        event.symbol,
        quantity=new_quantity,
        cost=position_to_split.cost,
        cost_per_share=new_cost_per_share,
    )


def spin_off(positions: Positions, event: Series) -> None:
    if positions.is_closed(event.symbol):
        # safeguard against incorrect data
        raise PositionNotOpenError(event.symbol)

    position_to_spin_off = positions.find(event.symbol)
    ratio = ratio_to_float(event.ratio)

    newco_quantity = math.trunc(position_to_spin_off.quantity / ratio)
    newco_cost = position_to_spin_off.cost * event.cost_basis
    newco_cost_per_share = newco_cost / newco_quantity

    new_quantity = position_to_spin_off.quantity
    new_cost = position_to_spin_off.cost - newco_cost
    new_cost_per_share = new_cost / position_to_spin_off.quantity

    positions.update(
        event.new_company,
        quantity=newco_quantity,
        cost=newco_cost,
        cost_per_share=newco_cost_per_share,
    )
    positions.update(
        event.symbol, quantity=new_quantity, cost=new_cost, cost_per_share=new_cost_per_share
    )


def stock_dividend(positions: Positions, event: Series) -> None:
    if positions.is_closed(event.symbol):
        # safeguard against incorrect data
        raise PositionNotOpenError(event.symbol)

    prev = positions.find(event.symbol)

    new_quantity = prev.quantity + event.quantity
    new_cost = prev.cost + (event.quantity * event.cost)
    new_cost_per_share = new_cost / new_quantity

    positions.update(
        event.symbol, quantity=new_quantity, cost=new_cost, cost_per_share=new_cost_per_share
    )


def event_fn(e: Series) -> Callable[[Positions, Series], None]:
    match e:
        case Series(event="trade", type="buy"):
            return buy
        case Series(event="trade", type="sell"):
            return sell
        case Series(event="right"):
            return right
        case Series(event="merger"):
            return merger
        case Series(event="split"):
            return split
        case Series(event="spin_off"):
            return spin_off
        case Series(event="stock_dividend"):
            return stock_dividend
        case _:
            raise UnknownEventError(e.event)
