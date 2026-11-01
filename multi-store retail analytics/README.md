# Walmart Retail Performance & Risk Intelligence

A portfolio-style retail analytics project built from the supplied Walmart weekly sales dataset. It examines the 45-store network through revenue concentration, holiday response, annual store performance, weekly sales volatility and store-level exposure to macroeconomic change.

The analysis is designed around one central distinction: **sales scale, sales stability and sales sensitivity are not the same thing**. A store can rank highly by revenue and still have volatile weeks; a store can respond positively to a holiday and still decline on a like-for-like basis.

## Project at a glance

| Dimension | Result |
|---|---:|
| Source rows | 6,435 |
| Stores | 45 |
| Weekly dates | 143 |
| Period | 5 February 2010 – 26 October 2012 |
| Missing values | 0 |
| Duplicate Store-Date keys | 0 |
| Holiday-flagged store-week rows | 450 |
| Distinct observed holiday dates | 10 |
| Total recorded sales | $6.737B |

## Analytical questions

- Which 10 stores account for the strongest sales base, and how much of network revenue do they represent?
- Which of the four holiday events produces a repeatable uplift after normalizing each store against its own non-holiday baseline?
- How does the monthly network sales rhythm evolve from 2010 to 2012?
- What do annual Store × Year totals and YoY rates say—and where do partial years distort that interpretation?
- Which stores are most volatile in absolute dollars and relative to their own sales scale?
- Do Temperature, Fuel_Price, CPI and Unemployment have meaningful relationships with sales?
- Which stores show the strongest negative unemployment sensitivity after controlling for weekly changes and calendar seasonality?

## Main findings

- Store 20 leads the observed period with **$301.4M** in cumulative sales; Store 33 is lowest at **$37.2M**. The leader is about 8.1 times the lowest store.
- The Top 10 stores contribute **39.1%** of total network sales; the Bottom 10 contribute **8.6%**.
- Holiday-flagged store-weeks average **$1.123M**, compared with **$1.041M** for non-holiday weeks: a **7.84%** uplift.
- Thanksgiving is the strongest event: **+41.3%** versus the overall non-holiday average and **+38.4%** after store-level normalization. Christmas is below baseline at **−7.7%** raw and **−7.4%** store-normalized.
- December 2010 is the highest monthly total at **$288.8M**. The largest single week is 24 December 2010 at **$80.9M**.
- Store 35 has the highest relative weekly volatility at **22.97% CV**. Store 14 has the largest absolute weekly standard deviation at about **$317.6K**.
- At the 143-week market level, macroeconomic correlations are weak. Temperature is the largest negative Pearson relationship (**r = −0.159, p = 0.058**); Fuel_Price, CPI and Unemployment are close to zero.
- Store 42 is the most consistently negative unemployment-sensitivity signal across the two store-level model specifications.
- Seven stores declined in the comparable February–October 2012 window despite positive 2012 holiday-week uplift.

The full interpretation, operational recommendations and caveats are in [`note.md`](note.md).

## Dataset and source

The project uses the supplied `Walmart.csv`, from the Kaggle Walmart dataset:

https://www.kaggle.com/datasets/yasserh/walmart-dataset

The original file is included under `data/Walmart.csv`. The dataset contains:

| Column | Meaning |
|---|---|
| `Store` | Store identifier |
| `Date` | Weekly date, stored as `dd-mm-yyyy` in the source |
| `Weekly_Sales` | Weekly store sales |
| `Holiday_Flag` | 1 for a holiday-associated week, otherwise 0 |
| `Temperature` | Store-week temperature |
| `Fuel_Price` | Store-week fuel price |
| `CPI` | Store-week consumer price index |
| `Unemployment` | Store-week unemployment rate |

The macroeconomic indicators vary across stores and dates; they are not constant across the 45 stores. On an average weekly date, the file contains approximately 34.8 distinct Temperature values, 9.3 Fuel_Price values, 15.0 CPI values and 29.7 Unemployment values.

## Project structure

```text
walmart_retail_intelligence/
├── Walmart_Retail_Analytics_Executed.ipynb
├── README.md
├── note.md
├── requirements.txt
├── data/
│   └── Walmart.csv
├── visuals/
│   ├── 01_store_revenue_tiering.png
│   ├── 02_holiday_uplift.png
│   ├── 03_monthly_sales_rhythm.png
│   ├── 04_store_year_sales_heatmap.png
│   ├── 05_macro_correlation_comparison.png
│   ├── 06_store_volatility_map.png
│   └── 07_unemployment_sensitivity_forest.png
└── outputs/
    ├── store_performance_and_tiers.csv
    ├── store_tier_contribution.csv
    ├── holiday_uplift_by_type.csv
    ├── holiday_date_sales.csv
    ├── monthly_sales_trend.csv
    ├── store_year_sales_pivot.csv
    ├── store_year_yoy_growth_pct.csv
    ├── store_like_for_like_growth_pct.csv
    ├── store_volatility_ranking.csv
    ├── macro_correlation_comparison.csv
    ├── store_unemployment_sensitivity.csv
    ├── unemployment_model_robustness.csv
    └── stores_for_investigation.csv
```

