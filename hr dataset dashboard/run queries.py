"""Rebuild hr.db, run every query block in queries.sql, export results, and
embed the actual results as SQL comments under each query.

Steps
  1. build_db.main()       -> rebuilds hr.db from the CSV and validates it (exits on failure)
  2. run every q* block    -> outputs/<block_name>.csv
  3. embed outputs         -> rewrites queries.sql, placing an
                              "ACTUAL EXECUTION OUTPUT" comment block under each query
                              (old output blocks are replaced, so re-running is idempotent)
  4. re-execute            -> re-reads the rewritten queries.sql, runs every block again and
                              checks the results are identical (proves the file still executes)
  5. Tableau extracts      -> tableau/employees enriched.csv, tableau/risk profiles.csv
  6. log                   -> outputs/sql execution log.txt

No analytical logic lives here: every number comes from SQL in queries.sql.
"""
import csv
import datetime as dt
import platform
import re
import sqlite3
import sys
from pathlib import Path

import importlib.util

_spec = importlib.util.spec_from_file_location("build_db", Path(__file__).resolve().parent / "build db.py")
build_db = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build_db)

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "outputs"
TABLEAU_DIR = ROOT / "tableau"
SQL_PATH = build_db.SQL_PATH
LOG_PATH = OUT_DIR / "sql execution log.txt"

OUT_START = "-- ==========================================================\n-- ACTUAL EXECUTION OUTPUT"
OUT_BLOCK_RE = re.compile(
    r"\n*-- =+\n-- ACTUAL EXECUTION OUTPUT\n(?:--.*\n)*?-- =+\n?", re.MULTILINE
)


def fmt(v) -> str:
    if v is None:
        return "NULL"
    if isinstance(v, float):
        return repr(round(v, 4)) if v != int(v) else f"{v:.1f}"
    return str(v)


def table_comment(header, rows, extra=None) -> str:
    """Render a result set as an aligned, pipe-separated SQL comment block."""
    cells = [list(header)] + [[fmt(v) for v in r] for r in rows]
    widths = [max(len(row[i]) for row in cells) for i in range(len(header))]
    line = lambda row: "-- " + " | ".join(c.ljust(w) for c, w in zip(row, widths)).rstrip()
    out = [
        "-- ==========================================================",
        "-- ACTUAL EXECUTION OUTPUT",
        f"-- Executed against: hr.db (SQLite {sqlite3.sqlite_version})",
        "-- Status: SUCCESS",
        f"-- Rows returned: {len(rows)}",
    ]
    out += [f"-- {e}" for e in (extra or [])]
    out.append("--")
    out.append(line(cells[0]))
    out.append("-- " + "-+-".join("-" * w for w in widths))
    out += [line(r) for r in cells[1:]]
    out.append("-- ==========================================================")
    return "\n".join(out)


def status_comment(lines) -> str:
    return "\n".join(
        ["-- ==========================================================",
         "-- ACTUAL EXECUTION OUTPUT",
         f"-- Executed against: hr.db (SQLite {sqlite3.sqlite_version})"]
        + [f"-- {l}" for l in lines]
        + ["-- =========================================================="]
    )


def run_block(con, sql):
    cur = con.execute(sql)
    return [d[0] for d in cur.description], cur.fetchall()


def write_csv(path: Path, header, rows) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def embed(results: dict, setup_notes: dict) -> None:
    """Rewrite queries.sql with fresh output comments under each block."""
    text = OUT_BLOCK_RE.sub("\n", SQL_PATH.read_text(encoding="utf-8"))
    parts = re.split(r"(^-- @name:\s*\S+\s*$)", text, flags=re.MULTILINE)
    rebuilt = [parts[0]]
    for i in range(1, len(parts), 2):
        marker, body = parts[i], parts[i + 1]
        name = marker.split(":", 1)[1].strip()
        body = body.rstrip("\n")
        if name in results:
            header, rows = results[name]
            body += "\n\n" + table_comment(header, rows)
        elif name in setup_notes:
            body += "\n\n" + status_comment(setup_notes[name])
        rebuilt += [marker, body + "\n\n\n"]
    SQL_PATH.write_text("".join(rebuilt).rstrip("\n") + "\n", encoding="utf-8")


