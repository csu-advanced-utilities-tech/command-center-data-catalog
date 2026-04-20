import subprocess
import sys

def run(script):
    print(f"\n▶ Running {script}")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        raise RuntimeError(f"❌ Pipeline stopped at {script}")

def main():
    # ---- Validate metadata ----
    run("src/extract/validate_technical_metadata.py")
    run("src/models/validate_metadata_models.py")

    # ---- Build catalog ----
    run("src/generate/build_catalog_data.py")
    run("src/generate/render_index_page.py")
    run("src/generate/render_table_pages.py")

    # ---- Generate contribution templates ----
    run("src/contribute/generate_templates.py")

    print("\n✅ DATA CATALOG PIPELINE COMPLETED SUCCESSFULLY")

if __name__ == "__main__":
    main()