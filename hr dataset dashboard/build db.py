"""Build hr.db from the IBM HR attrition CSV and validate the load.

Runs the setup_* blocks of queries.sql (DDL, attrition_flag, views), loads the
CSV in between, then checks row count, uniqueness, NULLs and class balance.
Exits with code 1 if any check fails.
"""
import csv
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "data" / "WA Fn-UseC -HR-Employee-Attrition.csv"
DB_PATH = ROOT / "hr.db"
SQL_PATH = ROOT / "queries.sql"

EXPECTED_ROWS = 1470
EXPECTED_YES = 237
EXPECTED_NO = 1233


def load_blocks(path: Path = SQL_PATH) -> dict[str, str]:
    """Split queries.sql into named blocks on '-- @name: <name>' lines."""
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"^-- @name:\s*(\S+)\s*$", text, flags=re.MULTILINE)
    # parts = [preamble, name1, body1, name2, body2, ...]
    return {parts[i]: parts[i + 1].strip() for i in range(1, len(parts), 2)}


def build() -> sqlite3.Connection:
    blocks = load_blocks()
    con = sqlite3.connect(DB_PATH)
    con.executescript(blocks["setup_ddl"])

    cols = [r[1] for r in con.execute("PRAGMA table_info(employees)")]
    int_cols = {r[1] for r in con.execute("PRAGMA table_info(employees)") if r[2] == "INTEGER"}

    # utf-8-sig strips the BOM that precedes the first header ("Age")
    with CSV_PATH.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = set(cols) - set(reader.fieldnames or [])
        if missing:
            sys.exit(f"CSV is missing columns: {sorted(missing)}")
        rows = [
            tuple(int(r[c]) if c in int_cols else r[c] for c in cols)
            for r in reader
        ]

    placeholders = ",".join("?" * len(cols))
    con.executemany(f"INSERT INTO employees ({','.join(cols)}) VALUES ({placeholders})", rows)
    con.executescript(blocks["setup_flag"])
    con.executescript(blocks["setup_views"])
    con.commit()
    return con


def validate(con: sqlite3.Connection) -> bool:
    blocks = load_blocks()
    cur = con.execute(blocks["q02a_validation_counts"])
    names = [d[0] for d in cur.description]
    counts = dict(zip(names, cur.fetchone()))

    cur = con.execute(blocks["q02b_validation_nulls"])
    null_cols = {d[0]: v for d, v in zip(cur.description, cur.fetchone()) if v}

    checks = [
        ("row count == 1470", counts["row_count"] == EXPECTED_ROWS, counts["row_count"]),
        ("distinct EmployeeNumber == 1470", counts["distinct_employee_numbers"] == EXPECTED_ROWS,
         counts["distinct_employee_numbers"]),
        ("no NULLs in any column", not null_cols, null_cols or 0),
        ("attritions (Yes) == 237", counts["attritions_yes"] == EXPECTED_YES, counts["attritions_yes"]),
        ("retained (No) == 1233", counts["retained_no"] == EXPECTED_NO, counts["retained_no"]),
        ("no bad Attrition labels", counts["bad_attrition_labels"] == 0, counts["bad_attrition_labels"]),
    ]
    ok = True
    for label, passed, value in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {label}  (got {value})")
        ok &= passed
    print(f"  attrition rate = {counts['attrition_rate_pct']}%")
    return ok


def main() -> sqlite3.Connection:
    if not CSV_PATH.exists():
        sys.exit(f"CSV not found: {CSV_PATH}")
    print(f"Building {DB_PATH.name} from {CSV_PATH.name}")
    con = build()
    print("Validation:")
    if not validate(con):
        con.close()
        sys.exit("Validation FAILED - stopping.")
    return con


if __name__ == "__main__":
    main().close()
