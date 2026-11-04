# Week 5 — Apparel & Textiles Trend Analysis and Forecasting

This project studies historical textiles-and-clothing trade exposure for India, China, Bangladesh, Vietnam and Türkiye, then compares simple forecasting baselines.

## Data and important interpretation
The pipeline downloads two annual World Bank World Development Indicators (WDI) series:
- `TX.VAL.TXTL.UN.ZS`: Textiles and clothing (% of merchandise exports).
- `TX.VAL.MRCH.CD.WT`: Merchandise exports (current US$).

It calculates a transparent **textiles-and-clothing export proxy** as:
`merchandise exports × textiles/clothing share / 100`.

This derived proxy is not a direct HS Chapter 61 + 62 export total, and should not be described as one. It is nominal/current-dollar data, not inflation-adjusted. Coverage and latest available year may vary by country.

Sources: World Bank WDI (CC BY 4.0); metadata and definitions are linked in the report.

## Run
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/analysis.py
```

The script downloads observations into `data/`, evaluates a 3-year recursive moving-average baseline and linear regression on the final five historical observations, chooses the lower-MAE model per country, and forecasts five years beyond each country's latest available observation.

## Outputs
- `data/wdi_raw_observations.csv`
- `data/country_year_textiles_proxy.csv`
- `outputs/model_comparison.csv`
- `outputs/five_year_forecasts.csv`
- `outputs/country_comparison.png`
- One historical/forecast chart per country.

## Method notes
A rolling holdout is used rather than fitting and scoring on the same observations. With short annual series, the models are intentionally simple baselines. The selected model is not guaranteed to be best in future periods. Forecasts are conditional extrapolations, not certainty or a market-size promise.

## Suggested extensions
Use UN Comtrade HS 61 and HS 62 exports separately for product-level analysis; use constant-price/volume indices where available; test ARIMA or exponential smoothing only when enough regular observations exist; add prediction intervals and structural-break analysis.
