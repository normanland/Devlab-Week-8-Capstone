# Compensation and Satisfaction Profiling

This project analyses employee compensation, job satisfaction and work-life balance in the supplied IBM HR Analytics dataset. Its focus is pay architecture and employee experience; attrition analysis is intentionally excluded.

## Project files

```text
HR compensation and satisfaction/
├── HR Compensation and Satisfaction Analysis.ipynb
├── README.md
├── note.md
```

All charts are rendered and stored **inside the executed Jupyter notebook**. Analytical tables are calculated and displayed in the relevant notebook sections. The project does not create separate `visuals`, `output csv`, PNG or CSV export folders.

## Dataset

**Source file:** `WA_Fn-UseC_-HR-Employee-Attrition.csv`

**Expected location on the user's computer:**

```text
C:\Users\anarrasulzada\Desktop\WA_Fn-UseC_-HR-Employee-Attrition.csv
```

The supplied file contains 1,470 employee records and 35 source columns. It covers three departments, nine job roles and five job levels. The source has no missing cells or duplicate rows, and all 1,470 employee numbers are unique.

The notebook reads the CSV directly with `pd.read_csv`. The employee is the unit of analysis, so each employee contributes one observation to each relevant compensation and experience calculation.

### Fields used

| Field | Analytical role |
|---|---|
| `Department` | Department benchmarking |
| `JobRole` | Role-level compensation |
| `JobLevel` | Compensation hierarchy |
| `Gender` | Descriptive pay comparison |
| `MonthlyIncome` | Compensation measure |
| `JobSatisfaction` | Four-point satisfaction distribution |
| `WorkLifeBalance` | Four-point work-life balance distribution |
| `OverTime` | Overtime group comparison |
| `YearsAtCompany` | Tenure correlation |
| `PercentSalaryHike` | Salary increase correlation |
| `TrainingTimesLastYear` | Training correlation |
| `EnvironmentSatisfaction` | Additional satisfaction context |

Five source columns are excluded from the scoped analytical table: `Attrition` is outside the project scope; `EmployeeNumber` is an identifier; `EmployeeCount`, `Over18` and `StandardHours` are constant fields with no analytical variation.

## Environment and execution

The notebook is intended for Visual Studio Code with the Jupyter extension and a Python 3 kernel.

Install the required packages:

```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels jupyter ipykernel
```

Open `HR Compensation and Satisfaction Analysis.ipynb`, select a Python 3 kernel, and run all cells from top to bottom. The source CSV must be present at the Desktop path above. The notebook calculates the tables and renders all 11 charts inline.

The data-loading step is a direct `pd.read_csv` call. No `if/else` path-selection logic is used.

## Analytical workflow

### Compensation structure

- Median MonthlyIncome by Department, JobRole, JobLevel and Gender.
- Department × JobLevel median-income pivot.
- Employee counts alongside medians, so small senior-level groups remain visible.
- Highest-to-lowest JobRole median pay ratio within each department.
- Income distribution by job level and the relationship between JobLevel and MonthlyIncome.

### Satisfaction and work-life balance

- Overall JobSatisfaction distribution from 1 to 4.
- Department-level satisfaction composition.
- Low-satisfaction flag: the share of employees with JobSatisfaction equal to 1 or 2.
- Overall and department-level WorkLifeBalance distributions.
- Department action flag when WorkLifeBalance equals 1 at a rate above the company average.
- Overtime comparison for average JobSatisfaction and WorkLifeBalance.

### Additional analysis

- Pearson and Spearman correlations with JobSatisfaction.
- Chi-square tests, Cramer's V and Kruskal–Wallis comparisons across departments.
- Income quintiles compared with average satisfaction and low-satisfaction share.
- Gender median comparisons within JobRole.
- Exploratory log-income regression adjusted for Department, JobLevel and JobRole, with HC3 robust standard errors.

## Main findings

- Company median MonthlyIncome is **4,919** dataset units; the mean is **6,503**. The right-skewed income distribution makes the median a more stable benchmark.
- Sales has the highest department median at **5,754.5**, followed by Research & Development at **4,374** and Human Resources at **3,886**.
- JobLevel and MonthlyIncome have a strong positive Pearson correlation of **0.950**.
- The highest-to-lowest role median pay ratios range from **6.08 to 6.61** across departments.
- **38.71%** of employees have JobSatisfaction scores of 1 or 2. Human Resources has the highest descriptive share at **49.21%**, but its sample is only 63 employees and the department-level satisfaction test is not statistically strong.
- WorkLifeBalance score 3 is the largest category, covering **60.75%** of employees. Human Resources and Research & Development have WorkLifeBalance = 1 shares above the company reference.
- The requested numeric factors have correlations with JobSatisfaction close to zero.
- Overtime groups have very similar average experience scores; the observed differences are small and statistically uncertain.
- The adjusted gender coefficient is approximately **+0.21%** for men relative to women, with **p = 0.863**. This exploratory model does not identify a statistically distinguishable overall gender difference after its included controls.

The detailed methodology, exact department figures, caveats and four compensation and benefits insights are in `note.md`.

## Deliverables

- `HR Compensation and Satisfaction Analysis.ipynb` — executed notebook with 24 code cells, displayed outputs, analytical tables and 11 inline charts.
- `note.md` — methodology, findings, limitations and recommendations.
- `README.md` — dataset, setup, scope and execution guide.
- `requirements.txt` — Python package list.

## Interpretation boundaries

MonthlyIncome has no currency metadata in the supplied file, so the project reports dataset units rather than assuming a currency. Group medians are descriptive benchmarks, not salary bands or job valuation recommendations.

Satisfaction and work-life balance are ordinal survey scores. Their averages are convenient summaries, but the distributions and low-score shares remain central to interpretation. Correlations and group tests describe associations in this dataset; they do not establish causality.

The adjusted gender model is exploratory and is not a formal equal-pay audit. It does not include every factor that can affect compensation, such as performance, location, working hours, prior experience or pay history. Small department and role groups require additional caution.
