# Input data guide

Download annual merchandise trade data from UN Comtrade Plus or another documented public source.

Recommended apparel scope:
- HS 61: knitted or crocheted apparel and accessories.
- HS 62: apparel and accessories not knitted or crocheted.
- Flow: exports; partner: World; frequency: annual.
- Aim for at least 10 annual observations when consistent coverage permits.

Save an aggregated CSV as `data/apparel_trade_annual.csv` with columns `year,export_value_usd`. Document source URL, retrieval date, reporter, partner, flow, HS revision, currency, unit, missing years and aggregation. Do not treat missing values as zero or combine incompatible classifications. The project intentionally does not invent historical market data; supply the verified source extract before generating numerical forecasts.
