# CLAUDE.md — Instrucciones para Claude en este repositorio

Cuadro de mando de mercado de valores en Power BI (formato PBIP: TMDL + PBIR), versionado en Git/GitHub.
Claude edita los ficheros de texto del proyecto; el humano valida en Power BI Desktop y gestiona commits/PRs.

## Estructura
- `App/Mercados.pbip` + `App/Mercados.SemanticModel/` (modelo, TMDL) + `App/Mercados.Report/` (informe, PBIR). Rutas internas relativas: moverlos siempre juntos.
- `scripts/ingesta_yfinance.py` descarga cotizaciones de Yahoo Finance.
- `config/tickers.csv` lista de valores (`Ticker,Grupo,Activo`). Para añadir valores se añaden filas aquí, no se toca el código.
- `data/` CSV generados por el script. **No se versiona.** Power Query los lee con el parámetro `RutaDatos`.

## Reglas de trabajo
1. **Power BI Desktop debe estar cerrado** mientras Claude edita ficheros; si no, Desktop sobrescribe los cambios al guardar.
2. Trabajar siempre en una rama (`feature/…`, `fix/…`, `docs/…`), nunca directamente en `main`.
3. No tocar nunca: `**/.pbi/` (`cache.abf`, `localSettings.json`, `editorSettings.json`), `diagramLayout.json`, `StaticResources/`.
4. Tras cada cambio, indicar qué ficheros se han tocado y qué debe comprobarse en Desktop.
5. Si un cambio en el modelo rompe referencias del informe (tablas/columnas/medidas renombradas o eliminadas), actualizar también los `visual.json` afectados.

## Convenciones del modelo (TMDL)
- Formato de ficheros: indentación con **tabuladores**, saltos de línea **CRLF**, UTF-8.
- Objetos nuevos: `lineageTag` con GUID nuevo.
- Nombres en español. Nombres con espacios o tildes entre comillas simples: `measure 'Precio Inicial' = …`.
- **Medidas**: siempre en la tabla `_Medidas`, con `displayFolder` (Precios, Rentabilidad, Riesgo, Volumen…), `formatString` y descripción `///` en la línea anterior.
- DAX legible: `VAR`/`RETURN`, espacios dentro de paréntesis, `DIVIDE` en lugar de `/`.
- Tiempo: usar siempre `Calendario[Fecha]` (tabla de fechas marcada). `Precios[Fecha]` está oculta. La fecha/hora automática está **desactivada**: no reactivarla.
- Valores: filtrar/segmentar por `Tickers[Ticker]` / `Tickers[Grupo]` (dimensión), no por `Precios[Ticker]`.
- Las medidas de precio requieren un único ticker en contexto (`HASONEVALUE ( Precios[Ticker] )`).
- Precio de referencia: `Precios[CierreAjustado]` (ajustado por dividendos y splits).

## Convenciones del informe (PBIR)
- Una carpeta por página (`pages/<id>/page.json`) y por visual (`visuals/<id>/visual.json`). IDs: 20 caracteres hex.
- Registrar cada página nueva en `pages/pages.json` (`pageOrder`).
- Lienzo 1920×1080, `FitToPage`. Márgenes de 20 px entre visuales.
- Todos los visuales con título (`visualContainerObjects.title`).
- Mantener el `$schema` que ya usan los ficheros existentes.

## Git
- Commits estilo *Conventional Commits*: `feat(modelo): …`, `feat(informe): …`, `fix: …`, `docs: …`, `chore: …`.
- Cada cambio entra en `main` mediante Pull Request.
- Versionado semántico con tags (`vMAYOR.MENOR.PARCHE`):
  - MAYOR: cambio que rompe (se elimina/renombra una medida o página usada).
  - MENOR: funcionalidad nueva (medida, página, tabla, valores).
  - PARCHE: correcciones y ajustes de formato.
- Actualizar `CHANGELOG.md` (sección *Sin publicar*) en cada PR.
