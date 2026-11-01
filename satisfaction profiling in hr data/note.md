# Pay architecture and employee experience: an evidence-led HR review

## Executive view

This dataset contains 1,470 employee records across Human Resources, Research & Development and Sales. The central finding is a clear separation between two systems:

- Compensation follows the organizational ladder. Job level is strongly associated with monthly income.
- Satisfaction does not follow the same ladder. The requested pay, tenure, salary-hike, job-level and training variables have almost no linear relationship with JobSatisfaction.

The most useful HR response is therefore not a single compensation adjustment. It is a combined review of pay architecture, role-level pay dispersion and the employee experience signals inside departments.

Attrition is outside the scope of this analysis. The source `Attrition` field was excluded before analytical work.

## Source integrity and scope

| Data check | Result |
|---|---:|
| Employee records | 1,470 |
| Source columns | 35 |
| Missing cells | 0 |
| Duplicate rows | 0 |
| Unique employee numbers | 1,470 |
| Departments | 3 |
| Job roles | 9 |
| Job levels | 5 |

The department populations are uneven:

| Department | Employees | Share of dataset |
|---|---:|---:|
| Research & Development | 961 | 65.37% |
| Sales | 446 | 30.34% |
| Human Resources | 63 | 4.29% |

The employee is the unit of analysis. Compensation medians are calculated from one MonthlyIncome value per employee. No department or job-role average is weighted by repeated observations.

### Fields removed from the analysis

- `Attrition` — outside the requested compensation and satisfaction scope.
- `EmployeeNumber` — employee identifier, not an analytical measure.
- `EmployeeCount` — constant value.
- `Over18` — constant value.
- `StandardHours` — constant value.

All other source fields remain available in the original `raw` DataFrame, while the scoped `hr` DataFrame contains the fields used in the analysis.

## Compensation: the median changes the story

The overall median monthly income is **4,919** dataset units, compared with a mean of **6,503**. The mean is approximately 32.2% higher than the median, and the income distribution has a positive skew of **1.37**. A relatively small number of senior and high-income records pull the mean upward.

The source does not declare a currency. For that reason, the report uses dataset units rather than attaching a dollar sign.

### Department benchmark

| Department | Employees | Median income | Mean income |
|---|---:|---:|---:|
| Sales | 446 | **5,754.5** | 6,959 |
| Research & Development | 961 | **4,374** | 6,281 |
| Human Resources | 63 | **3,886** | 6,655 |

Human Resources illustrates why median is the more useful central benchmark. Its mean is the highest of the three departments, while its median is the lowest. The 11 managers in the HR department have a median income of 18,844, creating a strong upward pull on the department mean.

The supplied reference note listed different department medians (R&D 5,420, Sales 4,975 and HR 4,800). Those values are not reproduced from the attached CSV. All figures in this report are recalculated from the actual 1,470 rows in the supplied file.

### The job-level ladder

| Job level | Employees | Median income |
|---:|---:|---:|
| 1 | 543 | 2,670 |
| 2 | 534 | 5,340 |
| 3 | 218 | 9,980 |
| 4 | 106 | 16,154 |
| 5 | 69 | 19,232 |

The Pearson correlation between JobLevel and MonthlyIncome is **0.950**. The median rises at every level, although the step between levels 4 and 5 is smaller than the earlier jumps.

The Department × JobLevel heatmap adds an important qualification: sample sizes become much smaller at senior levels. Human Resources has only four employees at level 4 and seven at level 5. Those medians are informative as observations, but they should not be treated as stable market benchmarks.

### Role-level spread within departments

The bonus pay-gap ratio is defined as:

`highest JobRole median income within department / lowest JobRole median income within department`

| Department | Lowest median role | Highest median role | Ratio |
|---|---|---|---:|
| Human Resources | Human Resources · 3,093 | Manager · 18,844 | **6.09×** |
| Research & Development | Laboratory Technician · 2,886 | Manager · 17,545.5 | **6.08×** |
| Sales | Sales Representative · 2,579 | Manager · 17,048 | **6.61×** |

These ratios describe the breadth of the role hierarchy. They are not evidence of inequity by themselves: job scope, seniority and accountability differ between roles. Their value is in identifying where the compensation architecture has the widest internal spread.

