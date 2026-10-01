"""Stáhne aktuální ceny pozic z portfolio.csv a uloží snapshot hodnoty portfolia."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import pandas as pd  # noqa: E402
import yfinance as yf  # noqa: E402

from shared.lib import excel_io  # noqa: E402
from shared.lib.repo import data_dir, dated, temp_dir  # noqa: E402

PROJECT = "stocks-tracker"


def fetch_price(ticker: str) -> float | None:
    """Poslední známá zavírací cena, nebo None když ji nelze získat."""
    try:
        hist = yf.Ticker(ticker).history(period="5d")
    except Exception as exc:  # síť, neznámý ticker
        print(f"  ! {ticker}: {exc}")
        return None
    if hist.empty:
        return None
    return float(hist["Close"].iloc[-1])


def main() -> None:
    data = data_dir(PROJECT)
    portfolio = pd.read_csv(data / "portfolio.csv")

    prices, missing = [], []
    for ticker in portfolio["ticker"]:
        price = fetch_price(ticker)
        if price is None:
            missing.append(ticker)
        prices.append(price)

    portfolio["price"] = prices
    portfolio["value"] = portfolio["price"] * portfolio["shares"]
    portfolio["cost"] = portfolio["buy_price"] * portfolio["shares"]
    portfolio["pnl"] = portfolio["value"] - portfolio["cost"]
    portfolio["pnl_pct"] = (portfolio["pnl"] / portfolio["cost"] * 100).round(2)

    out_dir = temp_dir(PROJECT) / "snapshots"
    out_dir.mkdir(exist_ok=True)
    out = excel_io.write_new(portfolio, out_dir / dated("snapshot", ".xlsx"), "Portfolio")

    # Součty jen po měnách — míchat CZK a USD bez kurzu nedává smysl.
    print("\nHodnota podle měny:")
    for currency, group in portfolio.dropna(subset=["value"]).groupby("currency"):
        print(f"  {currency}: {group['value'].sum():,.2f}  (P/L {group['pnl'].sum():+,.2f})")

    if missing:
        print(f"\n! Cena se nepodařila získat pro: {', '.join(missing)}")
        print("  Tyto pozice nejsou v součtech zahrnuty.")

    print(f"\nSnapshot uložen: {out}")


if __name__ == "__main__":
    main()
