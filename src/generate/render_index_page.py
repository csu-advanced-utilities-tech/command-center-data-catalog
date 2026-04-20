from pathlib import Path
import pandas as pd
from html import escape

BASE_DIR = Path(__file__).resolve().parents[2]
CATALOG_DIR = BASE_DIR / "output" / "catalog"
SITE_DIR = BASE_DIR / "docs"

SITE_DIR.mkdir(parents=True, exist_ok=True)

def main():
    df = pd.read_csv(CATALOG_DIR / "catalog_data.csv")

    tables = (
        df[["TABLE_NAME", "TABLE_DESCRIPTION"]]
        .drop_duplicates()
        .sort_values("TABLE_NAME")
        .reset_index(drop=True)
    )

    html = []

    html.append("<!DOCTYPE html>")
    html.append("<html lang='en'>")
    html.append("<head>")
    html.append("  <meta charset='UTF-8'>")
    html.append("  <title>Command Center Data Catalog</title>")
    html.append("  <link rel='stylesheet' href='assets/stylesd>")
    html.append("<body>")

    html.append("<div class='page'>")
    html.append("<h1>Command Center Data Catalog</h1>")
    html.append(
        "<p class='muted'>Search and browse available tables and their business definitions.</p>"
    )
    html.append(
        "<input type='text' id='searchInput' placeholder='Search tables or descriptions...'>"
    )

    html.append("<div class='panel'>")
    html.append("<table id='catalogTable'>")
    html.append("<tr><th>Table</th><th>Description</th></tr>")

    for _, row in tables.iterrows():
        name = escape(row["TABLE_NAME"])
        desc = escape(str(row["TABLE_DESCRIPTION"])) if pd.notna(row["TABLE_DESCRIPTION"]) else ""

        html.append(
            "<tr>"
            f"<td><a href='tables/{name}.html></td>"
            f"<td>{desc}</td>"
            "</tr>"
        )

    html.append("</table>")
    html.append("</div>")
    html.append("</div>")

    html.append("<script src='assetscript>")
    html.append("</body>")
    html.append("</html>")

