import numpy as np
import pandas as pd
from pandas import DataFrame
from pandera import check_input
from .events import event_fn, concat_events, filter_by_date
from datetime import date
from .schemas import (
    Rights,
    Splits,
    Trades,
    Mergers,
    SpinOffs,
    StockDividends,
    TradeConfirmations,
    TradeConfirmationsWithNullable,
)
from .positions import Positions


# Trade confirmation is a document that confirms the details of a trade, such as
# the security traded, the price, and the quantity. This function calculates
# some columns required for other calculations below.
#
# Traded volume: is the total value of the securities traded.
# Costs: is the sum of clearing, trading and brokerage fees.
# Net amount: the difference between sales and purchases and costs.
@check_input(TradeConfirmationsWithNullable)
def calc_trade_confirmations_costs(trade_confirmations: DataFrame) -> DataFrame:
    traded_volume = trade_confirmations.sales + trade_confirmations.purchases
    costs = (
        trade_confirmations.clearing_fees
        + trade_confirmations.trading_fees
        + trade_confirmations.brokerage_fees
    )
    net_amount = trade_confirmations.sales - trade_confirmations.purchases - costs

    return pd.concat(
        [traded_volume, costs, net_amount],
        axis="columns",
        keys=["traded_volume", "costs", "net_amount"],
    )


# Calculate pro rata costs for each trade included in a trade confirmation.
#
# Amount: is the quantity of the traded security x price.
# Costs: pro rata costs based on the amount of the traded security.
# Net amount: the amount of traded security + any costs.
@check_input(Trades, "trades")
@check_input(TradeConfirmations, "trade_confirmations")
def calc_trades_costs(trades: DataFrame, trade_confirmations: DataFrame) -> DataFrame:
    # The trade confirmation has a one-to-many association with trades, meaning
    # that a single trade confirmation has one or more trades.
    trades_w_confirmations = trades.join(trade_confirmations, on=["date", "broker"], rsuffix="_c")

    amount = trades_w_confirmations.quantity * trades_w_confirmations.price
    costs = (amount / trades_w_confirmations.traded_volume * trades_w_confirmations.costs_c).round(
        2
    )

    # net amount for buys is principal amount + costs, while for sells it's
    # amount - costs
    costs_with_sign = costs * np.where(trades_w_confirmations.type == "buy", 1, -1)
    net_amount = amount + costs_with_sign

    return pd.concat(
        [amount, costs, net_amount], axis="columns", keys=["amount", "costs", "net_amount"]
    )


# Rights net amount is the cost per share x quantity of exercised shares.
# Costs are already included in cost per share.
@check_input(Rights)
def calc_rights_net_amounts(rights: DataFrame) -> DataFrame:
    net_amount = rights.exercised * rights.price
    net_amount_df: DataFrame = net_amount.to_frame(name="net_amount")

    return net_amount_df


# Calculate positions at a given date by processing all trades along with all
# corporate actions.
@check_input(Trades, "trades")
@check_input(Rights, "rights")
@check_input(Splits, "splits")
@check_input(Mergers, "mergers")
@check_input(SpinOffs, "spin_offs")
@check_input(StockDividends, "stock_dividends")
def calc_positions(
    date: date,
    trades: DataFrame,
    rights: DataFrame,
    splits: DataFrame,
    mergers: DataFrame,
    spin_offs: DataFrame,
    stock_dividends: DataFrame,
) -> DataFrame:
    events = concat_events(
        ("trade", trades.reset_index()),
        ("right", rights.reset_index()),
        ("split", splits.reset_index()),
        ("merger", mergers.reset_index()),
        ("spin_off", spin_offs.reset_index()),
        ("stock_dividend", stock_dividends.reset_index()),
    )
    filtered_events = filter_by_date(events=events, date=date)
    positions = Positions()

    for _, event in filtered_events.iterrows():
        fn = event_fn(event)
        fn(positions, event)

    return positions.to_df()
