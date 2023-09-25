import pandas as pd
from typing import cast
from pandera import check_output
from datetime import date, timedelta
from .schemas import PTAX
from urllib.parse import urlencode

_PTAX_URL = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
_PTAX_DATE_FORMAT = "'%m-%d-%Y'"
_PTAX_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
_PTAX_DECIMAL = ","
_PTAX_DTYPES = {"cotacaoCompra": float, "cotacaoVenda": float, "dataHoraCotacao": str}
_PTAX_COLUMNS = {
    "dataHoraCotacao": "date",
    "cotacaoCompra": "buying_rate",
    "cotacaoVenda": "selling_rate",
}


# To calculate the cost basis from USD to BRL for tax filing purposes, it is
# necessary to obtain the PTAX rates from the Brazilian Central Bank (BCB).
# These rates represent the official exchange rate between the US dollar and the
# Brazilian real and are used to determine the value of foreign assets and
# investments held by Brazilian taxpayers.
#
# This function returns PTAX rates for the specified date range. Holidays and
# weekends are filled with the last available rate.
#
# https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/documentacao
@check_output(PTAX)
def fetch_ptax_usd(start_date: date, end_date: date) -> pd.DataFrame:
    if start_date > end_date:
        raise ValueError("start_date must be less than or equal than end_date")

    # request an extra week of data to compensate for weekends and holidays that
    # may affect the start date
    req_start_date = start_date - timedelta(days=7)

    qs = urlencode(
        {
            "@dataInicial": req_start_date.strftime(_PTAX_DATE_FORMAT),
            "@dataFinalCotacao": end_date.strftime(_PTAX_DATE_FORMAT),
            "$format": "text/csv",
            "$orderby": "dataHoraCotacao",
        }
    )
    url = f"{_PTAX_URL}?{qs}"

    ptax = pd.read_csv(url, dtype=_PTAX_DTYPES, decimal=_PTAX_DECIMAL).rename(
        columns=_PTAX_COLUMNS, errors="raise"
    )
    ptax["date"] = pd.to_datetime(ptax.date, format=_PTAX_DATETIME_FORMAT).dt.normalize()

    # for some reason there are duplicated entries for 2023-01-31
    ptax = ptax.drop_duplicates(subset="date", keep="last")
    ptax = ptax.set_index("date")

    # slice the data frame to remove extra data
    # forward fill missing dates, like weekends and holidays with the last
    # available PTAX
    date_range_idx = pd.date_range(name="date", start=start_date, end=end_date, freq="D")
    ffill_ptax = ptax.reindex(date_range_idx, method="ffill")

    return ffill_ptax
