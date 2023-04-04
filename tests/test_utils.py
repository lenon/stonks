from datetime import date
from stonks.utils import reverse_dict, ratio_to_float, previous_month_15th


def test_ratio_to_float():
    assert ratio_to_float("1:1") == 1
    assert ratio_to_float("4:1") == 4
    assert ratio_to_float("1:4") == 0.25
    assert ratio_to_float("1,25:1") == 1.25
    assert ratio_to_float("1:1,25") == 0.8


def test_reverse_dict():
    assert reverse_dict({"a": "b", "c": "d"}) == {"b": "a", "d": "c"}


def test_previous_month_15th():
    assert previous_month_15th(date(2022, 1, 1)) == date(2021, 12, 15)
    assert previous_month_15th(date(2022, 1, 15)) == date(2021, 12, 15)
    assert previous_month_15th(date(2022, 1, 31)) == date(2021, 12, 15)
    assert previous_month_15th(date(2022, 2, 28)) == date(2022, 1, 15)
    assert previous_month_15th(date(2022, 12, 31)) == date(2022, 11, 15)
