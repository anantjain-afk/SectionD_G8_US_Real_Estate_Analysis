"""
US Real Estate ETL Pipeline — Section D, Group 8
Orchestrator script to execute the data pipeline notebooks in sequence.

Structure:
1. Extraction (Raw -> Interim)
2. Cleaning (Interim -> Processed)
"""

import os
import sys
import logging
from pathlib import Path

# --- Configuration ---
class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent
    NOTEBOOK_DIR = BASE_DIR / "notebooks"
    DATA_DIR = BASE_DIR / "data"
    
    # Tiered Data Paths
    RAW_DATA = DATA_DIR / "raw" / "raw_data.csv"
    INTERIM_DATA = DATA_DIR / "raw" / "raw_extracted_data.csv"
    PROCESSED_DATA = DATA_DIR / "processed" / "clean_data.csv"
    
    # Pipeline Sequence
    NOTEBOOKS = [
        '01_extraction.ipynb',
        '02_cleaning.ipynb',
    ]

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Config.BASE_DIR / "etl_run.log")
    ]
)

def run_notebook(notebook_name: str) -> bool:
    """Execute a notebook in-place using nbconvert."""
    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor

    path = Config.NOTEBOOK_DIR / notebook_name
    if not path.exists():
        logging.error(f"Notebook not found: {path}")
        return False

    logging.info(f"STARTING: {notebook_name}")

    try:
        with open(path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        ep = ExecutePreprocessor(timeout=1200, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': str(Config.NOTEBOOK_DIR)}})

        # Save executed notebook (with outputs)
        with open(path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)

        logging.info(f"COMPLETED: {notebook_name}")
        return True
    except Exception as e:
        logging.error(f"FAILED: {notebook_name} | Error: {str(e)}")
        return False

def verify_pipeline():
    """Perform basic sanity checks on the output data."""
    import pandas as pd
    
    if not Config.PROCESSED_DATA.exists():
        logging.warning(f"Verification failed: {Config.PROCESSED_DATA} not found.")
        return

    try:
        df = pd.read_csv(Config.PROCESSED_DATA)
        rows, cols = df.shape
        nulls = df.isnull().sum().sum()
        
        logging.info("=" * 30)
        logging.info("PIPELINE VERIFICATION")
        logging.info(f"File: {Config.PROCESSED_DATA.name}")
        logging.info(f"Rows: {rows:,}")
        logging.info(f"Cols: {cols}")
        logging.info(f"Nulls: {nulls}")
        
        if nulls == 0:
            logging.info("Status: SUCCESS (Zero Nulls Detected)")
        else:
            logging.warning(f"Status: DIRTY ({nulls} Nulls Detected)")
        logging.info("=" * 30)
    except Exception as e:
        logging.error(f"Verification error: {e}")

def main():
    logging.info("=" * 60)
    logging.info("US REAL ESTATE ETL PIPELINE — EXECUTION STARTED")
    logging.info("=" * 60)

    for nb in Config.NOTEBOOKS:
        success = run_notebook(nb)
        if not success:
            logging.error("Pipeline aborted due to notebook failure.")
            sys.exit(1)

    verify_pipeline()
    logging.info("ETL PIPELINE COMPLETE.")
    logging.info("=" * 60)

if __name__ == "__main__":
    main()
