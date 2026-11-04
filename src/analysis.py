"""Download WDI indicators and run an apparel/textiles trade trend forecast.

The WDI textiles-and-clothing share is multiplied by total merchandise exports
to create a transparent proxy. This is NOT a direct HS 61+62 export series.
"""
from pathlib import Path
import time
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUTPUT = ROOT / "outputs"
DATA.mkdir(exist_ok=True)
OUTPUT.mkdir(exist_ok=True)
COUNTRIES = {"IND":"India", "CHN":"China", "BGD":"Bangladesh", "VNM":"Vietnam", "TUR":"Türkiye"}
INDICATORS = {
    "TX.VAL.TXTL.UN.ZS": "textiles_clothing_share_pct",
    "TX.VAL.MRCH.CD.WT": "merchandise_exports_current_usd",
}
START_YEAR, END_YEAR, FORECAST_HORIZON = 2000, 2024, 5
BASE = "https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}"

def fetch_indicator(indicator):
    country_path = ";".join(COUNTRIES)
    url = BASE.format(countries=country_path, indicator=indicator)
    params = {"format":"json", "date":f"{START_YEAR}:{END_YEAR}", "per_page":20000}
    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
        raise RuntimeError(f"No observations returned for {indicator}: {payload}")
    rows = []
    for item in payload[1]:
        if item.get("value") is not None:
            rows.append({"country_code":item["countryiso3code"],
                         "country":item["country"]["value"],
                         "year":int(item["date"]), "value":float(item["value"]),
                         "indicator":indicator})
    return pd.DataFrame(rows)

def fetch_data():
    frames=[]
    for indicator in INDICATORS:
        frames.append(fetch_indicator(indicator))
        time.sleep(0.2)
    raw=pd.concat(frames, ignore_index=True)
    raw.to_csv(DATA/"wdi_raw_observations.csv", index=False)
    wide=raw.pivot_table(index=["country_code","country","year"],
                         columns="indicator", values="value").reset_index()
    wide=wide.rename(columns=INDICATORS)
    wide["textiles_clothing_export_proxy_usd"] = (
        wide["merchandise_exports_current_usd"] *
        wide["textiles_clothing_share_pct"] / 100
    )
    wide=wide.sort_values(["country_code","year"])
    wide.to_csv(DATA/"country_year_textiles_proxy.csv", index=False)
    return wide

def moving_average_forecast(train, horizon=FORECAST_HORIZON, window=3):
    values=list(train.astype(float))
    forecasts=[]
    for _ in range(horizon):
        pred=float(np.mean(values[-window:]))
        forecasts.append(pred)
        values.append(pred)
    return np.array(forecasts)

def regression_forecast(train, horizon=FORECAST_HORIZON):
    years=train["year"].to_numpy().reshape(-1,1)
    values=train["textiles_clothing_export_proxy_usd"].to_numpy()
    model=LinearRegression().fit(years, values)
    future=np.arange(int(train.year.max())+1, int(train.year.max())+horizon+1).reshape(-1,1)
    return np.maximum(model.predict(future),0)

def evaluate_models(country_df):
    rows=[]
    ordered=country_df.dropna(subset=["textiles_clothing_export_proxy_usd"]).sort_values("year")
    if len(ordered)<9:
        return pd.DataFrame()
    train=ordered.iloc[:-5]
    test=ordered.iloc[-5:]
    actual=test["textiles_clothing_export_proxy_usd"].to_numpy()
    ma=moving_average_forecast(train["textiles_clothing_export_proxy_usd"],5)
    lr=regression_forecast(train,5)
    for name,pred in [("3-year recursive moving average",ma),("Linear regression",lr)]:
        rows.append({"model":name,"MAE_USD":mean_absolute_error(actual,pred),
                     "RMSE_USD":mean_squared_error(actual,pred)**0.5,
                     "holdout_years":f'{test.year.min()}-{test.year.max()}'})
    return pd.DataFrame(rows).sort_values("MAE_USD")

def main():
    df=fetch_data()
    all_forecasts=[]
    evaluations=[]
    for code, country in COUNTRIES.items():
        cdf=df[df.country_code==code].dropna(
            subset=["textiles_clothing_export_proxy_usd"]).sort_values("year")
        if len(cdf)<9:
            print(f"Skipping {country}: insufficient observations")
            continue
        metrics=evaluate_models(cdf)
        if metrics.empty:
            continue
        metrics.insert(0,"country",country)
        evaluations.append(metrics)
        selected=metrics.iloc[0]["model"]
        if selected=="Linear regression":
            preds=regression_forecast(cdf)
        else:
            preds=moving_average_forecast(cdf["textiles_clothing_export_proxy_usd"],5)
        years=np.arange(int(cdf.year.max())+1,int(cdf.year.max())+6)
        for year,pred in zip(years,preds):
            all_forecasts.append({"country":country,"year":int(year),
                                  "forecast_proxy_usd":float(pred),
                                  "selected_model":selected,
                                  "based_on_last_observation":int(cdf.year.max())})
        # Actual + forecasts chart
        plt.figure(figsize=(10,5))
        plt.plot(cdf.year,cdf.textiles_clothing_export_proxy_usd/1e9,
                 marker="o",label="Historical proxy")
        plt.plot(years,preds/1e9,marker="o",linestyle="--",label=f"Forecast: {selected}")
        plt.title(f"{country}: textiles & clothing export proxy")
        plt.xlabel("Year"); plt.ylabel("Current US$ billions")
        plt.grid(alpha=.25); plt.legend(); plt.tight_layout()
        plt.savefig(OUTPUT/f"{code.lower()}_forecast.png",dpi=160)
        plt.close()
    if not all_forecasts:
        raise RuntimeError("No countries had enough observations to forecast.")
    forecasts=pd.DataFrame(all_forecasts)
    scores=pd.concat(evaluations,ignore_index=True) if evaluations else pd.DataFrame()
    forecasts.to_csv(OUTPUT/"five_year_forecasts.csv",index=False)
    scores.to_csv(OUTPUT/"model_comparison.csv",index=False)
    # Comparative chart
    plt.figure(figsize=(11,6))
    for country,part in df.groupby("country"):
        part=part.dropna(subset=["textiles_clothing_export_proxy_usd"])
        plt.plot(part.year,part.textiles_clothing_export_proxy_usd/1e9,label=country)
    plt.title("Historical textiles and clothing export proxy")
    plt.xlabel("Year"); plt.ylabel("Current US$ billions")
    plt.grid(alpha=.25); plt.legend(); plt.tight_layout()
    plt.savefig(OUTPUT/"country_comparison.png",dpi=160); plt.close()
    print("Analysis complete.")
    print("Latest observed year by country:")
    print(df.dropna(subset=["textiles_clothing_export_proxy_usd"]).groupby("country").year.max())
    print("\nModel comparison (lower MAE is better):")
    print(scores.to_string(index=False))
    print("\nFive-year forecasts:")
    print(forecasts.to_string(index=False))
    print("\nOutputs saved under outputs/ and data/.")

if __name__=="__main__":
    main()
