# The Walmart network: where revenue concentrates, when the calendar pays, and where risk hides

## Executive readout

The 45-store network generated **$6.737 billion** across the observed period. That headline conceals three very different operating patterns.

- Revenue is concentrated: the Top 10 stores account for **39.05%** of sales, while the Bottom 10 account for **8.61%**.
- Holiday demand is not uniform: Thanksgiving creates a pronounced lift, Super Bowl produces a modest increase, Labour Day is close to neutral, and Christmas falls below the non-holiday baseline.
- The weakest store by cumulative sales is not necessarily the most unstable. Store 33 is the smallest by sales, while Store 35 has the highest relative volatility.
- Broad macroeconomic indicators explain little of network-wide sales variation in simple weekly correlations. A store-level unemployment sensitivity model identifies Store 42 as the most consistent negative exposure signal, but that result requires careful interpretation.

The management implication is to separate **portfolio scale**, **calendar response**, **operational volatility** and **economic exposure**. They should not be combined into a single store score.

## The source file, as observed

| Data control | Result |
|---|---:|
| Rows | 6,435 |
| Stores | 45 |
| Distinct weekly dates | 143 |
| First observed date | 5 February 2010 |
| Last observed date | 26 October 2012 |
| Weekly records per store | 143 |
| Missing cells | 0 |
| Duplicate Store-Date keys | 0 |
| Total recorded sales | $6,737,218,987 |

Every store has a complete 143-week panel. The data contains 48 weeks in 2010, 52 in 2011 and 43 in 2012. The first and final calendar years are therefore partial.

The macro fields are store-specific. On an average date there are approximately 34.8 distinct Temperature values, 9.3 Fuel_Price values, 15.0 CPI values and 29.7 Unemployment values across the 45 stores. This matters: the macro indicators should not be described as one identical weekly value repeated across all stores.

## Store portfolio: a wide revenue gap

### Tier contribution

| Tier | Stores | Network sales share | Average cumulative sales per store |
|---|---:|---:|---:|
| Top 10 | 10 | 39.05% | $263.1M |
| Mid 25 | 25 | 52.33% | $141.0M |
| Bottom 10 | 10 | 8.61% | $58.0M |

Store 20 leads with **$301.40M**, followed by Store 4 at **$299.54M**. Store 33 is last at **$37.16M**. The top store produced approximately **8.1 times** the cumulative sales of the lowest store.

This is a substantial performance spread, but cumulative sales alone do not establish execution quality. The file contains no store size, floor area, local market potential, operating hours or category mix. A high-revenue store may simply serve a larger catchment.

### What the ranking suggests

The Top 10 are the network's revenue anchors and deserve close attention to availability, replenishment and peak-week execution. The Bottom 10 need a different diagnostic: local demand, store footprint, category mix and operating constraints should be checked before attributing the gap to management performance.

## Holiday economics: the calendar is asymmetric

### Overall holiday comparison

| Week type | Mean sales per store-week | Difference from normal |
|---|---:|---:|
| Non-holiday | $1,041,256 | Baseline |
| Holiday | $1,122,888 | +7.84% |

The observed holiday mean is about **$81,632** higher per store-week. The source contains **450 rows** with `Holiday_Flag = 1`, which represent **10 distinct holiday dates × 45 stores**. This is not 63 distinct flagged calendar weeks.

### Event-level uplift

The primary event ranking compares each store's average sales for an event type with that same store's average non-holiday sales. The mean is then calculated across 45 stores. This reduces the influence of the largest stores.

| Event | Observed dates | Raw uplift vs network non-holiday mean | Store-normalized uplift | 95% CI across stores |
|---|---:|---:|---:|---:|
| Thanksgiving | 2 | +41.30% | **+38.40%** | +31.62% to +45.18% |
| Super Bowl | 3 | +3.64% | +3.42% | +1.34% to +5.51% |
| Labour Day | 3 | +0.11% | +0.56% | −1.75% to +2.87% |
| Christmas | 2 | −7.72% | **−7.39%** | −10.34% to −4.44% |

Thanksgiving is the clear commercial event in this sample. The effect is large and positive across stores. Super Bowl has a smaller but positive response. Labour Day is effectively neutral: its confidence interval crosses zero. Christmas is negative relative to the average non-holiday week, consistent with demand being pulled forward into earlier December weeks rather than concentrated in the Christmas week itself.

### Observed holiday dates

- **Super Bowl:** 12 February 2010, 11 February 2011, 10 February 2012.
- **Labour Day:** 10 September 2010, 9 September 2011, 7 September 2012.
- **Thanksgiving:** 26 November 2010, 25 November 2011.
- **Christmas:** 31 December 2010, 30 December 2011.

The dataset ends on 26 October 2012. The 2012 Thanksgiving and Christmas dates are outside the sample, so those event types have two observed dates rather than three.

### Reading the uplift correctly

