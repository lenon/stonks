import pandas as pd
from .events import event_fn, concat_events


def calc_positions(trades, subscriptions, splits, mergers, spinoffs):
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

    return sorted_positions
