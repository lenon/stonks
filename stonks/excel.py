from .utils import columns_to_title_case, positions_output_path
from openpyxl import Workbook as Wb
from openpyxl.utils.dataframe import dataframe_to_rows


class Sheet:
    _BRL_FORMAT = '_-"R$"\ * #,##0.00_-;\-"R$"\ * #,##0.00_-;_-"R$"\ * "-"??_-;_-@_-'
    _DATE_FORMAT = "dd/mm/yy"

    def __init__(self, ws):
        self._ws = ws

    def _find_column_by_name(self, name):
        header = next(self._ws.rows)
        cell = next(cell for cell in header if cell.value == name)

        return cell.column_letter

    def format_as_brl(self, column_name):
        column_letter = self._find_column_by_name(column_name)

        for cell in self._ws[column_letter]:
            cell.number_format = self._BRL_FORMAT

    def format_as_date(self, column_name):
        column_letter = self._find_column_by_name(column_name)

        for cell in self._ws[column_letter]:
            cell.number_format = self._DATE_FORMAT

    def set_column_width(self, column_name, width):
        column_letter = self._find_column_by_name(column_name)
        self._ws.column_dimensions[column_letter].width = width


class Workbook:
    def __init__(self, input_path):
        self._output_path = positions_output_path(input_path)
        self._wb = Wb()

    def add_sheet(self, name, df):
        ws = self._wb.create_sheet(name)
        df = df.rename(columns=columns_to_title_case)

        for r in dataframe_to_rows(df, index=False):
            ws.append(r)

        return Sheet(ws)

    def save(self):
        self._wb.save(self._output_path)
