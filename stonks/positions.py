from pandas import DataFrame, Series


class Positions:
    def __init__(self) -> None:
        self._df = DataFrame(columns=["quantity", "cost", "cost_per_share"]).rename_axis("symbol")

    def is_open(self, symbol: str) -> bool:
        return symbol in self._df.index

    def is_closed(self, symbol: str) -> bool:
        return not self.is_open(symbol)

    def find(self, symbol: str) -> Series:
        position: Series = self._df.loc[symbol]
        return position

    def update(self, symbol: str, quantity: float, cost: float, cost_per_share: float) -> None:
        self._df.loc[symbol] = {
            "quantity": quantity,
            "cost": cost,
            "cost_per_share": cost_per_share,
        }

    def close(self, symbol: str) -> None:
        self._df.drop(labels=symbol, inplace=True)

    def to_df(self) -> DataFrame:
        # return a dataframe sorted by symbol
        # round cost and cost per share, keep quantity as is
        return self._df.sort_index().round({"cost": 2, "cost_per_share": 2})
