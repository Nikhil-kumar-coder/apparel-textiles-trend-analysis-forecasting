# Week 5 Project Report: Trend Analysis and Forecasting in the Apparel & Textiles Industry

## Executive Summary
This project establishes a reproducible country-year analysis of textiles and clothing trade exposure for India, China, Bangladesh, Vietnam and Türkiye. It combines a quantitative historical indicator with qualitative interpretation of industry forces, and compares a recursive three-year moving average with linear regression. The analysis pipeline retrieves public World Bank indicators, constructs a clearly labelled export proxy, evaluates models on a five-observation holdout and forecasts five years beyond the latest available observation for each country.

**Data integrity note:** The quantitative series is a derived proxy, not a direct sum of HS Chapter 61 and 62 exports. It multiplies total merchandise exports by the WDI textiles-and-clothing share. Values are in current US dollars and are not adjusted for inflation. Actual country-level forecast values and charts are generated when `python src/analysis.py` is run; this report does not invent numerical findings.

## 1. Introduction and objectives
Apparel and textiles is influenced by global sourcing, labour costs, trade policy, consumer preferences, exchange rates, logistics, technology and sustainability requirements. Trend analysis can help businesses plan capacity, sourcing, inventory, market entry and investment. The project aims to:
- assemble a consistent historical indicator panel;
- describe trend direction and differences between selected economies;
- compare forecasting methods using an out-of-sample test;
- explain the business meaning and uncertainty of forecasts;
- identify risks, opportunities and strategic responses.

## 2. Scope and country selection
The analysis includes India, China, Bangladesh, Vietnam and Türkiye. These economies provide a useful illustrative comparison of major textile/apparel production and trade participants across Asia and its adjacent sourcing region. The sample is not a complete ranking of exporters and does not represent every part of the value chain.

The unit of analysis is annual country-level data. Annual data is suitable for medium-term structural direction but cannot reveal seasonal buying cycles, fashion micro-trends or short-term order volatility.

## 3. Data sources and collection
The pipeline uses the World Bank World Development Indicators API:
- Indicator `TX.VAL.TXTL.UN.ZS`: textiles and clothing as a percentage of merchandise exports.
- Indicator `TX.VAL.MRCH.CD.WT`: merchandise exports in current US dollars.

The World Bank metadata identifies the first series as textiles and clothing (% of merchandise exports), and the second as merchandise exports in current US dollars. The script requests 2000–2024 for the five selected economies. The latest available year can differ by country because statistical releases are not always simultaneous.

### Derived measure
For each country-year:
**Textiles & clothing export proxy (US$) = Merchandise exports (current US$) × Textiles & clothing share (%) ÷ 100.**

This construction produces an approximate value consistent with the share indicator. It is not a direct product-level customs value and should not be interpreted as a precise HS 61+62 total. A more detailed follow-up should query UN Comtrade for apparel HS 61 (knitted/crocheted apparel) and HS 62 (not knitted/crocheted apparel), harmonising HS revisions and reporting coverage.

### Data preparation
1. Request each indicator through the public WDI API.
2. retain country code, country, year, indicator and numeric value.
3. Pivot the indicators into one country-year record.
4. Calculate the proxy only when both input values are available.
5. Preserve missing values; do not convert missing observations into zero.
6. Sort by country and year, save raw observations and derived data as CSV.
7. Record the latest observed year per country before forecasting.

## 4. Historical trend analysis
The generated country comparison chart plots the proxy over time. Interpret it using:
- **Direction:** sustained increase, decline or relative stability.
- **Growth:** year-over-year percentage change, calculated only when the previous value is positive and available.
- **Volatility:** size and frequency of annual changes.
- **Comparative position:** differences in scale and trajectory, while remembering that current-dollar values are affected by prices and exchange rates.
- **Structural breaks:** unusual movements that may coincide with global shocks, policy changes or reporting revisions. A coincident event is a hypothesis to investigate, not proof of causation.

### Qualitative industry context
Several forces may shape future apparel and textile trade:
- **Supply-chain diversification:** buyers may distribute orders across more sourcing countries to reduce concentration and disruption risk.
- **Cost and productivity:** wages, energy, logistics, lead times, worker skills and factory productivity affect sourcing decisions.
- **Sustainability and traceability:** recycled fibres, water and chemical management, emissions reporting, product durability and supply-chain transparency are increasingly relevant to brand procurement and compliance.
- **Digitalisation:** demand forecasting, automated cutting, digital product development and inventory analytics can improve responsiveness and reduce waste.
- **Consumer demand:** price sensitivity, online retail, shorter trend cycles and demand for functional or comfortable clothing influence assortment and replenishment.
- **Trade policy and geopolitics:** tariffs, rules of origin, trade agreements and sanctions can shift landed costs and sourcing routes.

These are strategic themes for interpretation. The WDI export proxy does not measure sustainability, consumer sentiment, factory productivity or digital adoption directly.

## 5. Forecasting methodology
Two transparent baselines are compared.

### 5.1 Three-year recursive moving average
The next forecast is the average of the latest three observations. For the second future year, the first forecast is added to the series and the latest three values are averaged again. This continues through the horizon.

**Why use it:** It is easy to explain, reduces the influence of one unusual year and provides a baseline against which more complex models can be judged.

**Weakness:** It smooths turning points and tends to flatten longer-range forecasts. It does not explicitly model economic drivers or seasonality.

### 5.2 Linear regression
A simple least-squares model is fitted:
**Export proxy = intercept + slope × year.**
The fitted slope represents the average linear change per year over the training period. Substituting future years into the fitted equation produces the forecasts. Negative forecasts are clipped to zero because negative export values are not meaningful.