The raw uplift compares all holiday store-weeks with all non-holiday store-weeks. The store-normalized uplift compares an event with each store's own baseline. The two values differ because the second calculation controls for the large spread in store revenue levels.

The supplied reference notes mention a +24.3% Thanksgiving uplift and approximately +6.7% overall holiday uplift. Those figures are not reproduced using the direct mean and store-normalized definitions above. The calculations in this project are explicit and can be rebuilt from the source rows.

## Monthly rhythm: the year-end pulse is stronger than the November headline

Monthly totals are calculated by summing weekly sales across all 45 stores.

- Highest monthly total: **December 2010 — $288.76M**.
- Second-highest monthly total: **December 2011 — $288.08M**.
- Highest single week: **24 December 2010 — $80.93M**.
- Thanksgiving week 2011 (25 November) generated **$66.59M** across the network.

November 2011 does contain a pronounced Thanksgiving/Black Friday event week, but it is not the highest monthly sales total in this file. December 2010 is the monthly peak, and 24 December 2010 is the highest single week. The distinction between a holiday spike, a month total and the maximum week is important when planning inventory and staffing.

Monthly totals also depend on how many Friday-ending weekly observations fall into a calendar month. The notebook retains the number of observed weekly dates per month so that a five-Friday month is not compared with a four-Friday month without context.

## Store × Year: the annual pivot needs a like-for-like companion

The annual Store × Year pivot and the YoY percentage table are included as requested. However:

| Year | First observed week | Last observed week | Weekly dates |
|---|---|---|---:|
| 2010 | 5 February | 31 December | 48 |
| 2011 | 7 January | 30 December | 52 |
| 2012 | 6 January | 26 October | 43 |

The median raw store-level YoY rate is **+7.97%** for 2011 versus 2010 and **−17.50%** for 2012 versus 2011. The latter is not a fair performance comparison: 2012 has nine fewer weekly observations than 2011, while 2010 is also missing the first five weeks of the calendar year.

### Comparable February–October window

All three years contain exactly **39 weekly dates** from February through October. Using this consistent window:

| Comparison | Mean store growth | Median store growth |
|---|---:|---:|
| 2011 vs 2010 | −0.36% | +0.89% |
| 2012 vs 2011 | +2.90% | +3.46% |

The like-for-like result changes the story materially. The raw annual pivot suggests a sharp 2012 decline, while the common 39-week comparison shows positive median growth across stores. Seven stores nevertheless declined on the comparable 2012-vs-2011 window and also showed positive 2012 holiday uplift.

## Volatility: size and instability tell different stories

Two volatility measures produce different leaders.

| Lens | Store | Result |
|---|---:|---:|
| Highest absolute weekly sales standard deviation | Store 14 | $317,570 |
| Highest relative weekly volatility (CV) | Store 35 | 22.97% |
| Second-highest CV | Store 7 | 19.73% |
| Third-highest CV | Store 15 | 19.34% |
| Fourth-highest CV | Store 29 | 18.37% |
| Fifth-highest CV | Store 23 | 17.97% |

Store 14 has the largest dollar swings, which is unsurprising for a large store. Store 35 is the more interesting operational risk: its weekly standard deviation is about $211K, but that represents almost 23% of its mean weekly sales.

The CV ranking is more suitable for identifying stores that may need tighter forecasting, flexible labour plans or inventory buffers relative to their own operating scale.

## External factors: small market-wide correlations

The analysis reports both pooled store-week correlations and a 143-observation weekly market view. The latter sums sales across stores and averages the store-level macro indicators for each date.

| Indicator | Store-week Pearson r | Weekly aggregate Pearson r | Weekly aggregate p-value |
|---|---:|---:|---:|
| Temperature | −0.064 | −0.159 | 0.058 |
| Fuel_Price | +0.009 | −0.057 | 0.501 |
| CPI | −0.073 | +0.023 | 0.781 |
| Unemployment | −0.106 | +0.004 | 0.967 |

At the market level, all four relationships are weak. Temperature is the largest negative association, but its p-value is just above the conventional 5% threshold. Fuel_Price, CPI and Unemployment are very close to zero in the aggregated view.

The raw store-week correlations resemble the supplied reference values for Temperature and Unemployment. CPI is slightly negative in the supplied rows (−0.073), not positive; in either direction the relationship is practically negligible.

The difference between the two correlation views is not a contradiction. The pooled view retains local store variation, while the weekly market view averages that variation away. Neither establishes causation.

### Macro indicators move together

In the weekly aggregate, CPI and Unemployment have a correlation of approximately **−0.98**; CPI and Fuel_Price are about **+0.83**, and Fuel_Price and Unemployment about **−0.75**. These relationships make it difficult to assign a clean independent effect to any one macro indicator in a short historical sample.

## Unemployment sensitivity: Store 42 is the clearest review candidate

### Primary specification

For each store, the primary model uses:

`Δlog(Weekly_Sales) ~ ΔUnemployment + ΔTemperature + ΔFuel_Price + ΔCPI + month controls`

