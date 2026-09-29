# pbi-mercados

Cuadro de mando de mercado de valores en Power BI, desarrollado con Claude y versionado en Git.

## Puesta en marcha

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/ingesta_yfinance.py          # genera data/precios.csv y data/tickers.csv
```

Abrir `App/Mercados.pbip` en Power BI Desktop y actualizar.
Si el repositorio está en otra ruta, cambiar el parámetro `RutaDatos` (Transformar datos → Administrar parámetros).

## Añadir valores

Añadir filas a `config/tickers.csv` (`Ticker,Grupo,Activo`), volver a ejecutar el script y actualizar el informe.

## Estructura

| Ruta | Contenido |
|---|---|
| `App/` | Proyecto Power BI (PBIP): modelo TMDL e informe PBIR |
| `scripts/` | Ingesta de datos |
| `config/` | Valores a descargar |
| `data/` | CSV generados (no versionados) |
| `CLAUDE.md` | Convenciones para trabajar con Claude |
| `CHANGELOG.md` | Historial de versiones |
