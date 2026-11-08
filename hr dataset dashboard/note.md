# Methodology Note – HR Attrition Capstone (SQL + Tableau)

## 1. Dataset provenance
- **Source:** IBM HR Analytics Employee Attrition & Performance (Kaggle, `pavansubhasht/ibm-hr-analytics-attrition-dataset`), file `WA Fn-UseC -HR-Employee-Attrition.csv`. This is the dataset named in the brief. No substitute was used.
- **Location in project:** `data/WA Fn-UseC -HR-Employee-Attrition.csv`, copied unchanged from the user's `projects_datasets` folder. No records were modified, imputed or removed.
- **Nature:** synthetic data created by IBM data scientists. One row per employee, 35 columns, a single snapshot with no dates.
- **Validation (Q2, `outputs/q02a validation counts.csv`, `outputs/q02b validation nulls.csv`):** 1470 rows, 1470 distinct EmployeeNumber values, 0 NULLs in every column, 237 leavers and 1233 stayers, overall attrition 16.12%, 0 invalid Attrition labels. Every expected checkpoint matched the actual data.

## 2. Tool substitution: Power BI → Tableau
The brief specifies Power BI. The visual layer was delivered in **Tableau** (Tableau Public 2026.2). The SQL layer and the written deliverables follow the brief unchanged.

| Power BI requirement | Tableau deliverable |
|---|---|
| `.pbix` | `hr attrition.twbx` (packaged, extracts embedded) + editable `tableau/hr attrition.twb` |
| Import table / SQL views | Data source **HR Attrition (SQL enriched)** = extract of SQL view `v_employees_enriched`. Data source **Risk Profiles (SQL Q11)** = extract of SQL view `v_risk_profiles` |
| Model view screenshot | Single flat extract table, described in §10 (open the Data Source tab in the workbook) |
| Banding columns | Already computed in SQL (`TenureBand`, `band_order`, `IncomeQuartile`). Not recomputed in Tableau |
| Explicit DAX measures using DIVIDE | Calculated fields (`tableau/measures.md`). DIVIDE becomes `IF COUNT(...) = 0 THEN NULL ELSE ... END` |
| CALCULATE / filter context | Aggregate calculated fields re-evaluated per mark and per filter state |
| KPI cards | KPI worksheets on both dashboards |
| Matrix with conditional formatting | Highlight table Department × JobSatisfaction with a sequential amber→red scale |
| Slicers | Shared filters on Department, JobRole, OverTime, TenureBand and IncomeQuartile (dropdown cards on Segment Explorer) |
| Cross-filtering | Filter actions: Department bar → Executive Overview; segment row → Segment Explorer |
| Decomposition tree / tooltip page (bonus) | Not built |

## 3. Why SQL does the analysis and Tableau does the presentation
- **SQL is the single source of analytical truth.** Banding, quartiles, pivots, thresholds and ranking are deterministic, reviewable and versionable in one file (`queries.sql`). Each query carries its real output as a comment.
- **Tableau is the interaction layer.** It aggregates the SQL-enriched rows on the fly so an HR user can slice any combination. It never re-derives a band or quartile, which removes the main source of SQL/BI disagreement.
- **Python only orchestrates.** `build db.py` loads the CSV and runs the DDL and validation blocks from `queries.sql`. `run queries.py` executes every query block, exports results, embeds outputs and writes the log. `tableau/make extracts.py` copies the SQL exports into Tableau `.hyper` extracts. `tableau/build workbook.py` writes the workbook XML. None of these scripts contains analytical SQL or pandas aggregation.

## 4. SQL engine and loading process
- **Engine:** SQLite 3.50.4 through Python 3.14's built-in `sqlite3`. It needs no installation and supports window functions (NTILE, RANK).
- **Load:**
  1. `setup_ddl` creates `employees` with explicit types, `NOT NULL`, a `CHECK` on Attrition and `EmployeeNumber` as the primary key.
  2. `build db.py` bulk-inserts the CSV. The file starts with a UTF-8 BOM, so it is read with `utf-8-sig`.
  3. `setup_flag` adds `attrition_flag = CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END`.
  4. `setup_views` creates `v_employees_enriched` and `v_risk_profiles`.
