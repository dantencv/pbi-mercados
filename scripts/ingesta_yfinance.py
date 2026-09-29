"""
Ingesta de cotizaciones diarias desde Yahoo Finance.

Lee la lista de valores de config/tickers.csv (solo filas con Activo = 1)
y genera en data/:
  - precios.csv  -> formato largo: una fila por Fecha y Ticker
  - tickers.csv  -> dimensión con nombre, sector, industria, moneda y tipo

Uso (desde la raíz del repositorio):
    python scripts/ingesta_yfinance.py
    python scripts/ingesta_yfinance.py --desde 2018-01-01
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import yfinance as yf

RAIZ = Path(__file__).resolve().parents[1]
CONFIG = RAIZ / "config" / "tickers.csv"
DATA = RAIZ / "data"

COLUMNAS_PRECIOS = ["Fecha", "Ticker", "Apertura", "Maximo", "Minimo",
                    "Cierre", "CierreAjustado", "Volumen", "Dividendos", "Splits",
                    "RentabilidadDiaria"]


def leer_config() -> pd.DataFrame:
    cfg = pd.read_csv(CONFIG, dtype={"Ticker": str, "Grupo": str})
    return cfg[cfg["Activo"] == 1].reset_index(drop=True)


def descargar_precios(ticker: str, desde: str) -> pd.DataFrame:
    hist = yf.Ticker(ticker).history(start=desde, auto_adjust=False, actions=True)
    if hist.empty:
        print(f"  ! {ticker}: sin datos")
        return pd.DataFrame(columns=COLUMNAS_PRECIOS)

    hist = hist.reset_index()
    hist["Date"] = pd.to_datetime(hist["Date"]).dt.tz_localize(None).dt.date
    hist = hist.rename(columns={
        "Date": "Fecha", "Open": "Apertura", "High": "Maximo", "Low": "Minimo",
        "Close": "Cierre", "Adj Close": "CierreAjustado", "Volume": "Volumen",
        "Dividends": "Dividendos", "Stock Splits": "Splits",
    })
    hist["Ticker"] = ticker
    # Rentabilidad diaria sobre el cierre ajustado (la primera sesión queda vacía)
    hist["RentabilidadDiaria"] = hist["CierreAjustado"].pct_change(fill_method=None)
    for col in COLUMNAS_PRECIOS:
        if col not in hist.columns:
            hist[col] = 0
    return hist[COLUMNAS_PRECIOS]


def descargar_info(ticker: str, grupo: str) -> dict:
    try:
        info = yf.Ticker(ticker).info or {}
    except Exception as exc:  # la API de info falla a veces; no debe romper la carga
        print(f"  ! {ticker}: info no disponible ({exc})")
        info = {}
    return {
        "Ticker": ticker,
        "Nombre": info.get("longName") or info.get("shortName") or ticker,
        "Grupo": grupo,
        # Los ETFs no tienen sector: se usa su categoría (p. ej. "Technology")
        "Sector": info.get("sector") or info.get("category") or "N/D",
        "Industria": info.get("industry", "N/D"),
        "Moneda": info.get("currency", "N/D"),
        "Tipo": info.get("quoteType", "N/D"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingesta Yahoo Finance -> CSV")
    parser.add_argument("--desde", default="2019-01-01", help="Fecha inicial (YYYY-MM-DD)")
    args = parser.parse_args()

    DATA.mkdir(exist_ok=True)
    cfg = leer_config()
    print(f"Descargando {len(cfg)} valores desde {args.desde}...")

    precios, dim = [], []
    for fila in cfg.itertuples(index=False):
        print(f"  - {fila.Ticker}")
        precios.append(descargar_precios(fila.Ticker, args.desde))
        dim.append(descargar_info(fila.Ticker, fila.Grupo))

    df_precios = pd.concat(precios, ignore_index=True).sort_values(["Ticker", "Fecha"])
    df_dim = pd.DataFrame(dim)

    # Formato estable (punto decimal, fechas ISO) para que Power Query no dependa del idioma de Windows
    df_precios.to_csv(DATA / "precios.csv", index=False, float_format="%.6f")
    df_dim.to_csv(DATA / "tickers.csv", index=False)

    print(f"OK: {len(df_precios):,} filas en data/precios.csv | {len(df_dim)} valores en data/tickers.csv")


if __name__ == "__main__":
    main()
