def ratio_to_float(ratio):
    # expects ratio to be expressed as A:B and to have comma (,) as decimal separator
    a, b = [float(term.replace(",", ".")) for term in ratio.split(":")]

    return a / b
