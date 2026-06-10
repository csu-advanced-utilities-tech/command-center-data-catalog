import sys
from pathlib import Path
import pandas as pd
from html import escape

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR / "src"))
from utils.constants import SITE_TITLE, GOVERNANCE_HUB_URL, domain_for, gate_div, gate_script

CATALOG_DIR = BASE_DIR / "output" / "catalog"
SITE_DIR = BASE_DIR / "docs"
TABLES_DIR = SITE_DIR / "tables"

TABLES_DIR.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(CATALOG_DIR / "catalog_data.csv")

    for table_name, table_df in df.groupby("TABLE_NAME"):
        render_table_page(table_name, table_df)


def render_table_page(table_name, df):
    first = df.iloc[0]
    domain = domain_for(table_name)
    col_count = len(df)

    biz_name = str(first.get("TABLE_BUSINESS_NAME", "")) if pd.notna(first.get("TABLE_BUSINESS_NAME")) else ""
    biz_name = biz_name.strip()
    description = str(first.get("TABLE_DESCRIPTION", "")) if pd.notna(first.get("TABLE_DESCRIPTION")) else ""
    description = description.strip()
    grain = str(first.get("grain", "")) if pd.notna(first.get("grain")) else ""
    grain = grain.strip()

    html = []
    html.append("<!DOCTYPE html>")
    html.append("<html lang='en'>")
    html.append("<head>")
    html.append("  <meta charset='UTF-8'>")
    html.append("  <meta name='viewport' content='width=device-width, initial-scale=1'>")
    html.append(f"  <title>{escape(str(table_name))} – {escape(SITE_TITLE)}</title>")
    html.append("  <link rel='stylesheet' href='../assets/styles.css'>")
    html.append("</head>")
    html.append("<body>")

    # Access gate + wrapper (hidden until unlocked).
    html.append(gate_div(SITE_TITLE))
    html.append("<div id='site' style='display:none'>")

    # Top bar.
    html.append("<header class='topbar'>")
    html.append(f"  <a class='brand' href='../index.html'>{escape(SITE_TITLE)}</a>")
    html.append(
        f"  <a class='hub-link' href='{escape(GOVERNANCE_HUB_URL)}' "
        "target='_blank' rel='noopener'>Governance Hub &#8599;</a>"
    )
    html.append("</header>")

    html.append("<div class='page'>")

    # Breadcrumb.
    html.append(
        "<div class='breadcrumb'>"
        "<a href='../index.html'>Catalog</a>"
        f"<span class='sep'>/</span>{escape(domain)}"
        f"<span class='sep'>/</span>{escape(str(table_name))}"
        "</div>"
    )

    html.append(f"<h1>{escape(str(table_name))}</h1>")
    if biz_name:
        html.append(f"<p class='muted'>{escape(biz_name)}</p>")

    # Overview panel.
    html.append("<div class='panel pad'>")
    if description:
        html.append(f"<p>{escape(description)}</p>")
    else:
        html.append("<p class='muted'>No description yet.</p>")
    if grain:
        html.append(f"<p><strong>Grain:</strong> {escape(grain)}</p>")
    html.append(f"<p class='muted'><strong>Domain:</strong> {escape(domain)}</p>")
    html.append("</div>")

    # Columns.
    html.append(f"<h2>Columns <span class='count'>{col_count}</span></h2>")
    html.append("<div class='panel'>")
    html.append("<table>")
    html.append(
        "<thead><tr>"
        "<th class='num'>#</th>"
        "<th>Column</th>"
        "<th>Business Name</th>"
        "<th>Data Type</th>"
        "<th>Nullable</th>"
        "<th>Description</th>"
        "</tr></thead><tbody>"
    )

    for _, row in df.sort_values("COLUMN_ID").iterrows():
        dtype = str(row["DATA_TYPE"])
        if pd.notna(row.get("DATA_PRECISION")):
            if pd.notna(row.get("DATA_SCALE")) and int(row["DATA_SCALE"]) != 0:
                dtype += f"({int(row['DATA_PRECISION'])},{int(row['DATA_SCALE'])})"
            else:
                dtype += f"({int(row['DATA_PRECISION'])})"
        elif pd.notna(row.get("DATA_LENGTH")):
            dtype += f"({int(row['DATA_LENGTH'])})"

        col_biz = escape(str(row.get("COLUMN_BUSINESS_NAME", ""))) if pd.notna(row.get("COLUMN_BUSINESS_NAME")) else ""
        col_desc_raw = str(row.get("COLUMN_DESCRIPTION", "")) if pd.notna(row.get("COLUMN_DESCRIPTION")) else ""
        col_desc_raw = col_desc_raw.strip()
        col_desc = escape(col_desc_raw) if col_desc_raw else "<span class='undocumented'>—</span>"
        col_id = int(row["COLUMN_ID"]) if pd.notna(row.get("COLUMN_ID")) else ""

        html.append(
            "<tr>"
            f"<td class='num'>{col_id}</td>"
            f"<td><strong>{escape(str(row['COLUMN_NAME']))}</strong></td>"
            f"<td>{col_biz}</td>"
            f"<td>{escape(dtype)}</td>"
            f"<td>{'Yes' if row.get('NULLABLE') else 'No'}</td>"
            f"<td>{col_desc}</td>"
            "</tr>"
        )

    html.append("</tbody></table>")
    html.append("</div>")
    html.append("</div>")  # .page

    html.append("</div>")  # #site
    html.append(gate_script())
    html.append("</body>")
    html.append("</html>")

    out_file = TABLES_DIR / f"{table_name}.html"
    out_file.write_text("\n".join(html), encoding="utf-8")
    print(f"✅ Generated {out_file.name}")


if __name__ == "__main__":
    main()