## Gender comparison: raw medians and adjusted estimates

The overall gender medians are 5,081.5 for women (n = 588) and 4,837.5 for men (n = 882). This raw comparison is not adjusted for department or role composition.

Department-level medians differ by gender:

| Department | Female median | Male median | Female vs male |
|---|---:|---:|---:|
| Human Resources | 4,313.5 | 3,886 | +11.0% |
| Research & Development | 4,615 | 4,174.5 | +10.6% |
| Sales | 5,666 | 6,134 | −7.6% |

Role-level comparisons reveal more variation. The largest raw difference is in Research Director, where the female median is 14,275 and the male median is 17,584, a female-to-male median difference of **−18.8%**. The role contains 33 women and 47 men.

A separate exploratory model uses log MonthlyIncome as the outcome and controls for Department, JobLevel and JobRole. Its male coefficient corresponds to an adjusted difference of approximately **+0.21%**, with an HC3 robust p-value of **0.863**.

The raw role gaps and the adjusted overall estimate answer different questions. Differences in role and level composition can change the unadjusted picture. The adjusted result does not establish that every role is equitable; it indicates that this model does not detect an overall gender difference after the included controls. A formal pay-equity audit would require richer job, performance, location and pay-history information.

## Satisfaction: the low-score share deserves attention

The overall JobSatisfaction distribution is:

| Score | Employees | Share |
|---:|---:|---:|
| 1 | 289 | 19.66% |
| 2 | 280 | 19.05% |
| 3 | 442 | 30.07% |
| 4 | 459 | 31.22% |

Scores 1 and 2 together account for **569 employees**, or **38.71%** of the dataset.

### Department-level low satisfaction

| Department | Employees | Scores 1–2 | Low-satisfaction share |
|---|---:|---:|---:|
| Human Resources | 63 | 31 | **49.21%** |
| Research & Development | 961 | 366 | **38.09%** |
| Sales | 446 | 172 | **38.57%** |

Human Resources has the highest observed low-satisfaction share. Its 95% Wilson interval is approximately **37.27% to 61.24%**, reflecting the uncertainty from a small department sample.

The department-by-satisfaction chi-square test has p = **0.202** and Cramer's V = **0.054**. The Kruskal–Wallis test has p = **0.545**. The descriptive HR gap is worth monitoring, but the available evidence does not support a strong claim that satisfaction distributions differ by department.

## Work-life balance: two departments sit above the company reference

The overall WorkLifeBalance profile:

| Score | Dataset label | Employees | Share |
|---:|---|---:|---:|
| 1 | Bad | 80 | 5.44% |
| 2 | Good | 344 | 23.40% |
| 3 | Better | 893 | **60.75%** |
| 4 | Best | 153 | 10.41% |

Score 3 is the most common category. The company-wide share at score 1 is **5.44%**.

| Department | Score 1 employees | Score 1 share | Difference vs company |
|---|---:|---:|---:|
| Human Resources | 4 of 63 | **6.35%** | +0.91 pp |
| Research & Development | 60 of 961 | **6.24%** | +0.80 pp |
| Sales | 16 of 446 | **3.59%** | −1.85 pp |

Human Resources and Research & Development meet the requested action-flag rule because their score-1 shares are above the company average. The interpretation differs by scale: HR has the highest rate but only four employees in the category; R&D has a similar rate and 60 employees, making it the larger operational population.

The WorkLifeBalance department comparison has a chi-square p-value of **0.052**, Cramer's V of **0.065**, and a Kruskal–Wallis p-value of **0.013**. The ordinal test detects a distributional difference, but the effect size is small. This supports targeted follow-up rather than a broad claim of severe department-level imbalance.

## Pay and satisfaction do not move together

The requested Pearson correlations with JobSatisfaction are all close to zero:

| Factor | Pearson r |
|---|---:|
| PercentSalaryHike | +0.0200 |
| MonthlyIncome | −0.0072 |
| EnvironmentSatisfaction | −0.0068 |
| TrainingTimesLastYear | −0.0058 |
| YearsAtCompany | −0.0038 |
| JobLevel | −0.0019 |

Spearman correlations are similarly close to zero. YearsAtCompany has virtually no monotonic relationship with JobSatisfaction in this file. EnvironmentSatisfaction also has a near-zero relationship (r = −0.0068), rather than the positive value in the supplied reference note.

