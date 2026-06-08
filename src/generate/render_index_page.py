import sys
from pathlib import Path
import pandas as pd
from html import escape

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR / "src"))
from utils.constants import SITE_TITLE, GOVERNANCE_HUB_URL, DOMAIN_MAP, OTHER_DOMAIN, domain_for

CATALOG_DIR = BASE_DIR / "output" / "catalog"
SITE_DIR = BASE_DIR / "docs"

SITE_DIR.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(CATALOG_DIR / "catalog_data.csv")

    tables = (
        df[["TABLE_NAME", "TABLE_BUSINESS_NAME", "TABLE_DESCRIPTION"]]
        .drop_duplicates(subset=["TABLE_NAME"])
        .sort_values("TABLE_NAME")
        .reset_index(drop=True)
    )

    # One row per column in catalog_data, so column count = rows per table.
    col_counts = df.groupby("TABLE_NAME").size().to_dict()

    descriptions = tables["TABLE_DESCRIPTION"].fillna("").astype(str).str.strip()
    total_tables = len(tables)
    documented = int(descriptions.ne("").sum())
    total_columns = int(len(df))
    pct = round(documented / total_tables * 100) if total_tables else 0

    # Group tables by domain, preserving DOMAIN_MAP order, OTHER last.
    domain_order = list(DOMAIN_MAP.keys()) + [OTHER_DOMAIN]
    grouped = {d: [] for d in domain_order}
    for _, row in tables.iterrows():
        grouped[domain_for(row["TABLE_NAME"])].append(row)

    html = []
    html.append("<!DOCTYPE html>")
    html.append("<html lang='en'>")
    html.append("<head>")
    html.append("  <meta charset='UTF-8'>")
    html.append("  <meta name='viewport' content='width=device-width, initial-scale=1'>")
    html.append(f"  <title>{escape(SITE_TITLE)}</title>")
    html.append("  <link rel='stylesheet' href='assets/styles.css'>")
    html.append("</head>")
    html.append("<body>")

    # Top bar (matches the governance hub).
    html.append("<header class='topbar'>")
    html.append(f"  <a class='brand' href='index.html'>{escape(SITE_TITLE)}</a>")
    html.append(
        f"  <a class='hub-link' href='{escape(GOVERNANCE_HUB_URL)}' "
        "target='_blank' rel='noopener'>Governance Hub &#8599;</a>"
    )
    html.append("</header>")

    html.append("<div class='page'>")

    # Hero + stats.
    html.append("<div class='hero'>")
    html.append(f"<h1>{escape(SITE_TITLE)}</h1>")
    html.append("<p class='muted'>Browse the Command Center database by domain, or search across all tables.</p>")
    html.append("<div class='stats'>")
    html.append(f"  <div class='stat'><span class='num'>{total_tables}</span><span class='label'>Tables</span></div>")
    html.append(f"  <div class='stat'><span class='num'>{total_columns}</span><span class='label'>Columns</span></div>")
    html.append(f"  <div class='stat'><span class='num'>{documented}</span><span class='label'>Documented</span></div>")
    html.append(f"  <div class='stat'><span class='num'>{pct}%</span><span class='label'>Coverage</span></div>")
    html.append("</div>")
    html.append("</div>")

    html.append("<input type='text' id='searchInput' placeholder='Search tables by name, description, or domain...'>")

    # Domain sections.
    for domain in domain_order:
        rows = grouped[domain]
        if not rows:
            continue

        html.append(f"<section class='domain' data-domain='{escape(domain)}'>")
        html.append(f"<h2>{escape(domain)} <span class='count'>{len(rows)}</span></h2>")
        html.append("<div class='panel'>")
        html.append("<table class='catalog-table'>")
        html.append("<thead><tr><th>Table</th><th>Business Name</th><th>Description</th><th class='num'>Cols</th></tr></thead>")
        html.append("<tbody>")

        for row in rows:
            name = escape(str(row["TABLE_NAME"]))
            biz = escape(str(row["TABLE_BUSINESS_NAME"])) if pd.notna(row["TABLE_BUSINESS_NAME"]) else ""
            desc_raw = str(row["TABLE_DESCRIPTION"]) if pd.notna(row["TABLE_DESCRIPTION"]) else ""
            desc_raw = desc_raw.strip()
            cols = col_counts.get(row["TABLE_NAME"], 0)

            desc_cell = escape(desc_raw) if desc_raw else "<span class='undocumented'>—</span>"

            html.append(
                "<tr>"
                f"<td><a class='tname' href='tables/{name}.html'>{name}</a></td>"
                f"<td>{biz}</td>"
                f"<td>{desc_cell}</td>"
                f"<td class='num'>{cols}</td>"
                "</tr>"
            )

        html.append("</tbody>")
        html.append("</table>")
        html.append("</div>")
        html.append("</section>")

    html.append("<div id='noResults'>No tables match your search.</div>")
    html.append("</div>")  # .page

    html.append("<script src='assets/search.js'></script>")
    html.append("</body>")
    html.append("</html>")

    (SITE_DIR / "index.html").write_text("\n".join(html), encoding="utf-8")
    print("✅ Index page generated")


if __name__ == "__main__":
    main()
