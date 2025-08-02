from datetime import date

import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from pandera.pandas import check_input, check_output

from .events import concat_events, event_fn, filter_by_date
from .positions import Positions
from .schemas import (
    PTAX,
    Mergers,
    PositionsCalcResult,
    Rights,
    RightsCalcResult,
    RightsPreCalc,
    SpinOffs,
    Splits,
    StockDividends,
    TradeConfirmations,
    TradeConfirmationsCalcResult,
    TradeConfirmationsPreCalc,
    Trades,
    TradesCalcResult,
    TradesPreCalc,
    USDividendsCalcResult,
    USDividendsPreCalc,
    USPositionsCalcResult,
    USTrades,
    USTradesCalcResult,
    USTradesPreCalc,
)
from .utils import previous_month_15th


# This function calculates some columns required for other calculations based on
# the input trade confirmations DataFrame.
#
# Trade confirmation is a document that confirms the details of a trade, such as
# the security traded, its price, and the traded quantity.
@check_input(TradeConfirmationsPreCalc)
@check_output(TradeConfirmationsCalcResult)
def calc_trade_confirmations_costs(trade_confirmations: DataFrame) -> DataFrame:
    # calculate traded volume by adding purchases and sales
    #
    # traded volume is the total value of the securities traded and is used to
    # calculate costs of a single trade
    traded_volume = trade_confirmations.sales + trade_confirmations.purchases
    # calculate costs by adding clearing, trading, and brokerage fees
    costs = (
        trade_confirmations.clearing_fees
        + trade_confirmations.trading_fees
        + trade_confirmations.brokerage_fees
    )
    # calculate amount by subtracting purchases, sales, and costs
    #
    # amount is the effective value that will be credited or debited in the
    # account
    amount = trade_confirmations.sales - trade_confirmations.purchases - costs

    return pd.concat(
        [traded_volume, costs, amount],
        axis="columns",
        keys=["traded_volume", "costs", "amount"],
    )


# Calculate pro rata costs for each trade included in a trade confirmation.
#
# Costs: .
# Amount: the amount of traded security + any costs.
@check_input(TradesPreCalc, "trades")
@check_input(TradeConfirmations, "trade_confirmations")
@check_output(TradesCalcResult)
def calc_trades_costs(trades: DataFrame, trade_confirmations: DataFrame) -> DataFrame:
    # the trade confirmation has a one-to-many association with trades, meaning
    # that a single trade confirmation has one or more trades
    trades_w_confirmations = trades.join(trade_confirmations, on=["date", "broker"], rsuffix="_c")

    # amount is the quantity of the traded security x price, so no costs
    amount = trades_w_confirmations.quantity * trades_w_confirmations.price
    # costs is the pro rata cost based on the amount of the traded security
    # rounding to 2 decimal places to match broker's calculations
    costs = (amount / trades_w_confirmations.traded_volume) * trades_w_confirmations.costs_c
    costs = costs.round(2)

    # amount is the principal amount of traded security + or - pro rata costs
    # it is the effective value that will be credited or debited
    # for purchases it is principal amount + costs
    # for sales it is principal amount - costs
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
        {
            "trade": trades,
            "right": rights,
            "split": splits,
            "merger": mergers,
            "spin_off": spin_offs,
            "stock_dividend": stock_dividends,
        }
    )
    filtered_events = filter_by_date(events=events, date=date)
    positions = Positions()

    for _, event in filtered_events.iterrows():
        fn = event_fn(event)
        fn(positions, event)

    # reset index to a sequential numeric index so it can be used to update
    # excel tables
    return positions.to_df().reset_index()


# Calculate PTAX, price and amount in BRL for US trades.
@check_input(USTradesPreCalc, "trades")
@check_input(PTAX, "ptax")
@check_output(USTradesCalcResult)
def calc_us_trades(trades: DataFrame, ptax: DataFrame) -> DataFrame:
    trades_with_ptax = trades.join(ptax.selling_rate, on=["date"])

    # for some reason the price per share informed in the transactions page
    # is incorrect by a few pennies for DRIP transactions but the amount is correct
    # so we need to recalculate the correct price per share using amount / quantity
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


def _map_brl_event(event: Series) -> Series:
    # remove the _brl suffix from event so it can be used with all functions
    # defined in events.py
    return event.drop(["price", "amount"]).rename(
        {"price_brl": "price", "amount_brl": "amount"}, errors="raise"
    )


# Calculate positions at a given date by processing all trades along with all
# corporate actions.
@check_input(USTrades, "trades")
@check_output(USPositionsCalcResult)
def calc_us_positions(
    date: date,
    trades: DataFrame,
) -> DataFrame:
    events = concat_events({"trade": trades})
    filtered_events = filter_by_date(events=events, date=date)

    positions = Positions()
    positions_brl = Positions()

    # calculate positions in the original currency (USD) and in BRL for tax
    # purposes
    for _, event in filtered_events.iterrows():
        fn = event_fn(event)
        fn(positions, event)
        fn(positions_brl, _map_brl_event(event))

    # remove duplicate quantity as it is the same in both dataframes
    positions_brl_df = positions_brl.to_df().drop(columns="quantity")
    # join BRL details with the positions dataframe
    joined_positions = positions.to_df().join(positions_brl_df, on="symbol", rsuffix="_brl")

    # reset index to a sequential numeric index so it can be used to update
    # excel tables
    return joined_positions.reset_index()


# Calculate PTAX, amount and taxes in BRL for US dividends.
@check_input(USDividendsPreCalc, "dividends")
@check_input(PTAX, "ptax")
@check_output(USDividendsCalcResult)
def calc_us_dividends(dividends: DataFrame, ptax: DataFrame) -> DataFrame:
    # dividends in USD must be converted into BRL using the PTAX for the last
    # business day of the first fortnight of the month prior to the dividend
    #
    # since PTAX missing dates are filled with ffill, we can use 15th of the
    # month without having to calculate business days
    ptax_dates = dividends.index.map(previous_month_15th)
    dividends_w_ptax = dividends.assign(ptax_date=ptax_dates).join(
        ptax.buying_rate, on=["ptax_date"]
    )

    total = dividends.amount - dividends.taxes
    amount_brl = (dividends.amount * dividends_w_ptax.buying_rate).round(2)
    taxes_brl = (dividends.taxes * dividends_w_ptax.buying_rate).round(2)
    total_brl = (total * dividends_w_ptax.buying_rate).round(2)

    return pd.concat(
        [total, dividends_w_ptax.buying_rate, amount_brl, taxes_brl, total_brl],
        axis="columns",
        keys=["total", "ptax", "amount_brl", "taxes_brl", "total_brl"],
    )
