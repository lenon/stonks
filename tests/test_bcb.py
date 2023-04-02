import vcr
import pandas as pd
from pandas import to_datetime as dt
from datetime import date
from stonks.bcb import ptax_usd
from pandas.testing import assert_frame_equal


def test_ptax_usd():
    with vcr.use_cassette("tests/fixtures/vcr_cassettes/ptax_usd.yaml"):
        start_date = date(2023, 1, 1)
        end_date = date(2023, 2, 1)
        results = ptax_usd(start_date=start_date, end_date=end_date)

        expected = (
            pd.DataFrame(
                [
                    {"date": dt("2023-01-02"), "buying_rate": 5.3430, "selling_rate": 5.3436},
                    {"date": dt("2023-01-03"), "buying_rate": 5.3753, "selling_rate": 5.3759},
                    {"date": dt("2023-01-04"), "buying_rate": 5.4453, "selling_rate": 5.4459},
                    {"date": dt("2023-01-05"), "buying_rate": 5.4020, "selling_rate": 5.4026},
                    {"date": dt("2023-01-06"), "buying_rate": 5.2849, "selling_rate": 5.2855},
                    {"date": dt("2023-01-07"), "buying_rate": 5.2849, "selling_rate": 5.2855},
                    {"date": dt("2023-01-08"), "buying_rate": 5.2849, "selling_rate": 5.2855},
                    {"date": dt("2023-01-09"), "buying_rate": 5.2961, "selling_rate": 5.2967},
                    {"date": dt("2023-01-10"), "buying_rate": 5.2389, "selling_rate": 5.2395},
                    {"date": dt("2023-01-11"), "buying_rate": 5.2014, "selling_rate": 5.2020},
                    {"date": dt("2023-01-12"), "buying_rate": 5.1394, "selling_rate": 5.1400},
                    {"date": dt("2023-01-13"), "buying_rate": 5.1140, "selling_rate": 5.1146},
                    {"date": dt("2023-01-14"), "buying_rate": 5.1140, "selling_rate": 5.1146},
                    {"date": dt("2023-01-15"), "buying_rate": 5.1140, "selling_rate": 5.1146},
                    {"date": dt("2023-01-16"), "buying_rate": 5.1109, "selling_rate": 5.1115},
                    {"date": dt("2023-01-17"), "buying_rate": 5.1197, "selling_rate": 5.1203},
                    {"date": dt("2023-01-18"), "buying_rate": 5.0903, "selling_rate": 5.0909},
                    {"date": dt("2023-01-19"), "buying_rate": 5.2138, "selling_rate": 5.2144},
                    {"date": dt("2023-01-20"), "buying_rate": 5.1980, "selling_rate": 5.1986},
                    {"date": dt("2023-01-21"), "buying_rate": 5.1980, "selling_rate": 5.1986},
                    {"date": dt("2023-01-22"), "buying_rate": 5.1980, "selling_rate": 5.1986},
                    {"date": dt("2023-01-23"), "buying_rate": 5.1916, "selling_rate": 5.1922},
                    {"date": dt("2023-01-24"), "buying_rate": 5.1690, "selling_rate": 5.1696},
                    {"date": dt("2023-01-25"), "buying_rate": 5.1036, "selling_rate": 5.1042},
                    {"date": dt("2023-01-26"), "buying_rate": 5.0945, "selling_rate": 5.0951},
                    {"date": dt("2023-01-27"), "buying_rate": 5.0761, "selling_rate": 5.0767},
                    {"date": dt("2023-01-28"), "buying_rate": 5.0761, "selling_rate": 5.0767},
                    {"date": dt("2023-01-29"), "buying_rate": 5.0761, "selling_rate": 5.0767},
                    {"date": dt("2023-01-30"), "buying_rate": 5.0953, "selling_rate": 5.0959},
                    {"date": dt("2023-01-31"), "buying_rate": 5.0987, "selling_rate": 5.0993},
                    {"date": dt("2023-02-01"), "buying_rate": 5.0715, "selling_rate": 5.0721},
                ],
            )
            .set_index("date")
            .asfreq("D")
        )

        assert_frame_equal(results, expected)
