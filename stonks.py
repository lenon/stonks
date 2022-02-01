from stonks.positions import calc_positions
import argparse

parser = argparse.ArgumentParser(description="Calculate current stocks portfolio")

parser.add_argument(
    "File",
    metavar="file",
    type=str,
    help="the Excel file that contains confirmations, trades and other corporate actions",
)

args = parser.parse_args()
input_file = args.File

calc_positions(input_file)
