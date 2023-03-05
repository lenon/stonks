from pandas import read_csv
from pytest import fixture
from .helpers import fixture_path


@fixture
def confirmations_df():
    return read_csv(
        fixture_path("confirmations.csv"),
        parse_dates=["date"],
        index_col=["date", "broker"],
    )


@fixture
def confirmations_costs_df():
    return read_csv(
        fixture_path("confirmations-costs.csv"),
        parse_dates=["date"],
        index_col=["date", "broker"],
    )


@fixture
def confirmations_with_costs_df(confirmations_df, confirmations_costs_df):
    return confirmations_df.combine_first(confirmations_costs_df)


@fixture
def trades_df():
    return read_csv(
        fixture_path("trades.csv"),
        parse_dates=["date"],
        index_col=["date", "broker"],
    )


@fixture
def trades_costs_df():
    return read_csv(
        fixture_path("trades-costs.csv"),
        parse_dates=["date"],
        index_col=["date", "broker"],
    )


@fixture
def trades_with_costs_df(trades_df, trades_costs_df):
    return trades_df.combine_first(trades_costs_df)


@fixture
def subscriptions_df():
    return read_csv(
        fixture_path("subscriptions.csv"),
        parse_dates=["date", "start", "end", "settlement", "issue_date"],
    )


@fixture
def subscriptions_amounts_df():
    return read_csv(fixture_path("subscriptions-amounts.csv"))


@fixture
def subscriptions_with_amounts_df(subscriptions_df, subscriptions_amounts_df):
    return subscriptions_df.combine_first(subscriptions_amounts_df)


@fixture
def splits_df():
    return read_csv(
        fixture_path("splits.csv"),
        parse_dates=["date"],
    )


@fixture
def mergers_df():
    return read_csv(
        fixture_path("mergers.csv"),
        parse_dates=["date"],
    )


@fixture
def spinoffs_df():
    return read_csv(
        fixture_path("spinoffs.csv"),
        parse_dates=["date"],
    )


@fixture
def events_df():
    return read_csv(
        fixture_path("events.csv"),
        parse_dates=["date", "start", "end", "settlement", "issue_date"],
    )


@fixture
def events_filtered_df():
    return read_csv(
        fixture_path("events-filtered.csv"),
        dtype={"acquirer": object, "new_company": object},
        parse_dates=["date", "start", "end", "settlement", "issue_date"],
    )


@fixture
def positions_df():
    return read_csv(fixture_path("positions.csv"))
