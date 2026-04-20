import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

META_DIR = BASE_DIR / "metadata"
INBOX = BASE_DIR / "contrib" / "sharepoint_inbox"
DIFFS = BASE_DIR / "contrib" / "diffs"

DIFFS.mkdir(parents=True, exist_ok=True)

def diff(csv_file, excel_file, keys, business_cols, label):
    base = pd.read_csv(META_DIR / csv_file)
    incoming = pd.read_excel(INBOX / excel_file)

    base = base[keys + business_cols].copy()
    incoming = incoming[keys + business_cols].copy()

    base["_source"] = "current"
    incoming["_source"] = "proposed"

    combined = pd.concat([base, incoming], ignore_index=True)

    diffs = (
        combined
        .drop_duplicates(subset=keys + business_cols + ["_source"], keep=False)
        .sort_values(keys)
    )

    out = DIFFS / f"{label}_diff.csv"
    diffs.to_csv(out, index=False)
    print(f"🔍 Diff created: {out.name}")

def main():
    diff(
        "table_metadata.csv",
        "table_metadata_TEMPLATE.xlsx",
        ["owner", "table_name"],
        ["business_name", "description", "grain", "primary_key", "notes"],
        "table_metadata",
    )

    diff(
        "column_metadata.csv",
        "column_metadata_TEMPLATE.xlsx",
        ["owner", "table_name", "column_name"],
        ["business_name", "description", "example_value", "is_sensitive", "notes"],
        "column_metadata",
    )

if __name__ == "__main__":
    main()