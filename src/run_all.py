import subprocess
import sys
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parents[1]

def run(script):
    print(f"\n▶ Running {script}")
    result = subprocess.run(
        [sys.executable, script],
        cwd=BASE_DIR,
        check=False
    )
    if result.returncode != 0:
        raise RuntimeError(f"❌ Pipeline stopped at {script}")

def copy_assets_to_docs():
    src = BASE_DIR / "output" / "catalog" / "site" / "assets"
    dst = BASE_DIR / "docs" / "assets"

    if not src.exists():
        print("⚠️ No assets found to copy")
        return

    dst.mkdir(parents=True, exist_ok=True)

    for item in src.iterdir():
        target = dst / item.name
        try:
            if item.is_file():
                shutil.copy2(item, target)
        except PermissionError:
            print(f"⚠️ Could not overwrite {target.name}; file is in use")

    print("✅ Assets synced to docs/assets")

def main():
    # ---- Validate metadata ----
    run("src/extract/validate_technical_metadata.py")
    run("src/models/validate_metadata_models.py")

    # ---- Build catalog ----
    run("src/generate/build_catalog_data.py")
    run("src/generate/render_index_page.py")
    run("src/generate/render_table_pages.py")

    # ---- Copy static assets for GitHub Pages ----
    copy_assets_to_docs()

    # ---- Generate contribution templates ----
    run("src/contribute/generate_templates.py")

    print("\n✅ DATA CATALOG PIPELINE COMPLETED SUCCESSFULLY")

if __name__ == "__main__":
    main()