from stonks.utils import ratio_to_float, columns_to_snake_case, columns_to_title_case


def test_ratio_to_float():
    assert ratio_to_float("1:1") == 1
    assert ratio_to_float("4:1") == 4
    assert ratio_to_float("1:4") == 0.25
    assert ratio_to_float("1,25:1") == 1.25
    assert ratio_to_float("1:1,25") == 0.8


def test_columns_to_snake_case():
    assert columns_to_snake_case("My Column") == "my_column"
    assert columns_to_snake_case("my_column") == "my_column"


def test_columns_to_title_case():
    assert columns_to_title_case("My Column") == "My column"
    assert columns_to_title_case("my_column") == "My column"