Newey–West HAC standard errors use four lags. Benjamini–Hochberg adjustment is applied across the 45 store-level unemployment tests.

The five strongest negative coefficients in the weekly-change model are:

| Store | Unemployment coefficient | FDR-adjusted p-value |
|---:|---:|---:|
| 42 | **−0.689** | 0.0001 |
| 26 | −0.524 | 0.0003 |
| 40 | −0.521 | 0.0018 |
| 28 | −0.425 | <0.0001 |
| 41 | −0.387 | 0.0067 |

The coefficient is in log weekly-sales change per one-percentage-point change in unemployment, conditional on the other changes and month controls. For Store 42, the model-implied association for a 0.1 percentage-point rise is approximately −6.7% in weekly sales growth. This is a sensitivity illustration, not a forecast or causal estimate.

### Robustness check

A second specification uses macro indicator levels, a time trend and month controls. Store 42 remains the strongest negative coefficient (**−0.707**). This cross-specification consistency makes Store 42 the first store to investigate, while other store rankings are less stable across model forms.

### Why caution is essential

The market-average Unemployment series changes in only **11 of 142** week-to-week transitions. Much of the weekly change series is zero. The coefficient estimates are therefore driven by a limited number of macroeconomic change points. In addition, CPI, Fuel_Price, Unemployment and time are highly collinear. The model identifies an exposure pattern, not a causal unemployment elasticity.

A manager should validate Store 42 against local customer mix, category trends, competitor openings, promotions and store-specific conditions before taking action.

## Investigation queue: seven stores to review

A store is flagged when its February–October 2012 sales are below its February–October 2011 sales across the same 39 weekly dates, while its 2012 holiday weeks outperform its own 2012 non-holiday baseline.

| Store | 2012 vs 2011 like-for-like sales | 2012 holiday uplift |
|---:|---:|---:|
| 36 | **−17.47%** | +2.43% |
| 14 | −9.35% | +10.74% |
| 27 | −2.55% | +3.22% |
| 15 | −1.75% | +3.70% |
| 28 | −1.01% | +18.76% |
| 19 | −0.71% | +8.17% |
| 31 | −0.45% | +3.49% |

The most severe case is Store 36. Its positive holiday response shows that the store can participate in event demand, but it does not offset the wider like-for-like decline. Store 14 is also important: it is a Top 10 revenue store and has a 9.35% comparable-period decline despite positive holiday uplift.

## Five operational moves for a regional retail manager

### Protect Thanksgiving capacity first

Thanksgiving is the only event with a large, consistent uplift. Build the strongest inventory, replenishment and labour plan around the Thanksgiving trading window. Avoid copying the same uplift assumption into Christmas: Christmas is below the non-holiday baseline in this sample.

### Manage the network by tier, not by one universal target

The Top 10 generate 39.1% of sales, while the Bottom 10 contribute 8.6%. Use the Top tier to benchmark high-volume execution and the Bottom tier for targeted local-market diagnosis. Compare stores against peers of similar scale before assigning performance accountability.

### Create a volatility watchlist

Store 35, Store 7, Store 15, Store 29 and Store 23 have the highest relative volatility. Review forecast error, replenishment lead times, labour flexibility and category concentration at these stores. Track CV alongside standard deviation so large stores do not dominate the risk conversation.

### Separate holiday success from underlying recovery

The seven flagged stores show that a positive holiday response can coexist with declining comparable sales. Start with Store 36 and Store 14. Review non-holiday weeks, product availability, category mix and local competition rather than assuming that another holiday promotion will solve the underlying issue.

### Investigate Store 42's unemployment exposure without treating it as a causal verdict

Store 42 is the most consistent negative unemployment signal across the two model specifications. Compare its customer basket, local labour market, category mix and sales trend with similar stores. Use the regression as a prioritization tool, then validate with operational and local-market evidence.

## Method and limitations

- Source: the supplied `Walmart.csv` from the Kaggle Walmart dataset.
- Date parsing: explicit `%d-%m-%Y` format.
- Store panel: 45 stores × 143 weekly dates.
- Holiday event uplift: store-level mean holiday sales divided by the same store's non-holiday mean, less one.
- Confidence intervals: t-based 95% intervals across the 45 store-level event averages.
- Annual growth: raw annual pivot plus a comparable February–October 39-week view.
- Volatility: sample standard deviation and coefficient of variation.
- Macro correlation: pooled store-week and weekly aggregate Pearson correlation; the weekly aggregate p-values are reported with n = 143.
- Unemployment sensitivity: store-level first-difference OLS with month controls and four-lag HAC standard errors; Benjamini–Hochberg adjustment across 45 tests; second level model as a robustness check.

The dataset does not contain units sold, gross margin, inventory, promotion details, store size, local competition or customer demographics. It cannot identify causal drivers of sales or measure profit. The macro sensitivity estimates should be treated as descriptive risk signals for further investigation.