- **Rate formula everywhere:** `ROUND(100.0 * SUM(attrition_flag) / NULLIF(COUNT(*), 0), 2)`. `100.0` forces real division, `NULLIF` prevents division by zero, and rounding is to 2 dp.
- **Execution log:** `outputs/sql execution log.txt` records the engine, the command, each block's status and row count, the re-execution check and the validation results.

## 5. Banding choices
**Tenure bands (YearsAtCompany): 0-2, 3-5, 6-10, 11+.**
- 0–2 years: onboarding and "wrong fit" exits.
- 3–5 years: the first promotion window.
- 6–10 years: established staff.
- 11+ years: long-service staff.

The band sizes are 342 / 434 / 448 / 246, all large enough for stable rates. `band_order` (1–4) gives a chronological sort in Tableau.

**Income quartiles:** `NTILE(4)` on MonthlyIncome rather than fixed salary brackets. Quartiles give four near-equal groups (368 / 368 / 367 / 367), so every rate rests on similar evidence. Fixed brackets would give arbitrary, uneven groups.

**Deterministic tie-break:** quartile 1 ends at 2911 and quartile 2 starts at 2911. A plain `ORDER BY MonthlyIncome` could assign the tied employees differently between runs. Adding `EmployeeNumber` makes the assignment reproducible. Bands are computed once in `v_employees_enriched` and exported, so SQL and Tableau always agree.

## 6. Minimum-headcount thresholds
| Where | Threshold | Effect |
|---|---|---|
| Q5 and Tableau *Rate by Job Role* | ≥ 30 | All 9 roles pass (smallest is Human Resources, 52). The filter stays in place in case the data changes |
| Q11 and Executive *Top Risk Profiles* | ≥ 20 | 26 of 32 possible combinations kept. Profile 3 (22 people) sits near the floor and is flagged in the summary |
| Tableau *Ranked Segments* | ≥ 20 | Removes Department × Job Role cells too small to rank |

Pivots (Q9 and Q10) keep all cells and show the cell headcount (`*_n`) beside each rate, so small cells are visible rather than hidden.

## 7. Tableau implementation
- **Workbook:** `hr attrition.twbx` (packaged) and `tableau/hr attrition.twb` (editable). Both are produced by `python tableau/build workbook.py`.
- **Data sources:** two Tableau `.hyper` extracts built by `tableau/make extracts.py`.
  - The script uses the Hyper engine that ships with Tableau Public (`hyperd.exe`).
  - It loads the SQL-exported CSVs unchanged with `COPY` and checks the row counts (1470 and 26).
  - Tableau Public refuses to open workbooks with live file connections ("Workbooks saved to Tableau Public must use extracts"), so extracts are required.
- **Calculated fields:** see `tableau/measures.md`.
- **Dashboards (1366 × 768, fixed):**
  1. **Executive Overview:** 4 KPI cards; attrition by department and by job role (≥ 30), coloured on a continuous amber→red risk scale; tenure-band columns (teal) in band order; Department × JobSatisfaction risk matrix; top-3 risk profiles from Q11.
  2. **Segment Explorer:** 5 dropdown filters; 4 KPI cards; segments ranked by attrition rate (≥ 20 employees); attrition by tenure band, pay quartile and overtime.
  3. **SQL Cross-Validation:** Tableau-computed headcount, attritions and rate by overtime, department and tenure band, next to the SQL reference values.
