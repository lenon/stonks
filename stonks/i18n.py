SheetNamesMap = {
    "positions": "Posição",
    "trade_confirmations": "Notas de corretagem",
    "trades": "Negócios",
    "rights": "Subscrições",
    "splits": "Desdobramentos",
    "mergers": "Incorporações",
    "spin_offs": "Cisões",
    "stock_dividends": "Bonificações",
}

TableColumnsMap = {
    "positions": {
        "symbol": "Código",
        "quantity": "Quantidade",
        "cost": "Custo Total",
        "cost_per_share": "PM",
    },
    "trade_confirmations": {
        "date": "Data",
        "broker": "Corretora",
        "sales": "Vendas",
        "purchases": "Compras",
        "traded_volume": "Vol. Negociado",
        "clearing_fees": "Taxa de Liq.",
        "trading_fees": "Emolumentos",
        "brokerage_fees": "Corretagem",
        "income_tax": "IR",
        "costs": "Custos",
        "net_amount": "Total Líquido",
    },
    "trades": {
        "date": "Data",
        "broker": "Corretora",
        "symbol": "Código",
        "type": "Tipo",
        "quantity": "Quantidade",
        "price": "Preço",
        "amount": "Total",
        "costs": "Custos",
        "net_amount": "Total Líquido",
    },
    "rights": {
        "date": "Data",
        "broker": "Corretora",
        "symbol": "Código",
        "description": "Descrição",
        "start": "Início",
        "end": "Fim",
        "settlement": "Liquidação",
        "shares": "Quantidade",
        "exercised": "Exercido",
        "price": "Preço",
        "net_amount": "Valor Total",
        "issue_date": "Emissão",
    },
    "splits": {"date": "Data", "symbol": "Código", "ratio": "Proporção"},
    "mergers": {"date": "Data", "symbol": "Código", "acquirer": "Compradora", "ratio": "Proporção"},
    "spin_offs": {
        "date": "Data",
        "symbol": "Código",
        "new_company": "Novo Código",
        "ratio": "Proporção",
        "cost_basis": "Percentual Custo",
    },
    "stock_dividends": {
        "date": "Data",
        "symbol": "Código",
        "quantity": "Quantidade",
        "cost": "Custo",
    },
}

TableValuesMap = {"trades": {"type": {"C": "buy", "V": "sell"}}}
