import argparse
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

calc_positions(input_file)
