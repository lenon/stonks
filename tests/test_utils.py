from stonks.utils import reverse_dict, ratio_to_float


def test_ratio_to_float():
    assert ratio_to_float("1:1") == 1
    assert ratio_to_float("4:1") == 4
    assert ratio_to_float("1:4") == 0.25
    assert ratio_to_float("1,25:1") == 1.25
    assert ratio_to_float("1:1,25") == 0.8


def test_reverse_dict():
    assert reverse_dict({"a": "b", "c": "d"}) == {"b": "a", "d": "c"}
