from datetime import date, timedelta


# Expects ratio to be expressed as A:B and to have comma (,) as decimal separator.
def ratio_to_float(ratio: str) -> float:
    a, b = (float(term.replace(",", ".")) for term in ratio.split(":"))
    return a / b


def reverse_dict(d: dict[str, str]) -> dict[str, str]:
    return {v: k for k, v in d.items()}


def previous_month_15th(date: date) -> date:
    # change the date to 1st of the month then subtract 1 day and we get the
    # previous month
    previous_month = date.replace(day=1) - timedelta(days=1)

    # calculate the 15th day of the previous month
    previous_month_15th = previous_month.replace(day=15)

    return previous_month_15th
