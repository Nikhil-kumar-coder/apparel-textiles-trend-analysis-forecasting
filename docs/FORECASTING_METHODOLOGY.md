# Forecasting Methodology

## 1. Unit of analysis
Country-year observations. Five apparel/textile trading economies are selected: India, China, Bangladesh, Vietnam and Türkiye. The analysis uses a proxy derived from two WDI indicators, not a product-level HS 61/62 measure.

## 2. Data construction
For each country and year:
1. Retrieve the share of merchandise exports represented by textiles and clothing.
2. Retrieve merchandise exports in current US dollars.
3. Compute proxy = merchandise exports × share / 100.
4. Retain the source observations and save the derived panel.
5. Do not replace missing values with zero; countries can have different latest years.

## 3. Models
### Three-year moving average
The next value is the mean of the most recent three observed values. For multi-step forecasting, each prediction is appended and used in the next window (recursive forecast). This smooths short-term volatility but reacts slowly to turning points.

### Linear regression
Fit export proxy as a linear function of calendar year. Extrapolate the fitted line five years beyond the latest observation. It captures a broad linear direction but cannot represent seasonality, abrupt policy changes or nonlinear growth.

### Time-series model discussion
ARIMA models use autoregressive terms, differencing and moving-average errors to model temporal dependence. They can be evaluated as an extension when the series is sufficiently long and stable. The core reproducible implementation compares two transparent baselines to avoid presenting a fragile ARIMA fit as authoritative. For monthly or quarterly data, seasonal ARIMA/exponential smoothing may be more appropriate after checking seasonality and stationarity.

## 4. Model selection
The last five available observations are held out. Each candidate is trained only on earlier years; MAE and RMSE are computed against the holdout. The lower-MAE candidate is selected for the five-year extrapolation for that country. Scores are country-specific and should not be compared across countries without considering scale.

## 5. Limitations
- Derived export proxy, not direct HS 61/62 commodity trade.
- Current US dollars include price and exchange-rate effects; no deflation.
- WDI observations may be revised or missing and may lag.
- Five-country sample is illustrative, not the entire global industry.
- Five-year extrapolation cannot anticipate shocks, trade policy, pandemics, climate events or technology shifts.
- No prediction interval in the baseline implementation.
