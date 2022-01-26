import pandas as pd
from stonks.events import concat_dfs


def test_concat_dfs(
    trades_with_costs, subscriptions_with_net_amount, splits, mergers, spinoffs, events
):
    result = concat_dfs(
        ["trade", trades_with_costs.reset_index()],
        ["subscription", subscriptions_with_net_amount],
        ["split", splits],
        ["merger", mergers],
        ["spinoff", spinoffs],
    )

    pd.testing.assert_frame_equal(result, events)
