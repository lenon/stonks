import pandas as pd
from .events import event_fn, concat_events
from .schemas import (
    SplitSchema,
    TradeSchema,
    MergerSchema,
    SpinoffSchema,
    SubscriptionSchema,
)


def calc_positions(trades, subscriptions, splits, mergers, spinoffs):
    trades_df = TradeSchema(trades)
    subscriptions_df = SubscriptionSchema(subscriptions)
    splits_df = SplitSchema(splits)
    mergers_df = MergerSchema(mergers)
    spinoffs_df = SpinoffSchema(spinoffs)

    events = concat_events(
        ["trade", trades_df.reset_index()],
        ["subscription", subscriptions_df],
        ["split", splits_df],
        ["merger", mergers_df],
        ["spinoff", spinoffs_df],
    )

    positions = pd.DataFrame(columns=["quantity", "cost", "cost_per_share"])

    for _, event in events.iterrows():
        fn = event_fn(event)
        fn(positions, event)

    sorted_positions = (
        positions.sort_index().round(2).reset_index().rename(columns={"index": "symbol"})
    )

    return sorted_positions
