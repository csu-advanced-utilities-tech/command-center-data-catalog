import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

META_DIR = BASE_DIR / "metadata"
INBOX = BASE_DIR / "contrib" / "sharepoint_inbox"

def promote(base_csv, excel_file, keys, business_cols):
    base = pd.read_csv(META_DIR / base_csv)
    incoming = pd.read_excel(INBOX / excel_file)

    # Ensure business columns are treated as strings
    for col in business_cols:
        if col in base.columns:
            base[col] = base[col].astype("string")
        if col in incoming.columns:
            incoming[col] = incoming[col].astype("string")

    base.set_index(keys, inplace=True)
    incoming.set_index(keys, inplace=True)

    base.update(incoming[business_cols])

    base.reset_index(inplace=True)
    base.to_csv(META_DIR / base_csv, index=False)

    print(f"✅ Promoted business metadata into {base_csv}")

def main():
    promote(
        "table_metadata.csv",
        "table_metadata_TEMPLATE.xlsx",
        ["owner", "table_name"],
        ["business_name", "description", "grain", "primary_key", "notes"]
    )

    promote(
        "column_metadata.csv",
        "column_metadata_TEMPLATE.xlsx",
        ["owner", "table_name", "column_name"],
        ["business_name", "description", "example_value", "is_sensitive", "notes"]
    )

if __name__ == "__main__":
    main()