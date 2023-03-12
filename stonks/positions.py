import pandas as pd


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
