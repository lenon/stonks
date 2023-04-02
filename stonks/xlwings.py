import xlwings as xw  # type: ignore
from .bcb import ptax_usd
from typing import Generator
from .excel import Workbook
from contextlib import contextmanager
from .calculations import (
    calc_positions,
    calc_us_trades,
    calc_trades_costs,
    calc_us_positions,
    calc_rights_amounts,
    calc_trade_confirmations_costs,
)


@contextmanager
def _update_table(table_name: str) -> Generator[Workbook, None, None]:
    wb = Workbook(xw.Book.caller())
    table = getattr(wb, table_name)

    table.set_message("Working...")

    try:
        yield (wb)
        table.set_message("")
    except Exception as e:
        table.set_message(f"error: {e}")


def on_positions_date_update() -> None:
    with _update_table("positions") as wb:
        positions = calc_positions(
            date=wb.positions.date_input_value("date"),
            trades=wb.trades.to_df(),
            rights=wb.rights.to_df(),
            splits=wb.splits.to_df(),
            mergers=wb.mergers.to_df(),
            spin_offs=wb.spin_offs.to_df(),
            stock_dividends=wb.stock_dividends.to_df(),
        )
        wb.positions.replace_with_df(positions)


def on_us_positions_date_update() -> None:
    with _update_table("us_positions") as wb:
        us_positions = calc_us_positions(
            date=wb.us_positions.date_input_value("date"),
            trades=wb.us_trades.to_df(),
        )
        wb.us_positions.replace_with_df(us_positions)


def on_trade_confirmations_update() -> None:
    with _update_table("trade_confirmations") as wb:
        trade_confirmations_costs = calc_trade_confirmations_costs(wb.trade_confirmations.to_df())
        wb.trade_confirmations.update_from_df(trade_confirmations_costs)


def on_trades_update() -> None:
    with _update_table("trades") as wb:
        trades_costs = calc_trades_costs(wb.trades.to_df(), wb.trade_confirmations.to_df())
        wb.trades.update_from_df(trades_costs)


def on_rights_update() -> None:
    with _update_table("rights") as wb:
        rights_amounts = calc_rights_amounts(wb.rights.to_df())
        wb.rights.update_from_df(rights_amounts)


def on_ptax_dates_update() -> None:
    with _update_table("ptax") as wb:
        ptax_usd_df = ptax_usd(
            start_date=wb.ptax.date_input_value("start_date"),
            end_date=wb.ptax.date_input_value("end_date"),
        )
        wb.ptax.replace_with_df(ptax_usd_df, index=True)


def on_us_trades_update() -> None:
    with _update_table("us_trades") as wb:
        us_trades_ptax = calc_us_trades(trades=wb.us_trades.to_df(), ptax=wb.ptax.to_df())
        wb.us_trades.update_from_df(us_trades_ptax)
