from datetime import date, datetime
from functools import cached_property

import xlwings as xw  # type: ignore
from pandas import DataFrame

from stonks.mapping import SHEET_NAMES, TABLE_COLUMNS, TABLE_INDEXES, TABLE_VALUES

from .utils import reverse_dict


class Workbook:
    def __init__(self, wb: xw.Book):
        self._wb = wb

    def _table(self, name: str) -> "Table":
        sheet = self._wb.sheets[SHEET_NAMES[name]]
        table = sheet.tables[name]
        table_col_map = TABLE_COLUMNS[name]
        table_values_map = TABLE_VALUES.get(name, {})
        index = TABLE_INDEXES.get(name, [])

        return Table(self._wb, sheet, table, index, table_col_map, table_values_map)

    @cached_property
    def positions(self) -> "Table":
        return self._table("positions")

    @cached_property
    def trade_confirmations(self) -> "Table":
        return self._table("trade_confirmations")

    @cached_property
    def trades(self) -> "Table":
        return self._table("trades")

    @cached_property
    def rights(self) -> "Table":
        return self._table("rights")

    @cached_property
    def splits(self) -> "Table":
        return self._table("splits")

    @cached_property
    def mergers(self) -> "Table":
        return self._table("mergers")

    @cached_property
    def spin_offs(self) -> "Table":
        return self._table("spin_offs")

    @cached_property
    def stock_dividends(self) -> "Table":
        return self._table("stock_dividends")

    @cached_property
    def ptax(self) -> "Table":
        return self._table("ptax")

    @cached_property
    def us_trades(self) -> "Table":
        return self._table("us_trades")

    @cached_property
    def us_positions(self) -> "Table":
        return self._table("us_positions")

    @cached_property
    def us_dividends(self) -> "Table":
        return self._table("us_dividends")


class Table:
    def __init__(
        self,
        wb: xw.Book,
        sheet: xw.Sheet,
        table: xw.main.Table,
        index: list[str],
        col_map: dict[str, str],
        val_map: dict[str, dict[str, str]],
    ):
        self._wb = wb
        self._sheet = sheet
        self._table = table
        self._index = index
        self._col_map = col_map
        self._val_map = val_map

    def _cell(self, name: str) -> xw.Range:
        return self._sheet.range(name)

    def set_message(self, message: str) -> None:
        self._cell("message_box").value = message

    def date_input_value(self, name: str) -> date:
        value: datetime = self._cell(name).value
        return value.date()

    def to_df(self) -> DataFrame:
        headers = self._table.header_row_range.options(ndim=1).value
        # ndim=2 to force .value to return 2-dimensional list when table
        # contains a single row
        data = self._table.data_body_range.options(ndim=2).value

        df = DataFrame(data, columns=headers).rename(
            columns=reverse_dict(self._col_map), errors="raise"
        )

        if self._index:
            df.set_index(self._index, inplace=True)

        if self._val_map:
            df.replace(self._val_map, inplace=True)

        return df

    def update_from_df(self, df: DataFrame) -> None:
        renamed_df = df.rename(columns=self._col_map)

        with self._wb.app.properties(enable_events=False, screen_updating=False):
            # update only the columns included in the dataframe to avoid changing
            # any other data
            for column_name in renamed_df.columns:
                range = self._sheet.range(f"{self._table.name}[{column_name}]")
                range.options(index=False, header=False).value = renamed_df[column_name]

    def replace_with_df(self, df: DataFrame, index: bool = False) -> None:
        renamed_df = df.rename(columns=self._col_map)

        if index:
            renamed_df.rename_axis(index=self._col_map, inplace=True)

        with self._wb.app.properties(enable_events=False, screen_updating=False):
            self._table.update(renamed_df, index=index)