## Run the notebook

### Environment

Python 3.10+ is recommended.

Install the required libraries:

```bash
pip install -r requirements.txt
```

Launch Jupyter:

```bash
jupyter lab
```

Open `Walmart_Retail_Analytics_Executed.ipynb` and run the notebook from top to bottom. The delivered notebook already contains execution counts, embedded table outputs and all seven chart outputs.

### Dataset path

The notebook's `DATA_PATH` is configured to the requested Windows Desktop location:

```python
DATA_PATH = r"C:\Users\anarrasulzada\Desktop\Walmart.csv"
df = pd.read_csv(DATA_PATH)
```

If you prefer the included project copy, change only the path value to:

```python
DATA_PATH = "data/Walmart.csv"
```

The loading step uses a direct `pd.read_csv` call; it does not use an `if/else` file-discovery fallback.

## Analytical design

### Store tiering

Stores are ranked by total `Weekly_Sales` across the observed period:

- Top 10: ranks 1–10
- Mid 25: ranks 11–35
- Bottom 10: ranks 36–45

The analysis reports total sales, average weekly sales, standard deviation and coefficient of variation. Tier contribution is measured against the $6.737B network total.

### Holiday analysis

The four event types are mapped to their observed weekly dates. The file contains 10 distinct holiday dates, each represented by 45 store-week rows: 450 rows in total.

The holiday comparison reports both:

1. Raw mean sales for all rows where `Holiday_Flag = 1` versus `Holiday_Flag = 0`.
2. Store-normalized uplift: each store's event-week mean is compared with its own non-holiday average. Confidence intervals are calculated across the 45 store-level event averages.

The 2012 Thanksgiving and Christmas dates fall after the source end date and are not observed.

### Monthly trend

Weekly sales are summed across stores by calendar month. The number of observed weekly dates per month is retained so that month totals are not interpreted without their observation coverage.

### Store × Year pivot

The annual pivot reports raw total sales by store and year, followed by store-level YoY percentage change. The data is incomplete at both ends:

- 2010: 48 weekly dates, beginning in February.
- 2011: 52 weekly dates.
- 2012: 43 weekly dates, ending in October.

A separate February–October comparison uses exactly 39 weekly dates in each year. This is the preferred view for comparing 2012 with 2011.

### Volatility

- Standard deviation is the absolute-dollar measure.
- Coefficient of variation (standard deviation divided by mean weekly sales) is the relative measure.

A high standard deviation can simply reflect a large store. CV helps identify stores with more unstable sales relative to their own average.

### External factors and unemployment sensitivity

The notebook reports Pearson correlations at two observation levels:

- Pooled store-week records: retains store-level variation.
- Weekly market aggregates: sums sales and averages the four macro indicators across stores, producing 143 observations.

Store-level unemployment sensitivity uses a first-difference model:

`Δlog(Weekly_Sales) ~ ΔUnemployment + ΔTemperature + ΔFuel_Price + ΔCPI + month controls`

Newey–West HAC standard errors use four lags. Benjamini–Hochberg false-discovery-rate adjustment is applied across the 45 store-level unemployment tests. A second level specification with a time trend is used as a robustness comparison.

## Interpretation boundaries

- The file has sales but no units, margin, inventory, promotion, local competition or operating-hour data. It cannot explain why sales changed.
- `Holiday_Flag` marks a holiday-associated week; it does not isolate the causal impact of a specific promotion or shopping day.
- Holiday event samples are uneven: Super Bowl and Labour Day have three observed dates each; Thanksgiving and Christmas have two each.
- Annual 2010 and 2012 totals are partial. Raw annual YoY rates should not be treated as full-year growth.
- Monthly sums depend on the number of weekly dates in each month.
- Macro correlations are descriptive. The 143-week aggregate and pooled store-week view answer different questions.
- CPI, Fuel_Price, Unemployment and time are strongly collinear. Store-specific coefficients are exposure signals, not causal elasticities.
- Unemployment changes in only 11 of 142 weekly transitions in the averaged market series. The sensitivity ranking is therefore exploratory and should be checked against local commercial data.

## Included deliverables

- Fully executed Jupyter notebook with code, comments, outputs and embedded charts.
- `note.md` with the detailed findings, reference-note reconciliation and five operational insights.
- Seven standalone PNG visualizations.
- CSV outputs for store ranking, tier contribution, holiday effects, monthly trends, annual pivots, volatility, macro correlations, unemployment sensitivity and investigation flags.
