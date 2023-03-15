import pandas as pd
from pandera import check_output
from datetime import date
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


# Get PTAX rates from BCB (the Brazilian central bank). They are required to
# calculate cost basis from USD to BRL, which is required for tax filing.
#
# https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/documentacao
@check_output(PTAX)
def ptax_usd(start_date: date, end_date: date) -> pd.DataFrame:
    qs = urlencode(
        {
            "@dataInicial": start_date.strftime(_PTAX_DATE_FORMAT),
            "@dataFinalCotacao": end_date.strftime(_PTAX_DATE_FORMAT),
            "$format": "text/csv",
            "$orderby": "dataHoraCotacao",
        }
    )
    url = f"{_PTAX_URL}?{qs}"

    df = pd.read_csv(url, dtype=_PTAX_DTYPES, decimal=_PTAX_DECIMAL).rename(columns=_PTAX_COLUMNS)
    df["date"] = pd.to_datetime(df["date"], format=_PTAX_DATETIME_FORMAT).dt.normalize()

    # for some reason there are duplicated entries for 2023-01-31
    return df.drop_duplicates(subset="date", keep="last").set_index("date")
