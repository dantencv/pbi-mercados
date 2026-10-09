# Changelog

Todos los cambios relevantes del cuadro de mando se documentan aquí.
Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y [versionado semántico](https://semver.org/lang/es/).

## [Sin publicar]

### Añadido
- Revisión automática del modelo con el Best Practice Analyzer (GitHub Actions) en cada PR.

### Cambiado
- Títulos de los visuales en azul oscuro (`#1F3864`).

### Corregido
- El gráfico de precios no tenía título: ahora se titula «Precio Cierre ajustado».
- `Rentabilidad Anualizada` usa `DIVIDE` en lugar del operador `/` (aviso del BPA).

## [1.1.0] - 2026-09-29

### Añadido
- ETFs en `config/tickers.csv`: SPY, QQQ, XLK, SMH y VGT (grupo `ETF`).
- Columna `RentabilidadDiaria` calculada en la ingesta y cargada en `Precios`.
- Medidas: Volatilidad Anualizada, Rentabilidad Anualizada (CAGR) y Rentabilidad / Riesgo.
- Página **Riesgo vs rentabilidad**: dispersión volatilidad vs rentabilidad anualizada por valor y grupo.
- Tabla resumen de *Rentabilidad y riesgo* con las nuevas medidas.

### Cambiado
- La ingesta usa la categoría del fondo como `Sector` cuando el valor es un ETF.

## [1.0.0] - 2026-09-29

### Añadido
- Ingesta de cotizaciones diarias desde Yahoo Finance (`scripts/ingesta_yfinance.py`) configurable desde `config/tickers.csv`: 7 Big Tech (AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA) y los índices ^GSPC y ^NDX desde 2019.
- Proyecto Power BI en formato PBIP (`App/Mercados.pbip`) con modelo en TMDL e informe en PBIR.
- Modelo: tablas `Precios`, `Tickers`, `Calendario` (tabla de fechas) y `_Medidas`.
- Medidas: Precio, Precio Inicial, Máximo Periodo, Última Fecha, Rentabilidad Acumulada, Drawdown y Volumen Medio.
- Página **Precios**: evolución del precio ajustado por valor.
- Página **Rentabilidad y riesgo**: segmentadores de valor, grupo y periodo; rentabilidad acumulada y drawdown por valor; tabla resumen.

### Cambiado
- Desactivada la fecha/hora automática de Power BI en favor de la tabla `Calendario`.

[Sin publicar]: https://github.com/dantencv/pbi-mercados/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/dantencv/pbi-mercados/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/dantencv/pbi-mercados/releases/tag/v1.0.0
