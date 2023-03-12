from typing import Any


# Expects ratio to be expressed as A:B and to have comma (,) as decimal separator.
def ratio_to_float(ratio: str) -> float:
    a, b = [float(term.replace(",", ".")) for term in ratio.split(":")]
    return a / b


def reverse_dict(d: dict[str, str]) -> dict[str, str]:
    return {v: k for k, v in d.items()}
