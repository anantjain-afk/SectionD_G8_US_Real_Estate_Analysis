"""
ETL Pipeline — Section D, Group 8
Thin orchestrator that runs the notebooks in sequence.
All cleaning logic lives in the notebooks themselves.

Usage:
    python scripts/etl_pipeline.py
"""

import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTEBOOK_DIR = os.path.join(BASE_DIR, 'notebooks')

NOTEBOOKS = [
    '01_extraction.ipynb',
    '02_cleaning.ipynb',
]


def run_notebook(name):
    """Execute a notebook in-place using nbconvert API (no CLI dependency)."""
    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor

    path = os.path.join(NOTEBOOK_DIR, name)
    if not os.path.exists(path):
        logging.error(f"Notebook not found: {path}")
        return False

    logging.info(f"Running {name} ...")

    with open(path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

    try:
        ep.preprocess(nb, {'metadata': {'path': NOTEBOOK_DIR}})
    except Exception as e:
        logging.error(f"{name} FAILED: {e}")
        return False

    # Save executed notebook (with outputs)
    with open(path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

    logging.info(f"{name} completed successfully.")
    return True


def main():
    logging.info("=" * 50)
    logging.info("ETL Pipeline — US Real Estate Analysis")
    logging.info("=" * 50)

    for nb in NOTEBOOKS:
        ok = run_notebook(nb)
        if not ok:
            logging.error(f"Pipeline stopped at {nb}")
            sys.exit(1)

    # Quick verification
    import pandas as pd
    clean_path = os.path.join(BASE_DIR, 'data', 'clean_data.csv')
    if os.path.exists(clean_path):
        df = pd.read_csv(clean_path)
        nulls = df.isnull().sum().sum()
        logging.info(f"Verification: {clean_path}")
        logging.info(f"  Rows: {len(df):,}  Columns: {df.shape[1]}  Nulls: {nulls}")
    else:
        logging.warning(f"clean_data.csv not found at {clean_path}")

    logging.info("=" * 50)
    logging.info("ETL Pipeline complete.")
    logging.info("=" * 50)


if __name__ == "__main__":
    main()


