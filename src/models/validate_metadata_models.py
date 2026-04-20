import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
META_DIR = BASE_DIR / "metadata"
OUT_DIR = BASE_DIR / "output" / "validated"

def main():
    tech_file = OUT_DIR / "technical_columns_validated.csv"
    table_file = META_DIR / "table_metadata.csv"
    column_file = META_DIR / "column_metadata.csv"

    # Load data
    tech = pd.read_csv(tech_file)
    tables = pd.read_csv(table_file)
    columns = pd.read_csv(column_file)

    # ---- Guardrails: fail fast on empty metadata ----
    if tables.empty:
        raise ValueError("❌ table_metadata.csv contains no rows")

    if columns.empty:
        raise ValueError("❌ column_metadata.csv contains no rows")

    # ---- Normalize casing ----
    tech["OWNER"] = tech["OWNER"].str.upper()
    tech["TABLE_NAME"] = tech["TABLE_NAME"].str.upper()
    tech["COLUMN_NAME"] = tech["COLUMN_NAME"].str.upper()

    tables["owner"] = tables["owner"].str.upper()
    tables["table_name"] = tables["table_name"].str.upper()

    columns["owner"] = columns["owner"].str.upper()
    columns["table_name"] = columns["table_name"].str.upper()
    columns["column_name"] = columns["column_name"].str.upper()

    # ---- Table validation ----
    valid_tables = set(zip(tech["OWNER"], tech["TABLE_NAME"]))

    for _, row in tables.iterrows():
        key = (row["owner"], row["table_name"])
        if key not in valid_tables:
            raise ValueError(
                f"❌ Table not found in technical metadata: OWNER={key[0]}, TABLE={key[1]}"
            )

    # ---- Column validation ----
    valid_columns = set(zip(
        tech["OWNER"],
        tech["TABLE_NAME"],
        tech["COLUMN_NAME"]
    ))

    for _, row in columns.iterrows():
        key = (row["owner"], row["table_name"], row["column_name"])
        if key not in valid_columns:
            raise ValueError(
                f"❌ Column not found in technical metadata: OWNER={key[0]}, "
                f"TABLE={key[1]}, COLUMN={key[2]}"
            )

    # ---- Cross-check: column metadata tables exist ----
    table_keys = set(zip(tables["owner"], tables["table_name"]))

    for _, row in columns.iterrows():
        table_key = (row["owner"], row["table_name"])
        if table_key not in table_keys:
            raise ValueError(
                f"❌ Column metadata references table not defined in table_metadata: "
                f"OWNER={table_key[0]}, TABLE={table_key[1]}"
            )

    print("✅ Business metadata validated successfully")

if __name__ == "__main__":
    main()