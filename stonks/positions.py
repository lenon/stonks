from dataclasses import dataclass

from pandas import DataFrame


@dataclass
class Position:
    quantity: float
    cost: float
    cost_per_share: float


class Positions:
    def __init__(self) -> None:
        self._positions: dict[str, Position] = {}

    def is_open(self, symbol: str) -> bool:
        return symbol in self._positions

    def is_closed(self, symbol: str) -> bool:
        return not self.is_open(symbol)

    def find(self, symbol: str) -> Position:
        return self._positions[symbol]

    def update(self, symbol: str, /, quantity: float, cost: float, cost_per_share: float) -> None:
        self._positions[symbol] = Position(
            quantity=quantity,
            cost=cost,
            cost_per_share=cost_per_share,
        )

    def close(self, symbol: str) -> None:
        self._positions.pop(symbol)

    def to_df(self) -> DataFrame:
        return (
            DataFrame.from_dict(
                self._positions,
                orient="index",
                columns=["quantity", "cost", "cost_per_share"],
            )
            .rename_axis("symbol")  # rename the index
            .sort_index()  # sort by symbol
            .round({"cost": 2, "cost_per_share": 2})  # round costs, keep quantity as is
        )