- **Design system (redesign of 2026-11-07, following the three reference images):**
  - **Colours:** warm ivory background `#F8F5EF` with white rounded cards (Tableau rounded-corner zones). Dark-teal `#075E5A` section bands with white titles and icons. Mint `#E4F2ED` KPI cards; the Attrition Rate card uses an amber tint for emphasis. Navy `#14243D` values, slate `#64748B` captions.
  - **Risk scale:** a continuous amber `#F4B64C` → orange `#E98B32` → red `#D62828` scale on the department and job-role bars, the risk matrix and the ranked-segment rate column. Teal `#087F78` columns for neutral measures. Gridlines and zero lines are switched off workbook-wide.
  - **Images:** small decorative PNGs only (logo tiles, KPI and section icons, PASS badges, header wave), rendered by `tableau/make assets.py` from the Windows Segoe MDL2 icon font and packaged in the `.twbx` under `Image/`. Every chart and table is a native Tableau mark.
  - **Validation copy:** the SQL Cross-Validation panels use a separate, unfiltered copy of the data source, **HR Attrition (validation copy)**. It reads `employees enriched validation.hyper`, an identical file copy. Segment Explorer filters therefore cannot alter the validated figures.
  - **Static PASS badges:** the PASS badges and SQL reference values on that page are static text. They record the comparison in §9, whose figures Tableau still computes live in the panels above them.
- **How it was tested:** every dashboard was opened in Tableau Public 2026.2 on this machine and captured with a window screenshot (`screenshots/`). The filter tests used copies of the workbook with one shared filter pre-set (generated with `python tableau/build workbook.py --variant ot_yes|sales|tenure02`). These differ from the main workbook only in that filter value and the opening tab.

## 8. SQL ↔ Tableau cross-validation (measured)
The Tableau values were read from Tableau's own rendering in two independent ways:
- **(a)** the *SQL Cross-Validation* dashboard, which groups by each dimension (`screenshots/sql cross validation.png`);
- **(b)** the *Segment Explorer* KPI cards with the shared filter set to the segment (`screenshots/validation overtime yes.png`, `screenshots/validation department sales.png`, `screenshots/validation tenure 0-2.png`).

Both methods gave the same numbers.

| Segment | SQL headcount | Tableau headcount | SQL attritions | Tableau attritions | SQL rate | Tableau rate | Difference | Result | SQL source |
|---|---|---|---|---|---|---|---|---|---|
| OverTime = Yes | 416 | 416 | 127 | 127 | 30.53% | 30.53% | 0 / 0 / 0.00 pp | **PASS** | `q06 rate by demographics.csv` |
| Department = Sales | 446 | 446 | 92 | 92 | 20.63% | 20.63% | 0 / 0 / 0.00 pp | **PASS** | `q04 rate by department.csv` |
| TenureBand = 0-2 | 342 | 342 | 102 | 102 | 29.82% | 29.82% | 0 / 0 / 0.00 pp | **PASS** | `q07 rate by tenure band.csv` |

Additional agreement visible in the same captures:
- Overall: 1,470 / 237 / 16.12% (Q3).
- Every department, tenure-band and overtime row on the cross-validation dashboard.
- All 12 risk-matrix cells (Q9).
- Pay-quartile rates 29.35 / 14.13 / 10.63 / 10.35% (Q8).

The counts match exactly, so the equal rates are not a rounding artefact.

## 9. Model view
The Tableau model is a single flat table: **HR Attrition (SQL enriched)**, an extract of the SQL view `v_employees_enriched`, with 1,470 rows. Two more sources sit alongside it: **Risk Profiles (SQL Q11)** and an unfiltered validation copy. There are no joins or relationships. Open `hr attrition.twbx` and click the **Data Source** tab to see it.

## 10. Assumptions
- MonthlyIncome is used as given. No currency is stated in the dataset, so no currency symbol is shown.
- JobSatisfaction and WorkLifeBalance are treated as ordinal 1–4 categories, not continuous scores.
- "Tenure" means YearsAtCompany, not TotalWorkingYears or YearsInCurrentRole.
- The company rate (16.12%) is the reference for "elevated" risk.

## 11. Reproducibility
Run these commands from the project folder:
```bash
python run queries.py                 # rebuild hr.db, run Q1–Q12, embed outputs, export CSVs + log
python tableau/make extracts.py       # build .hyper extracts (needs Tableau Public 2026.2 installed)
python tableau/build workbook.py      # write tableau/hr attrition.twb and hr attrition.twbx
```

Then open `hr attrition.twbx` in Tableau Public or Tableau Desktop. Re-running is idempotent: the embedded output comments are replaced, not duplicated.
