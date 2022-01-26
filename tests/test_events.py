import pandas as pd
from stonks.events import concat_dfs


def test_concat_dfs(trades, subscriptions, splits, mergers, spinoffs, events):
    result = concat_dfs(
        ["trade", trades.reset_index()],
        ["subscription", subscriptions],
        ["split", splits],
        ["merger", mergers],
        ["spinoff", spinoffs],
    )

    pd.testing.assert_frame_equal(result, events)
