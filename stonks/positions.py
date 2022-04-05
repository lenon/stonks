import pandas as pd
from .costs import (
    calc_trades_costs,
    calc_confirmations_costs,
    calc_subscriptions_net_amounts,
)
from .utils import columns_to_snake_case
from .events import event_fn, concat_events


def _read_sheet(xlsx, sheet_name):
    return pd.read_excel(xlsx, sheet_name=sheet_name).rename(columns=columns_to_snake_case)


def calc_positions(xlsx):
    # confirmations (or "notas de corretagem") include a summary of all trades made in a single day
    # they are needed to calculate the cost basis for each position
    confirmations = (
        _read_sheet(xlsx, "confirmations")
        .set_index(["date", "broker"])
        .pipe(calc_confirmations_costs)
    )
    # trades contain all buys and sells of stocks
    trades = (
        _read_sheet(xlsx, "trades")
        .set_index(["date", "broker"])
        .pipe(calc_trades_costs, confirmations)
    )

    # other corporate actions that are needed to calculate the current porfolio
    subscriptions = _read_sheet(xlsx, "subscriptions").pipe(calc_subscriptions_net_amounts)
    splits = _read_sheet(xlsx, "splits")
    mergers = _read_sheet(xlsx, "mergers")
    spinoffs = _read_sheet(xlsx, "spinoffs")

    events = concat_events(
        ["trade", trades.reset_index()],
        ["subscription", subscriptions],
        ["split", splits],
        ["merger", mergers],
        ["spinoff", spinoffs],
    )

    positions = pd.DataFrame(columns=["quantity", "cost", "cost_per_share"])

    for _, event in events.iterrows():
        fn = event_fn(event)
        fn(positions, event)

    sorted_positions = (
        positions.sort_index().round(2).reset_index().rename(columns={"index": "symbol"})
    )

    return [
        sorted_positions,
        confirmations,
        trades,
        subscriptions,
        splits,
        mergers,
        spinoffs,
        events,
    ]
