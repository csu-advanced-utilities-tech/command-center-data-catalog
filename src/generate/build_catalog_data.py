import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
META_DIR = BASE_DIR / "metadata"
VALIDATED_DIR = BASE_DIR / "output" / "validated"
OUT_DIR = BASE_DIR / "output" / "catalog"

OUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    tech = pd.read_csv(VALIDATED_DIR / "technical_columns_validated.csv")
    tables = pd.read_csv(META_DIR / "table_metadata.csv")
    columns = pd.read_csv(META_DIR / "column_metadata.csv")

    # Normalize casing
    for df, cols in [
        (tables, ["owner", "table_name"]),
        (columns, ["owner", "table_name", "column_name"])
    ]:
        for c in cols:
            df[c] = df[c].str.upper()

    merged = tech.merge(
        tables,
        how="left",
        left_on=["OWNER", "TABLE_NAME"],
        right_on=["owner", "table_name"]
    )

    merged = merged.merge(
        columns,
        how="left",
        left_on=["OWNER", "TABLE_NAME", "COLUMN_NAME"],
        right_on=["owner", "table_name", "column_name"],
        suffixes=("", "_col")
    )

    merged = merged[
        [
            "OWNER",
            "TABLE_NAME",
            "business_name",
            "description",
            "grain",
            "COLUMN_ID",
            "COLUMN_NAME",
            "business_name_col",
            "description_col",
            "DATA_TYPE",
            "DATA_LENGTH",
            "DATA_PRECISION",
            "DATA_SCALE",
            "NULLABLE"
        ]
    ].rename(columns={
        "business_name": "TABLE_BUSINESS_NAME",
        "description": "TABLE_DESCRIPTION",
        "business_name_col": "COLUMN_BUSINESS_NAME",
        "description_col": "COLUMN_DESCRIPTION"
    })

    for col in [
        "TABLE_BUSINESS_NAME",
        "TABLE_DESCRIPTION",
        "COLUMN_BUSINESS_NAME",
        "COLUMN_DESCRIPTION",
        "grain"
    ]:
        merged[col] = merged[col].fillna("")

    merged = merged.sort_values(["TABLE_NAME", "COLUMN_ID"], ignore_index=True)

    merged.to_csv(OUT_DIR / "catalog_data.csv", index=False)
    print("✅ Catalog dataset created")

if __name__ == "__main__":
    main()