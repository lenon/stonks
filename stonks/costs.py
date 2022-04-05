import numpy as np
import pandas as pd


# Calculate some columns that are not included in trade confirmations ("nota de
# corretagem" in Portuguese) and are required for other calculations.
def calc_confirmations_costs(confirmations):
    volume = confirmations.sells + confirmations.buys
    costs = confirmations.clearing_fees + confirmations.trading_fees + confirmations.brokerage_fees
    net_amount = confirmations.sells - confirmations.buys - costs

    return pd.concat(
        [volume, costs, net_amount], axis="columns", keys=["volume", "costs", "net_amount"]
    )


# Calculate pro rata costs for each trade. This is also not included in trade
# confirmations and is required to calculate the portfolio.
def calc_trades_costs(trades, confirmations):
    # trade confirmation has a one-to-many association with a trade, identified
    # by date and broker name
    trades_w_confirmations = trades.join(confirmations, on=["date", "broker"], rsuffix="_c")

    amount = trades_w_confirmations.quantity * trades_w_confirmations.price
    costs = (amount / trades_w_confirmations.volume * trades_w_confirmations.costs_c).round(2)

    # net amount for buys is principal amount + costs, while for sells it's
    # amount - costs
    costs_with_sign = costs * np.where(trades_w_confirmations.type == "buy", 1, -1)
    net_amount = amount + costs_with_sign

    return pd.concat(
        [amount, costs, net_amount], axis="columns", keys=["amount", "costs", "net_amount"]
    )


# Subscriptions net amount is the cost per share x quantity of exercised shares.
# Costs are already included in cost per share.
def calc_subscriptions_net_amounts(subscriptions):
    return pd.DataFrame().assign(net_amount=subscriptions.exercised * subscriptions.price)
