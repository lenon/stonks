from pathlib import Path


# Expects ratio to be expressed as A:B and to have comma (,) as decimal separator.
def ratio_to_float(ratio):
    a, b = [float(term.replace(",", ".")) for term in ratio.split(":")]
    return a / b


def columns_to_snake_case(name):
    return name.lower().replace(" ", "_")


def columns_to_title_case(name):
    return name.replace("_", " ").capitalize()


def positions_output_path(input_path):
    input_path = Path(input_path)
    return input_path.parent.joinpath(f"{input_path.stem}-positions.xlsx")
