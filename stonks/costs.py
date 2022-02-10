import pandas as pd


# Calculate volume (sells + buys), costs (sum of all fees) and net amount (sells
# - buys - costs). These columns are not included in trade confirmations ("nota
# de corretagem" in Portuguese) and are required for other calculations.
def sum_confirmations_costs(confirmations):
    return confirmations.assign(
        volume=lambda c: c.sells + c.buys,
        costs=lambda c: c.clearing_fees + c.trading_fees + c.brokerage_fees,
        net_amount=lambda c: c.sells - c.buys - c.costs,
    )


# Calculate net amount for each trade, which is principal amount + costs for
# buys and principal amount - costs for sells.
def _calc_trade_net_amount(trades):
    return trades.apply(
        lambda t: t.amount + t.costs if t.type == "buy" else t.amount - t.costs,
        axis="columns",
    )


# Calculate amount (quantity x price), pro rata costs (amount / volume * total
# costs) and net amount for each trade. A trade confirmation has a one-to-many
# association with a trade, identified by date and broker name.
def calc_trades_costs(trades, confirmations):
    confirmations_prefix = "c_"
    confirmations_with_prefix = confirmations.add_prefix(confirmations_prefix)

    drop_confirmations_prefix = lambda t: t.drop(
        columns=t.columns[t.columns.str.startswith(confirmations_prefix)]
    )

    return (
        # join confirmations columns with a prefix to avoid overriding values
        # for columns with the same name
        trades.join(confirmations_with_prefix, on=["date", "broker"])
        .assign(
            amount=lambda t: t.quantity * t.price,
            costs=lambda t: (t.amount / t.c_volume * t.c_costs).round(2),
            net_amount=_calc_trade_net_amount,
        )
        .pipe(drop_confirmations_prefix)
    )


# Subscriptions net amount is the cost per share x quantity of exercised shares.
# Costs are already included in cost per share.
def calc_subscriptions_net_amounts(subscriptions):
    return subscriptions.assign(net_amount=subscriptions.exercised * subscriptions.price)
