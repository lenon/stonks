import pandas as pd
from pprint import pprint


def concat_dfs(*dfs):
    events = [df.assign(event=event) for event, df in dfs]

    return pd.concat(events).sort_values(by="date", ignore_index=True)
