import math
import pandas as pd
from .utils import ratio_to_float
from datetime import date


def concat_events(*dfs):
    events = [df.assign(event=event) for event, df in dfs]

    return pd.concat(events).sort_values(by="date", ignore_index=True)


def buy(positions, event):
    if event.symbol not in positions.index:
        # first buy, not yet in positions dataframe
        new_quantity = event.quantity
        new_cost = event.net_amount
        new_cost_per_share = event.net_amount / event.quantity
    else:
        # bought it before, let's update cost per share
        prev = positions.loc[event.symbol]

        new_quantity = prev.quantity + event.quantity
        new_cost = prev.cost + event.net_amount
        new_cost_per_share = new_cost / new_quantity

    positions.loc[event.symbol] = {
        "quantity": new_quantity,
        "cost": new_cost,
        "cost_per_share": new_cost_per_share,
    }


def sell(positions, event):
    if event.symbol not in positions.index:
        raise ValueError(f"can't sell position {event.symbol} as it is not open")

    prev = positions.loc[event.symbol]
    new_quantity = prev.quantity - event.quantity
    new_cost = new_quantity * prev.cost_per_share

    if new_quantity == 0:
        # closing position if there's nothing left in stock
        positions.drop(labels=event.symbol, inplace=True)
    else:
        positions.loc[event.symbol] = {
            "quantity": new_quantity,
            "cost": new_cost,
            # cost per share stay the same
            "cost_per_share": prev.cost_per_share,
        }


def subscription(positions, event):
    # subscriptions not yet issued must not change current positions
    if pd.isnull(event.issue_date) or event.issue_date.date() > date.today():
        return

    if event.symbol not in positions.index:
        # first subscription, not yet in positions dataframe
        new_quantity = event.exercised
        new_cost = event.net_amount
        new_cost_per_share = event.net_amount / event.exercised
    else:
        # subscription for a position that is already open
        prev = positions.loc[event.symbol]

        new_cost = prev.cost + event.net_amount
        new_cost_per_share = new_cost / (prev.quantity + event.exercised)
        new_quantity = prev.quantity + event.exercised

    positions.loc[event.symbol] = {
        "quantity": new_quantity,
        "cost": new_cost,
        "cost_per_share": new_cost_per_share,
    }


def merger(positions, event):
    if event.symbol not in positions.index:
        raise ValueError(
            f"can't merge {event.symbol} into {event.acquirer} as {event.symbol} position is not open"
        )

    position_to_merge = positions.loc[event.symbol]
    ratio = ratio_to_float(event.ratio)

    # quantity should be truncated because fractional shares are not allowed on B3
    quantity = math.trunc(position_to_merge.quantity / ratio)
    cost_per_share = position_to_merge.cost / quantity

    positions.drop(labels=event.symbol, inplace=True)
    positions.loc[event.acquirer] = {
        "quantity": quantity,
        "cost": position_to_merge.cost,
        "cost_per_share": cost_per_share,
    }


def split(positions, event):
    if event.symbol not in positions.index:
        raise ValueError(f"can't split position {event.symbol} as it is not open")

    position_to_split = positions.loc[event.symbol]
    ratio = ratio_to_float(event.ratio)

    new_quantity = position_to_split.quantity * ratio
    new_cost_per_share = position_to_split.cost / new_quantity

    positions.loc[event.symbol] = {
        "quantity": new_quantity,
        "cost": position_to_split.cost,
        "cost_per_share": new_cost_per_share,
    }


def spinoff(positions, event):
    if event.symbol not in positions.index:
        raise ValueError(f"can't spinoff position {event.symbol} as it is not open")

    position_to_spinoff = positions.loc[event.symbol]
    ratio = ratio_to_float(event.ratio)

    newco_quantity = math.trunc(position_to_spinoff.quantity / ratio)
    newco_cost = position_to_spinoff.cost * event.cost_basis
    newco_cost_per_share = newco_cost / newco_quantity

    new_quantity = position_to_spinoff.quantity
    new_cost = position_to_spinoff.cost - newco_cost
    new_cost_per_share = new_cost / position_to_spinoff.quantity

    positions.loc[event.new_company] = {
        "quantity": newco_quantity,
        "cost": newco_cost,
        "cost_per_share": newco_cost_per_share,
    }
    positions.loc[event.symbol] = {
        "quantity": new_quantity,
        "cost": new_cost,
        "cost_per_share": new_cost_per_share,
    }


def event_fn(e):
    match e:
        case pd.Series(event="trade", type="buy"):
            return buy
        case pd.Series(event="trade", type="sell"):
            return sell
        case pd.Series(event="subscription"):
            return subscription
        case pd.Series(event="merger"):
            return merger
        case pd.Series(event="split"):
            return split
        case pd.Series(event="spinoff"):
            return spinoff
        case _:
            raise ValueError(f"unknown event type {e.event}")
