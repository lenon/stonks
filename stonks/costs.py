import pandas as pd


# Calculate volume, costs and net amount since these values are not included in
# the confirmation (or "nota de corretagem").
def sum_confirmations_costs(confirmations):
    return confirmations.assign(
        volume=lambda c: c.sells + c.buys,
        costs=lambda c: c.clearing_fees + c.trading_fees + c.brokerage_fees,
        net_amount=lambda c: c.sells - c.buys - c.costs,
    )


# The net amount is also not included in the confirmation document, so here we
# calculate it for each trade. The "amount" value here is the principal amount,
# which is price x quantity. For buys it's principal amount + costs, for sells
# it's principal amount - costs.
def _calc_trade_net_amount(trades):
    return trades.apply(
        lambda t: t.amount + t.costs if t.type == "buy" else t.amount - t.costs,
        axis="columns",
    )


# Calculate amount, costs and net amount for each trade. A single trade has a
# relationship with only one confirmation entry, but a confirmation could have
# one or more trades.
def calc_trades_costs(confirmations, trades):
    conf_prefix = "c_"

    drop_conf_prefix = lambda t: t.drop(
        columns=t.columns[t.columns.str.startswith(conf_prefix)]
    )

    return (
        trades.join(confirmations.add_prefix(conf_prefix), on=["date", "broker"])
        .assign(
            amount=lambda t: t.quantity * t.price,
            costs=lambda t: (t.amount / t.c_volume * t.c_costs).round(2),
            net_amount=_calc_trade_net_amount,
        )
        .pipe(drop_conf_prefix)
    )


# Subscriptions net amount is the cost per share x quantity of exercised shares.
# Costs are already included in cost per share.
def calc_subscriptions_net_amounts(subscriptions):
    return subscriptions.assign(
        net_amount=subscriptions.exercised * subscriptions.price
    )
