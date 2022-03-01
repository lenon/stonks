import argparse
from .excel import Workbook
from .positions import calc_positions

parser = argparse.ArgumentParser(description="Calculate current stocks portfolio")

parser.add_argument(
    "File",
    metavar="file",
    type=str,
    help="the Excel file that contains confirmations, trades and other corporate actions",
)

args = parser.parse_args()
input_file = args.File

positions = calc_positions(input_file)

wb = Workbook(input_file)

ws = wb.add_sheet("positions", positions)
ws.format_as_brl("Cost")
ws.format_as_brl("Cost per share")
ws.set_column_width("Cost", 15)
ws.set_column_width("Cost per share", 15)

wb.save()
