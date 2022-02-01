import pandas as pd
from .utils import columns_to_snake_case, columns_to_title_case
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

_BRL_FORMAT = '_(R$* #,##0.00_);_(R$* (#,##0.00);_(R$* "-"??_);_(@_)'


def read_sheet(xlsx, sheet_name):
    return pd.read_excel(xlsx, sheet_name=sheet_name).rename(columns=columns_to_snake_case)


def save_as_excel(positions, output_path):
    wb = Workbook()
    ws = wb.active
    ws.title = "positions"

    df = (
        positions.rename(columns=columns_to_title_case)
        .sort_index()
        .round(2)
        .reset_index()
        .rename(columns={"index": "Symbol"})
    )

    for r in dataframe_to_rows(df, index=False):
        ws.append(r)

    for cell in ws["C"]:
        cell.number_format = _BRL_FORMAT

    for cell in ws["D"]:
        cell.number_format = _BRL_FORMAT

    ws.column_dimensions["C"].width = 15
    ws.column_dimensions["D"].width = 15

    wb.save(output_path)