def main() -> None:
    log = [
        "HR Attrition Capstone - SQL execution log",
        f"Run at          : {dt.datetime.now().isoformat(timespec='seconds')}",
        f"SQL engine      : SQLite {sqlite3.sqlite_version} (Python {platform.python_version()} sqlite3 module)",
        f"Command         : python run queries.py   (working dir: {ROOT})",
        f"Source CSV      : {build_db.CSV_PATH.relative_to(ROOT)}",
        "",
    ]
    con = build_db.main()  # rebuilds the DB from scratch and validates; exits on failure
    OUT_DIR.mkdir(exist_ok=True)
    TABLEAU_DIR.mkdir(exist_ok=True)

    # --- Q1 status (DDL + load + flag): documented from the database, not invented
    n_rows = con.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
    n_cols = len(con.execute("PRAGMA table_info(employees)").fetchall())
    flag = con.execute(
        "SELECT SUM(attrition_flag), SUM(attrition_flag = 0), "
        "SUM((Attrition='Yes') <> (attrition_flag=1)) FROM employees").fetchone()
    views = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='view' ORDER BY name")]
    setup_notes = {
        "setup_ddl": ["Status: SUCCESS",
                      f"Table employees created with {n_cols - 1} source columns (+ attrition_flag added in setup_flag)",
                      f"Rows loaded from CSV by build db.py: {n_rows}"],
        "setup_flag": ["Status: SUCCESS",
                       f"attrition_flag = 1 rows: {flag[0]}   attrition_flag = 0 rows: {flag[1]}",
                       f"Rows where flag disagrees with Attrition label: {flag[2]}"],
        "setup_views": ["Status: SUCCESS", f"Views created: {', '.join(views)}"],
    }
    log += ["Setup blocks:"] + [f"  {k}: " + " / ".join(v) for k, v in setup_notes.items()] + [""]

    # --- run every q* block
    blocks = build_db.load_blocks()
    results = {}
    log.append("Query blocks (first execution):")
    for name, sql in blocks.items():
        if not name.startswith("q"):
            continue
        try:
            header, rows = run_block(con, sql)
        except sqlite3.Error as e:
            log.append(f"  {name}: FAILED - {e}")
            LOG_PATH.write_text("\n".join(log) + "\n", encoding="utf-8")
            sys.exit(f"Query {name} failed: {e}")
        results[name] = (header, rows)
        write_csv(OUT_DIR / f"{name.replace('_', ' ')}.csv", header, rows)
        log.append(f"  {name:38s} SUCCESS  rows={len(rows):<3d} -> outputs/{name.replace('_', ' ')}.csv")
        print(f"  {name:38s} -> outputs/{name.replace('_', ' ')}.csv ({len(rows)} rows)")

    # --- embed outputs as comments, then re-execute the rewritten file
    embed(results, setup_notes)
    reblocks = build_db.load_blocks()
    mismatches = [n for n, (h, r) in results.items() if run_block(con, reblocks[n]) != (h, r)]
    missing = [n for n in results if OUT_START not in reblocks[n]]
    log += ["", "Embedded outputs into queries.sql and re-executed every block:",
            f"  blocks re-executed: {len(results)}   result mismatches: {len(mismatches)} {mismatches or ''}",
            f"  blocks missing an output comment: {len(missing)} {missing or ''}"]
    if mismatches or missing:
        LOG_PATH.write_text("\n".join(log) + "\n", encoding="utf-8")
        sys.exit(f"Re-execution check failed: mismatches={mismatches} missing={missing}")
    print("Embedded outputs into queries.sql; re-execution identical.")

    # --- Tableau extracts (from SQL views)
    for view, fname, order in [("v_employees_enriched", "employees enriched.csv", "EmployeeNumber"),
                               ("v_risk_profiles", "risk profiles.csv", "risk_rank, headcount DESC")]:
        header, rows = run_block(con, f"SELECT * FROM {view} ORDER BY {order}")
        write_csv(TABLEAU_DIR / fname, header, rows)
        log.append(f"  export {view} -> tableau/{fname} ({len(rows)} rows)")

    # --- validation summary
    v = dict(zip(*results["q02a_validation_counts"]))
    v = {h: r for h, r in zip(results["q02a_validation_counts"][0], results["q02a_validation_counts"][1][0])}
    nulls = sum(results["q02b_validation_nulls"][1][0])
    log += ["", "Validation (Q2):",
            f"  row_count={v['row_count']}  distinct_employee_numbers={v['distinct_employee_numbers']}",
            f"  attritions_yes={v['attritions_yes']}  retained_no={v['retained_no']}  "
            f"attrition_rate_pct={v['attrition_rate_pct']}  bad_attrition_labels={v['bad_attrition_labels']}",
            f"  total NULLs across all columns={nulls}",
            "", "Errors encountered: none in this run."]
    LOG_PATH.write_text("\n".join(log) + "\n", encoding="utf-8")
    print(f"Log written to {LOG_PATH.relative_to(ROOT)}")
    con.close()


if __name__ == "__main__":
    main()
