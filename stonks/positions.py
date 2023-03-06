import pandas as pd
from .events import event_fn, concat_events, filter_by_date
from .schemas import Rights, Splits, Trades, Mergers, SpinOffs, StockDividends


def calc_positions(date, trades, rights, splits, mergers, spin_offs, stock_dividends):
    trades_df = Trades(trades)
    rights_df = Rights(rights)
    splits_df = Splits(splits)
    mergers_df = Mergers(mergers)
    spin_offs_df = SpinOffs(spin_offs)
    stock_dividends_df = StockDividends(stock_dividends)

    events = concat_events(
        ["trade", trades_df.reset_index()],
        ["right", rights_df],
        ["split", splits_df],
        ["merger", mergers_df],
        ["spin_off", spin_offs_df],
        ["stock_dividend", stock_dividends_df],
    )
    filtered_events = filter_by_date(events=events, date=date)
    positions = pd.DataFrame(columns=["quantity", "cost", "cost_per_share"])

    for _, event in filtered_events.iterrows():
        fn = event_fn(event)
        fn(positions, event)

    sorted_positions = (
        positions.sort_index().round(2).reset_index().rename(columns={"index": "symbol"})
    )

    return sorted_positions
