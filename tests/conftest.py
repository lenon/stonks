from pytest import fixture
from pandas import DataFrame, to_datetime as dt


def df_from_list(list):
    columns = list[0:1][0]
    data = list[1:]

    return DataFrame(data, columns=columns)


@fixture
def confirmations():
    return df_from_list(
        [
            # fmt: off
            ["date",          "broker", "sells", "buys", "clearing_fees", "trading_fees", "brokerage_fees", "income_tax"],
            [dt("2022-01-01"), "Acme",  0,       1000,   2.5,             0.5,            1,                0],
            [dt("2022-01-02"), "Acme",  0,       1100,   3,               0.6,            1,                0],
            [dt("2022-01-03"), "Acme",  500,     750,    5,               1,              1,                0.5],
            [dt("2022-01-04"), "Acme",  0,       500,    0.5,             0.5,            1,                0],
            # fmt: on
        ]
    ).set_index(["date", "broker"])


@fixture
def confirmations_with_volume_and_costs():
    return df_from_list(
        [
            # fmt: off
            ["date",          "broker", "sells", "buys", "clearing_fees", "trading_fees", "brokerage_fees", "income_tax", "volume", "costs", "net_amount"],
            [dt("2022-01-01"), "Acme",  0,       1000,   2.5,             0.5,            1,                0,            1000,     4,       -1004],
            [dt("2022-01-02"), "Acme",  0,       1100,   3,               0.6,            1,                0,            1100,     4.6,     -1104.6],
            [dt("2022-01-03"), "Acme",  500,     750,    5,               1,              1,                0.5,          1250,     7,       -257],
            [dt("2022-01-04"), "Acme",  0,       500,    0.5,             0.5,            1,                0,            500,      2,       -502],
            # fmt: on
        ]
    ).set_index(["date", "broker"])


@fixture
def trades():
    return df_from_list(
        [
            # fmt: off
            ["date",          "broker", "symbol", "type", "quantity", "price"],
            [dt("2022-01-01"), "Acme",  "ABC3",   "buy",  100,        10],
            [dt("2022-01-02"), "Acme",  "DEF3",   "buy",  100,        11],
            [dt("2022-01-03"), "Acme",  "ABC3",   "sell", 100,        5],
            [dt("2022-01-03"), "Acme",  "DEF3",   "buy",  125,        6],
            [dt("2022-01-04"), "Acme",  "DEF3",   "buy",  100,        5],
            # fmt: on
        ],
    ).set_index(["date", "broker"])


@fixture
def trades_with_costs():
    return df_from_list(
        [
            # fmt: off
            ["date",          "broker", "symbol", "type", "quantity", "price", "amount", "costs", "net_amount"],
            [dt("2022-01-01"), "Acme",  "ABC3",   "buy",  100,        10,      1000,     4.0,     1004.0],
            [dt("2022-01-02"), "Acme",  "DEF3",   "buy",  100,        11,      1100,     4.6,     1104.6],
            [dt("2022-01-03"), "Acme",  "ABC3",   "sell", 100,        5,       500,      2.8,     497.2],
            [dt("2022-01-03"), "Acme",  "DEF3",   "buy",  125,        6,       750,      4.2,     754.2],
            [dt("2022-01-04"), "Acme",  "DEF3",   "buy",  100,        5,       500,      2.0,     502.0],
            # fmt: on
        ],
    ).set_index(["date", "broker"])


@fixture
def subscriptions():
    return df_from_list(
        [
            # fmt: off
            ["date",           "broker", "symbol", "description", "start",          "end",            "settlement",     "shares", "exercised", "price", "issue_date"],
            [dt("2022-01-01"), "Acme",   "ABC3",   "4th subs",    dt("2022-01-01"), dt("2022-01-02"), dt("2022-01-03"), 100,      90,          50.1,    dt("2022-01-10")],
            [dt("2022-02-01"), "Acme",   "ABC3",   "5th subs",    dt("2022-02-01"), dt("2022-02-02"), dt("2022-02-03"), 50,       50,          10.5,    dt("2022-02-10")],
            # fmt: on
        ],
    )


@fixture
def subscriptions_with_net_amount():
    return df_from_list(
        [
            # fmt: off
            ["date",           "broker", "symbol", "description", "start",          "end",            "settlement",     "shares", "exercised", "price", "issue_date",     "net_amount"],
            [dt("2022-01-01"), "Acme",   "ABC3",   "4th subs",    dt("2022-01-01"), dt("2022-01-02"), dt("2022-01-03"), 100,      90,          50.1,    dt("2022-01-10"), 4509.0],
            [dt("2022-02-01"), "Acme",   "ABC3",   "5th subs",    dt("2022-02-01"), dt("2022-02-02"), dt("2022-02-03"), 50,       50,          10.5,    dt("2022-02-10"), 525.0],
            # fmt: on
        ]
    )
