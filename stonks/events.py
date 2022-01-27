import pandas as pd


def concat_dfs(*dfs):
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