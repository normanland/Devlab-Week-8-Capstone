# Walmart Retail Performance and Risk Intelligence

A weekly retail performance study of the 45-store Walmart network. The analysis looks beyond total revenue to distinguish store scale, holiday response, like-for-like movement, sales volatility and exposure to changing economic conditions.

The project is organized around the folders already used in the working directory: `visuals` contains the seven chart exports, while `output csv` contains the thirteen analytical tables.

## Project structure

```text
walmart retail analytics/
├── walmart retail analytics.ipynb
├── README.md
├── note.md
├── output csv/
│   ├── holiday date sales.csv
│   ├── holiday uplift by type.csv
│   ├── macro correlation comparison.csv
│   ├── monthly sales trend.csv
│   ├── store like for like growth.csv
│   ├── store performance and tiers.csv
│   ├── store tier contribution.csv
│   ├── store unemployment sensitivity.csv
│   ├── store volatility ranking.csv
│   ├── store year sales pivot.csv
│   ├── store year yoy growth.csv
│   ├── stores for investigation.csv
│   └── unemployment model robustness.csv
└── visuals/
    ├── holiday uplift by event.png
    ├── macro correlation comparison.png
    ├── monthly sales rhythm.png
    ├── store revenue tiers.png
    ├── store volatility profile.png
    ├── store year sales heatmap.png
    └── unemployment sensitivity.png
```

All words in the notebook, PNG and CSV filenames are separated with ordinary spaces. There are no hyphens, underscores or numbering prefixes in those filenames.

## Dataset and location

The notebook reads the supplied Walmart dataset from this location:

```text
C:\Users\anarrasulzada\Desktop\Walmart.csv
```

The dataset is expected to remain on the Windows Desktop; it is not duplicated inside the project folder. The source contains 6,435 store-week records for 45 stores over 143 weekly dates, from 5 February 2010 to 26 October 2012.

The fields used are:

| Field | Analytical role |
|---|---|
| `Store` | Store identifier |
| `Date` | Weekly observation date |
| `Weekly_Sales` | Weekly store sales |
| `Holiday_Flag` | Holiday-associated week indicator |
| `Temperature` | Store-week temperature |
| `Fuel_Price` | Store-week fuel price |
| `CPI` | Consumer price index |
| `Unemployment` | Unemployment rate |

## Running the notebook in VS Code

1. Keep `walmart retail analytics.ipynb`, `visuals` and `output csv` together in one project folder.
2. Confirm that `Walmart.csv` is located on the Desktop at the path shown above.
3. Open the project folder in Visual Studio Code.
4. Open `walmart retail analytics.ipynb` and select a Python Jupyter kernel with the required packages installed.
5. Run the notebook from top to bottom.

The notebook creates `visuals` and `output csv` if they do not already exist. Run it with the project folder as the notebook working directory so the exported files are written into the expected locations.

Required Python packages:

```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels jupyter ipykernel
```

## Analysis workflow

The notebook follows a single reproducible workflow:

- Source inspection and data-quality checks, including missing values, duplicate store-date keys and panel completeness.
- Date parsing and chronological sorting by store and week.
- Store ranking by cumulative sales, with Top 10, Mid 25 and Bottom 10 tiers.
- Holiday comparison at both network level and store-normalized event level.
- Monthly network sales trend and an annual Store × Year pivot.
- Like-for-like annual comparison using the common February–October window.
- Store volatility analysis using standard deviation and coefficient of variation.
- Pearson correlation analysis for the four external indicators.
- Store-level unemployment sensitivity modelling with first differences, HAC standard errors and a multiple-testing adjustment.
- An investigation queue for stores with declining comparable-period sales despite positive holiday uplift.

## Main findings

- The network recorded **$6.737 billion** in sales across the observed period.
- Store 20 was the largest contributor at **$301.40 million**; Store 33 was the smallest at **$37.16 million**.
- The Top 10 stores generated **39.05%** of network sales; the Bottom 10 generated **8.61%**.
- Holiday-flagged store-weeks averaged **7.84%** more sales than non-holiday store-weeks.
- Thanksgiving had the strongest store-normalized uplift at **38.40%**. Christmas was below the store-level non-holiday baseline at **−7.39%**.
- December 2010 was the strongest month by total sales at **$288.76 million**.
- Store 35 had the highest relative weekly volatility, with a coefficient of variation of **22.97%**.
- At the weekly market level, the four macroeconomic indicators had weak simple correlations with total sales.
- Store 42 was the clearest negative unemployment-sensitivity signal across the two model specifications.
- Seven stores had negative February–October 2012 like-for-like sales growth despite positive 2012 holiday uplift.

Further definitions, detailed tables, caveats and the five operational recommendations are documented in `note.md`.

## Deliverables

- `walmart retail analytics.ipynb` — executed notebook with code, tables and seven embedded charts.
- `visuals/` — seven standalone PNG exports.
- `output csv/` — thirteen analytical CSV exports.
- `note.md` — detailed methodology, findings, limitations and operational insights.

## Interpretation limits

Weekly sales are not profit. The dataset does not include units sold, margin, inventory, promotions, store size, operating hours, local competition or customer demographics. Holiday uplift and macroeconomic relationships are descriptive rather than causal. The first and final years are partial, so raw annual totals and growth rates require the like-for-like comparison alongside them.