from pathlib import Path
import pandas as pd
from html import escape

BASE_DIR = Path(__file__).resolve().parents[2]

CATALOG_DIR = BASE_DIR / "output" / "catalog"
SITE_DIR = BASE_DIR / "docs"
TABLES_DIR = SITE_DIR / "tables"

TABLES_DIR.mkdir(parents=True, exist_ok=True)

def main():
    df = pd.read_csv(CATALOG_DIR / "catalog_data.csv")

    for table_name, table_df in df.groupby("TABLE_NAME"):
        render_table_page(table_name, table_df)

def render_table_page(table_name, df):
    html = []

    html.append("<!DOCTYPE html>")
    html.append("<html lang='en'>")
    html.append("<head>")
    html.append("  <meta charset='UTF-8'>")
    html.append(f"  <title>{escape(table_name)} – Data Dictionary</title>")
    html.append("  <link rel='stylesheet' href='../assets/styles.css'>")
    html.append("</head>")
    html.append("<body>")

    html.append("<div class='page'>")
    html.append("<p class='back-link'><a href='../index.html'>← Back to Catalog</a></p>")
    html.append(f"<h1>{escape(table_name)}</h1>")

    first = df.iloc[0]

    if pd.notna(first.get("TABLE_DESCRIPTION")) or pd.notna(first.get("grain")):
        html.append("<div class='panel'>")

        if pd.notna(first.get("TABLE_DESCRIPTION")):
            html.append(
                f"<p class='muted'>{escape(str(first['TABLE_DESCRIPTION']))}</p>"
            )

        if pd.notna(first.get("grain")):
            html.append(
                f"<p><strong>Grain:</strong> {escape(str(first['grain']))}</p>"
            )

        html.append("</div>")

    html.append("<h2>Columns</h2>")
    html.append("<div class='panel'>")
    html.append("<table>")
    html.append(
        "<tr>"
        "<th>Column</th>"
        "<th>Business Name</th>"
        "<th>Data Type</th>"
        "<th>Nullable</th>"
        "<th>Description</th>"
        "</tr>"
    )

    for _, row in df.sort_values("COLUMN_ID").iterrows():
        dtype = row["DATA_TYPE"]

        if pd.notna(row.get("DATA_PRECISION")):
            if pd.notna(row.get("DATA_SCALE")):
                dtype += f"({int(row['DATA_PRECISION'])},{int(row['DATA_SCALE'])})"
            else:
                dtype += f"({int(row['DATA_PRECISION'])})"
        elif pd.notna(row.get("DATA_LENGTH")):
            dtype += f"({int(row['DATA_LENGTH'])})"

        html.append(
            "<tr>"
            f"<td>{escape(row['COLUMN_NAME'])}</td>"
            f"<td>{escape(str(row.get('COLUMN_BUSINESS_NAME', '')))}</td>"
            f"<td>{escape(dtype)}</td>"
            f"<td>{'Yes' if row.get('NULLABLE') else 'No'}</td>"
            f"<td>{escape(str(row.get('COLUMN_DESCRIPTION', '')))}</td>"
            "</tr>"
        )

    html.append("</table>")
    html.append("</div>")
    html.append("</div>")

    html.append("<script src='../assets/search.js'></script>")
    html.append("</body>")
    html.append("</html>")

    out_file = TABLES_DIR / f"{table_name}.html"
    out_file.write_text("\n".join(html), encoding="utf-8")

    print(f"✅ Generated {out_file.name}")

if __name__ == "__main__":
    main()