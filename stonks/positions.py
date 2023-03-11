import pandas as pd
from .events import event_fn, concat_events, filter_by_date
from .schemas import Rights, Splits, Trades, Mergers, SpinOffs, StockDividends


class Positions:
    def __init__(self):
        self._df = pd.DataFrame(columns=["quantity", "cost", "cost_per_share"]).rename_axis(
            "symbol"
        )

    def is_open(self, symbol):
        return symbol in self._df.index

    def is_closed(self, symbol):
        return not self.is_open(symbol)

    def find(self, symbol):
        return self._df.loc[symbol]

    def update(self, symbol, quantity, cost, cost_per_share):
        self._df.loc[symbol] = {
            "quantity": quantity,
            "cost": cost,
            "cost_per_share": cost_per_share,
        }

    def close(self, symbol):
        self._df.drop(labels=symbol, inplace=True)

    def to_df(self):
        # return a dataframe sorted by symbol, with 2 decimal places and a
        # sequential numeric index
        return self._df.sort_index().round(2).reset_index()


def calc_positions(date, trades, rights, splits, mergers, spin_offs, stock_dividends):
    trades_df = Trades(trades)
    rights_df = Rights(rights)
    splits_df = Splits(splits)
    mergers_df = Mergers(mergers)
    spin_offs_df = SpinOffs(spin_offs)
    stock_dividends_df = StockDividends(stock_dividends)

    events = concat_events(
        ["trade", trades_df.reset_index()],
        ["right", rights_df.reset_index()],
        ["split", splits_df],
        ["merger", mergers_df],
        ["spin_off", spin_offs_df],
        ["stock_dividend", stock_dividends_df],
    )
    filtered_events = filter_by_date(events=events, date=date)
    positions = Positions()

    for _, event in filtered_events.iterrows():
        fn = event_fn(event)
        fn(positions, event)

    return positions.to_df()
