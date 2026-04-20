import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
META_DIR = BASE_DIR / "metadata"
OUT_DIR = BASE_DIR / "output" / "validated"

OUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    df = pd.read_csv(META_DIR / "technical_columns.csv")

    # Required columns (Oracle exports uppercase by default)
    required_cols = {
        "OWNER",
        "TABLE_NAME",
        "COLUMN_ID",
        "COLUMN_NAME",
        "DATA_TYPE",
        "DATA_LENGTH",
        "DATA_PRECISION",
        "DATA_SCALE",
        "NULLABLE"
    }

    actual_cols = set(df.columns.str.upper())
    missing = required_cols - actual_cols
    if missing:
        raise ValueError(f"❌ Missing required columns: {missing}")

    # Normalize casing and values
    df.columns = df.columns.str.upper()
    df["OWNER"] = df["OWNER"].str.upper()
    df["TABLE_NAME"] = df["TABLE_NAME"].str.upper()
    df["COLUMN_NAME"] = df["COLUMN_NAME"].str.upper()

    df["NULLABLE"] = df["NULLABLE"].map({"Y": True, "N": False})

    df = df.sort_values(["TABLE_NAME", "COLUMN_ID"])

    out_file = OUT_DIR / "technical_columns_validated.csv"
    df.to_csv(out_file, index=False)

    print(f"✅ Technical metadata validated and written to:")
    print(f"   {out_file}")

if __name__ == "__main__":
    main()