**Why use it:** It provides an interpretable long-run direction and is suitable as a basic trend extrapolation.

**Weakness:** It assumes a constant linear relationship with time. It can overstate or understate future values when growth accelerates, saturates or changes direction.

### 5.3 Time-series analysis and ARIMA
ARIMA combines autoregression, differencing and moving-average error terms. The analyst first inspects the series, checks whether its mean and variance are stable, and applies differencing if required. Candidate orders are selected using diagnostics and validation, then residuals are checked for remaining autocorrelation. ARIMA can capture serial dependence better than a straight trend in some settings, but annual series with limited observations can produce unstable estimates. Therefore, ARIMA is documented as a justified extension rather than automatically treated as superior.

### 5.4 Validation and model selection
For each country, the final five observed years are held out. Each model is trained on earlier years and predicts the holdout period. The script calculates:
- **MAE:** average absolute forecast error, in US dollars.
- **RMSE:** square root of average squared error, penalising large misses.

The model with lower holdout MAE is selected for the five-year forecast. The comparison is country-specific. MAE values should not be compared directly across countries without considering the scale of their export proxy. A single holdout window is a limited evaluation; rolling-origin validation would be stronger.

## 6. Forecast interpretation
The script writes a five-year forecast table and a chart for each country. For each country, the reader should:
1. note the latest actual year and the selected model;
2. compare the forecast slope with the historical trajectory;
3. compare the model score with the alternative;
4. identify whether the forecast is stable, rising or falling;
5. avoid treating extrapolation as a guaranteed outcome.

The forecast is conditional on the historical pattern continuing. It does not incorporate future GDP, consumer demand, tariffs, input prices, exchange rates, sustainability rules or investment. These drivers should be added in a future multivariate model.

## 7. Potential market impacts
- A sustained positive trajectory may support investment in capacity, worker training, quality systems and export-market development.
- A flat or declining trajectory may encourage productivity improvements, product differentiation, market diversification and careful working-capital management.
- Divergent country trajectories may motivate buyers to diversify sourcing, but supplier qualification, quality, compliance and lead time remain essential.
- Higher sustainability expectations may increase short-term compliance costs while creating opportunities for certified materials, traceable supply chains and lower-waste production.
- Digital planning can reduce forecasting error and excess inventory, particularly where demand is volatile.

## 8. Risks and opportunities
### Risks
- Exchange-rate and inflation effects can distort nominal-dollar comparisons.
- Trade restrictions, geopolitical events and logistics disruption can change trade flows abruptly.
- Labour, energy, water and raw-material costs may erode competitiveness.
- Sustainability and labour-compliance failures can damage market access and reputation.
- Fashion demand is uncertain; annual trade data cannot capture fast-moving product preferences.
- Forecast models can fail when structural breaks occur.

### Opportunities
- Diversifying export destinations and sourcing markets.
- Investing in higher-value products, technical textiles and product quality.
- Improving traceability, recycled-material use, water and energy efficiency.
- Applying digital forecasting and inventory optimisation.
- Building resilient supplier networks and shorter replenishment cycles.

## 9. Strategic recommendations
1. Use the five-year forecast as a planning scenario, not a sales target.
2. Refresh the WDI data annually and compare it with direct HS 61/62 Comtrade trade values.
3. Track export value alongside export volume or unit-value indices to separate price from quantity effects.
4. Develop country-specific sourcing strategies rather than relying on one global trend.
5. Invest in traceability, quality, energy/water efficiency and compliance readiness.
6. Use monthly company-level orders and sell-through data for operational forecasting; annual macro data is too coarse for SKU-level inventory decisions.
7. Revalidate models after major policy, demand or supply-chain shocks.

## 10. Limitations and future improvements
This is a five-country macro-level exercise using a derived WDI proxy. Current-dollar values are not inflation-adjusted. Annual observations do not expose seasonality. The project does not directly measure retail sales, domestic consumption, brand demand, sustainability performance or factory output. Forecasts are point estimates without prediction intervals. Future work should add direct UN Comtrade HS 61 and HS 62 data, constant-price/volume measures, more countries, rolling-origin validation, prediction intervals and explanatory variables such as GDP, exchange rates, wages and freight costs.

## 11. Conclusion
The project provides a reproducible workflow for collecting public indicators, constructing a documented textiles-and-clothing trade proxy, comparing simple forecasting baselines and interpreting forecasts in a business context. Its central discipline is transparency: historical observations, derived measures, model predictions and qualitative hypotheses are kept distinct. This makes the analysis useful as a learning and planning reference without overstating what the available data can prove.

## Appendix A: Reproduction
Install packages with `pip install -r requirements.txt`, then run `python src/analysis.py`. The script creates raw and derived CSV files, model comparison metrics, five-year forecasts and trend charts in the `data/` and `outputs/` directories.

## Appendix B: Key references
- World Bank WDI indicator TX.VAL.TXTL.UN.ZS — Textiles and clothing (% of merchandise exports): https://api.worldbank.org/v2/indicator/TX.VAL.TXTL.UN.ZS
- World Bank WDI indicator TX.VAL.MRCH.CD.WT — Merchandise exports (current US$): https://api.worldbank.org/v2/indicator/TX.VAL.MRCH.CD.WT
- World Bank DataBank metadata for merchandise exports: https://databank.worldbank.org/metadataglossary/world-development-indicators/series/TX.VAL.MRCH.CD.WT
- UN Comtrade API documentation: https://uncomtrade.org/docs/un-comtrade-api/
- WTO merchandise trade statistics: https://data.wto.org/en/dataset/commerchandise