The income-quintile analysis makes the same point in a more operational form:

| Income group | Median income | Average satisfaction | Low-satisfaction share |
|---|---:|---:|---:|
| Lowest income | 2,316 | 2.72 | 40.14% |
| Lower-middle | 3,315.5 | 2.73 | 37.76% |
| Middle | 4,919 | 2.68 | 39.12% |
| Upper-middle | 6,888 | 2.82 | 35.71% |
| Highest income | 13,798 | 2.68 | **40.82%** |

The highest-paid fifth has the highest low-satisfaction share. The relationship is not monotonic, so higher pay alone is not a reliable proxy for better employee experience.

## Overtime: small differences, no strong evidence

| Overtime | Employees | Average JobSatisfaction | Average WorkLifeBalance |
|---|---:|---:|---:|
| No | 1,054 | 2.712 | 2.773 |
| Yes | 416 | 2.772 | 2.731 |

Employees with overtime have a 0.060-point higher average JobSatisfaction score and a 0.042-point lower average WorkLifeBalance score. Both differences are small.

Welch test p-values are **0.353** for JobSatisfaction and **0.293** for WorkLifeBalance. Mann–Whitney p-values are **0.274** and **0.248**, respectively. The evidence does not support a meaningful group difference in this sample.

## Four insights for the compensation and benefits team

### The pay architecture is level-led, not department-led

JobLevel and MonthlyIncome correlate at **r = 0.950**, and median pay rises from 2,670 at level 1 to 19,232 at level 5. Department medians alone hide role mix: Human Resources has the lowest median but the highest mean because of a small number of senior roles. Compensation reviews should therefore benchmark employees by job family and level before comparing departments.

### Human Resources has the clearest satisfaction warning, but the sample is small

Almost half of HR employees (49.21%) report satisfaction scores of 1 or 2, compared with 38.71% company-wide. The 63-person sample creates a wide confidence interval, and the department-level test is not statistically strong. A focused pulse check is more defensible than treating this as a confirmed department-wide problem.

### Work-life balance follow-up should cover both R&D and HR

Both departments exceed the company reference for WorkLifeBalance = 1. R&D has the larger affected population: 60 employees, compared with four in HR. R&D is therefore the larger operational priority, while HR's higher rate warrants a smaller, targeted review.

### Compensation increases alone are unlikely to close satisfaction gaps

The requested pay and career variables have near-zero correlations with JobSatisfaction. The highest income quintile still has a 40.82% low-satisfaction share. The benefits agenda should include workload, manager support, role clarity, flexibility and work environment rather than relying on salary movement as the only lever.

## Additional review signal: role-level gender differences

The Research Director median gap of −18.8% for women is a useful audit lead, not a conclusion. The overall adjusted gender coefficient is small and statistically uncertain. A deeper review would compare like-for-like role scope, job level, tenure, performance ratings, location and pay history before reaching an equity conclusion.

## Methodology and limitations

- **Grain:** one row per employee.
- **Median compensation:** median MonthlyIncome within each requested grouping.
- **Compensation pivot:** Department × JobLevel with median MonthlyIncome.
- **Role pay gap ratio:** maximum JobRole median divided by minimum JobRole median within Department.
- **Low satisfaction:** JobSatisfaction in {1, 2}; department share calculated against all employees in that department.
- **Work-life action flag:** department WorkLifeBalance = 1 share compared with the company-wide share.
- **Correlation:** Pearson as required, with Spearman as a rank-based companion.
- **Distribution tests:** chi-square with Cramer's V and Kruskal–Wallis.
- **Overtime comparison:** group means, Welch tests and Mann–Whitney tests.
- **Gender model:** exploratory OLS on log MonthlyIncome, controlling for Department, JobLevel and JobRole, with HC3 robust standard errors.

The data is cross-sectional and contains no salary history, job descriptions, location, hours worked, manager quality or complete performance context. Ordinal satisfaction scores should be interpreted through both their distributions and their group summaries. None of the relationships in this notebook establishes causality.

## Project contents

The complete analysis, calculated tables and all visualizations are contained in `HR Compensation and Satisfaction Analysis.ipynb`. The notebook has no separate PNG or CSV export deliverables.
