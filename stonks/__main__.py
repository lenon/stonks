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


positions, confirmations, trades, subscriptions, splits, mergers, spinoffs, events = calc_positions(
    input_file
)

wb = Workbook(input_file)

ws = wb.add_sheet("positions", positions)
ws.format_as_brl("Cost")
ws.format_as_brl("Cost per share")
ws.set_column_width("Cost", 13)
ws.set_column_width("Cost per share", 13)

ws = wb.add_sheet("confirmations", confirmations.reset_index())
ws.format_as_date("Date")
ws.format_as_brl("Sells")
ws.format_as_brl("Buys")
ws.format_as_brl("Clearing fees")
ws.format_as_brl("Trading fees")
ws.format_as_brl("Brokerage fees")
ws.format_as_brl("Income tax")
ws.format_as_brl("Volume")
ws.format_as_brl("Costs")
ws.format_as_brl("Net amount")

ws.set_column_width("Date", 10)
ws.set_column_width("Buys", 13)
ws.set_column_width("Sells", 13)
ws.set_column_width("Clearing fees", 13)
ws.set_column_width("Trading fees", 13)
ws.set_column_width("Brokerage fees", 13)
ws.set_column_width("Income tax", 10)
ws.set_column_width("Volume", 13)
ws.set_column_width("Costs", 10)
ws.set_column_width("Net amount", 13)

wb.save()
