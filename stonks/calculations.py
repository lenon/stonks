import numpy as np
import pandas as pd
from pandas import DataFrame
from pandera import check_input, check_output
from .events import event_fn, concat_events, filter_by_date
from datetime import date
from .schemas import (
    PTAX,
    Rights,
    Splits,
    Trades,
    Mergers,
    SpinOffs,
    USTrades,
    RightsPreCalc,
    TradesPreCalc,
    StockDividends,
    USTradesPreCalc,
    RightsCalcResult,
    TradesCalcResult,
    TradeConfirmations,
    USTradesCalcResult,
    PositionsCalcResult,
    USPositionsCalcResult,
    TradeConfirmationsPreCalc,
    TradeConfirmationsCalcResult,
)
from .positions import Positions


# Trade confirmation is a document that confirms the details of a trade, such as
# the security traded, the price, and the quantity. This function calculates
# some columns required for other calculations below.
#
# Traded volume: is the total value of the securities traded.
# Costs: is the sum of clearing, trading and brokerage fees.
# Amount: the difference between sales and purchases and costs.
@check_input(TradeConfirmationsPreCalc)
@check_output(TradeConfirmationsCalcResult)
def calc_trade_confirmations_costs(trade_confirmations: DataFrame) -> DataFrame:
    traded_volume = trade_confirmations.sales + trade_confirmations.purchases
    costs = (
        trade_confirmations.clearing_fees
        + trade_confirmations.trading_fees
        + trade_confirmations.brokerage_fees
    )
    amount = trade_confirmations.sales - trade_confirmations.purchases - costs

    return pd.concat(
        [traded_volume, costs, amount],
        axis="columns",
        keys=["traded_volume", "costs", "amount"],
    )


# Calculate pro rata costs for each trade included in a trade confirmation.
#
# Amount: is the quantity of the traded security x price.
# Costs: pro rata costs based on the amount of the traded security.
# Amount: the amount of traded security + any costs.
@check_input(TradesPreCalc, "trades")
@check_input(TradeConfirmations, "trade_confirmations")
@check_output(TradesCalcResult)
def calc_trades_costs(trades: DataFrame, trade_confirmations: DataFrame) -> DataFrame:
    # The trade confirmation has a one-to-many association with trades, meaning
    # that a single trade confirmation has one or more trades.
    trades_w_confirmations = trades.join(trade_confirmations, on=["date", "broker"], rsuffix="_c")

    amount = trades_w_confirmations.quantity * trades_w_confirmations.price
    costs = (amount / trades_w_confirmations.traded_volume * trades_w_confirmations.costs_c).round(
        2
    )

    # amount with costs for buys is principal amount + costs, while for sells it's
    # amount - costs
    costs_with_sign = costs * np.where(trades_w_confirmations.type == "buy", 1, -1)
    amount_with_costs = amount + costs_with_sign

    return pd.concat([costs, amount_with_costs], axis="columns", keys=["costs", "amount"])


# Rights amount is the cost per share x quantity of exercised shares.
# Costs are already included in cost per share.
@check_input(RightsPreCalc)
@check_output(RightsCalcResult)
def calc_rights_amounts(rights: DataFrame) -> DataFrame:
    amount = rights.exercised * rights.price
    amount_df: DataFrame = amount.to_frame(name="amount")

    return amount_df


# Calculate positions at a given date by processing all trades along with all
# corporate actions.
@check_input(Trades, "trades")
@check_input(Rights, "rights")
@check_input(Splits, "splits")
@check_input(Mergers, "mergers")
@check_input(SpinOffs, "spin_offs")
@check_input(StockDividends, "stock_dividends")
@check_output(PositionsCalcResult)
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

    return positions.to_df().reset_index()


# Calculate PTAX, price and amount in BRL for US trades.
@check_input(USTradesPreCalc, "trades")
@check_input(PTAX, "ptax")
@check_output(USTradesCalcResult)
def calc_us_trades(trades: DataFrame, ptax: DataFrame) -> DataFrame:
    # forward fill missing dates, like weekends and holidays with the last
    # available PTAX
    ptax_idx = pd.date_range(min(ptax.index), max(ptax.index))
    ptax_bfilled = ptax.reindex(ptax_idx).ffill(axis="rows")

    trades_with_ptax = trades.join(ptax_bfilled.selling_rate, on=["date"])

    # for some reason the price per share informed by my broker's transaction
    # history is incorrect by a few pennies for DRIP transactions, so we need to
    # recalculate the correct price
    price_adjusted = trades_with_ptax.amount / trades_with_ptax.quantity

    costs = trades_with_ptax.commission + trades_with_ptax.reg_fee

    # calculate the amount in BRL for tax purposes
    price_brl = (trades_with_ptax.selling_rate * price_adjusted).round(2)
    amount_brl = (trades_with_ptax.selling_rate * trades_with_ptax.amount).round(2)

    return pd.concat(
        [costs, trades_with_ptax.selling_rate, price_brl, amount_brl],
        axis="columns",
        keys=["costs", "ptax", "price_brl", "amount_brl"],
    )


_EVENT_WITHOUT_BRL_SUFFIX = {
    "price": "price_usd",
    "amount": "amount_usd",
    "price_brl": "price",
    "amount_brl": "amount",
}


# Calculate positions at a given date by processing all trades along with all
# corporate actions.
@check_input(USTrades, "trades")
@check_output(USPositionsCalcResult)
def calc_us_positions(
    date: date,
    trades: DataFrame,
) -> DataFrame:
    events = concat_events(
        ("trade", trades.reset_index()),
    )

    filtered_events = filter_by_date(events=events, date=date)
    positions = Positions()
    positions_brl = Positions()

    # calculate positions in the original currency (USD) and in BRL for tax
    # purposes
    for _, event in filtered_events.iterrows():
        fn = event_fn(event)
        fn(positions, event)
        # rename columns with the names that event functions expect (without the _brl suffix)
        fn(positions_brl, event.rename(_EVENT_WITHOUT_BRL_SUFFIX, errors="raise"))

    # join BRL details with the positions df and drop duplicated columns
    positions_df = positions.to_df()
    positions_brl_df = positions_brl.to_df()
    joined_positions = positions_df.join(positions_brl_df, on="symbol", rsuffix="_brl").drop(
        columns=["quantity_brl"]
    )

    return joined_positions.reset_index()
