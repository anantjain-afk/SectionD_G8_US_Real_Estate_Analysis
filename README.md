# US Real Estate Analysis — Section D, Group 8

## Project Overview

This project performs an end-to-end analysis of US Real Estate listings (Zillow-style data). Starting from a raw dataset of ~600,000 rows and 28 columns, it produces a perfectly cleaned, analytical-ready dataset with **0 nulls, 0 infinities, and 0 invalid zeros** across all 19 final columns (59,581 rows). The pipeline focuses exclusively on residential buildings and uses domain-specific hierarchical imputation.

---

## Folder Structure

```
SectionD_G8_US_Real_Estate_Analysis/
├── data/
│   ├── raw_data.csv                 # Original raw dataset (~600k rows, 28 columns)
│   ├── raw_extracted_data.csv     # Representative 80k sample
│   └── clean_data.csv              # FINAL cleaned dataset (59,581 rows, 19 columns)
├── notebooks/
│   ├── 01_extraction.ipynb          # Data loading, profiling, sampling
│   ├── 02_cleaning.ipynb            # Step-by-step cleaning with formulas
│   ├── 03_eda.ipynb                 # Exploratory analysis & visualizations
│   ├── 04_statistical_analysis.ipynb # Hypothesis tests & regression models
│   └── 05_final_load_prep.ipynb     # Final audit & Tableau readiness
├── scripts/
│   └── etl_pipeline.py             # Thin orchestrator — runs notebooks 01 & 02 in sequence
├── reports/
│   └── cleaning_report.csv         # Step-by-step cleaning log
├── tableau/                        # Reserved for BI exports
├── requirements.txt
└── README.md
```

---

## Setup Instructions

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate
source venv/bin/activate        # macOS / Linux
.\venv\Scripts\activate          # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Register Jupyter kernel (needed for ETL script)
python3 -m ipykernel install --user --name python3 --display-name "Python 3"

# 5. Run the automated pipeline (executes notebooks 01 & 02)
python scripts/etl_pipeline.py

# OR run the notebooks manually in order: 01 → 02 → 03 → 04 → 05
```

> **Note:** The ETL pipeline (`etl_pipeline.py`) is a thin orchestrator. It does NOT contain any cleaning logic itself — it simply executes `01_extraction.ipynb` and `02_cleaning.ipynb` programmatically using `nbconvert`. All data transformation code lives in the notebooks.

---

## Raw Data — Original 28 Columns

| # | Raw Column | Type | Description |
|---|---|---|---|
| 1 | `property_url` | string | Listing URL on Zillow |
| 2 | `property_id` | int | Unique identifier for the listing |
| 3 | `address` | string | Full address string (e.g. "123 Main St, Austin, TX 78701") |
| 4 | `street_name` | string | Street name extracted from address |
| 5 | `apartment` | string | Apartment/unit number (if applicable) |
| 6 | `city` | string | City name |
| 7 | `state` | string | US state abbreviation |
| 8 | `latitude` | float | GPS latitude |
| 9 | `longitude` | float | GPS longitude |
| 10 | `postcode` | int/string | ZIP code |
| 11 | `price` | float | Listing price in USD |
| 12 | `bedroom_number` | float | Number of bedrooms |
| 13 | `bathroom_number` | float | Number of bathrooms |
| 14 | `price_per_unit` | float | Zillow-provided price per unit (inconsistent) |
| 15 | `living_space` | float | Interior living area in square feet |
| 16 | `land_space` | float | Total land/lot area |
| 17 | `land_space_unit` | string | Unit for land_space ("sqft" or "acres") |
| 18 | `broker_id` | string | Broker identifier |
| 19 | `property_type` | string | SINGLE_FAMILY, CONDO, TOWNHOUSE, LOT, etc. |
| 20 | `property_status` | string | FOR_SALE, RECENTLY_SOLD, etc. |
| 21 | `year_build` | float | Year the property was built |
| 22 | `total_num_units` | float | Total units (for multi-family) |
| 23 | `listing_age` | int | Days since the listing was created |
| 24 | `RunDate` | string | Date the data was scraped |
| 25 | `agency_name` | string | Listing brokerage name |
| 26 | `agent_name` | string | Listing agent's name |
| 27 | `agent_phone` | string | Agent's phone number |
| 28 | `is_owned_by_zillow` | bool | Whether Zillow owns the property |

---

## Complete Cleaning Process — Step by Step

### Step 0: Pre-Extraction Filtering (before sampling)

| Filter | Condition | Reason |
|---|---|---|
| Zero-price removal | `price == 0` | Listings with $0 price are data-entry errors or unlisted properties |
| Placeholder ZIP removal | `postcode == '11111'` | Dummy postcode indicating missing/invalid address data |

After filtering, **80,000 rows** were randomly sampled and saved as `raw_extracted_data.csv` using `random_state=42` for full reproducibility.

### Step 1: Row Filtering — Remove LOTs

| Filter | Condition | ~Rows Removed | Reason |
|---|---|---|---|
| LOT removal | `property_type == 'LOT'` | ~20,700 | Land-only listings have no bedrooms, bathrooms, or living space by definition. Keeping them would create massive artificial nulls and skew all residential metrics. |

### Step 2: Acres → SqFt Conversion

Before dropping the `land_space_unit` column, all land areas recorded in acres were converted:

```
land_space_sqft = land_space_acres × 43,560
```

~18,900 rows were converted. This ensures all `land_space` values are in consistent square feet.

### Step 3: Column Drops — Removed 12 Raw Columns

| Dropped Column | Reason for Removal |
|---|---|
| `apartment` | >95% null — most listings are not apartments |
| `broker_id` | Internal Zillow identifier, no analytical value |
| `year_build` | >80% null — insufficient data for age-based analysis |
| `total_num_units` | >90% null — only relevant for multi-family, mostly missing |
| `agent_name` | >70% null — personal info, not needed for market analysis |
| `agent_phone` | >70% null — personal info, not needed for market analysis |
| `is_owned_by_zillow` | >95% null — irrelevant binary flag |
| `price_per_unit` | Replaced by our recalculated `Price_Per_SqFt` (see below) |
| `land_space_unit` | No longer needed after converting all land values to sqft |
| `property_url` | URL string, not needed for analysis or dashboards |
| `listing_age` | Every single row had the value `-1` — no useful data |
| `RunDate` | Every single row had the same date `2022-04-24` — no variation |

### Step 4: Zero → NaN Conversion

**Critical fix**: The raw data contained zeros disguised as valid values. A house cannot have 0 sqft of living space or 0 bedrooms — these are missing values recorded as zero.

| Column | Zeros Converted to NaN | Reason |
|---|---|---|
| `living_space` | ~569 | A 0 sqft home does not exist |
| `bedroom_number` | ~461 | Every residential building has ≥1 bedroom |
| `bathroom_number` | ~614 | Every residential building has ≥1 bathroom |

### Step 5: Address Recovery (Regex)

For rows with missing `street_name` or `city`, we parsed the full `address` string using:

```
Pattern: ^([^,]+),\s*([^,]+),\s*([A-Z]{2})\s*(\d{5})
Group 1 → street_name
Group 2 → city
```

**Example**: `"2412, Montalba, TX 75853"` → street=`2412`, city=`Montalba`

Any remaining nulls after regex were filled with `"Unknown Street"` or `"Unknown City"` (only 1 row each).

---

## Step 6–10: Hierarchical Imputation — Column by Column

### `Living_Space_SqFt` (originally `living_space`)
- **Raw nulls after zero-conversion**: ~1,700
- **Tier 1 — Bedrooms → Space** (when bedrooms were known):
  ```
  Living_Space = bedroom_number × city_median(sqft_per_bedroom)
  Fallback: national median if city has no data
  ```
  **Example**: 3-bed home in a city where median = 600 sqft/bed → `3 × 600 = 1,800 sqft`
  - Filled ~1,094 rows

- **Tier 2 — Price → Space** (when bedrooms were also missing):
  ```
  Living_Space = Sale_Price / city_median(price_per_sqft)
  Fallback: state median → national median
  ```
  **Example**: $400,000 home in city with $200/sqft → `400,000 / 200 = 2,000 sqft`
  - Filled ~597 rows

- **Final nulls**: **0**

### `Bedrooms` (originally `bedroom_number`)
- **Raw nulls after zero-conversion**: ~1,700
- **Tier 3 — Reverse from Space**:
  ```
  Bedrooms = round(Living_Space / city_median(sqft_per_bedroom))
  Fallback: national median ratio
  ```
  **Example**: 2,000 sqft home, city median = 500 sqft/bed → `round(2000/500) = 4`
  - Filled ~1,234 rows
- **Clamped to [1, 10]**: Values below 1 set to 1, above 10 set to 10
- **Final nulls**: **0**, **Final zeros**: **0**

### `Bathrooms` (originally `bathroom_number`)
- **Raw nulls after zero-conversion**: ~1,600
- **Imputation formula**:
  ```
  Bathrooms = round(Living_Space / city_median(sqft_per_bathroom))
  Fallback: national median ratio
  ```
  **Example**: 1,500 sqft home, city median = 750 sqft/bath → `round(1500/750) = 2`
  - Filled ~1,030 rows
- **Clamped to [1, 10]**: Same logic as bedrooms
- **Final nulls**: **0**, **Final zeros**: **0**

### `latitude` and `longitude`
- **Raw nulls**: ~4,000 each
- **3-Level hierarchical centroid imputation**:
  ```
  Level 1: median(coordinate) WHERE postcode = same_postcode
  Level 2: median(coordinate) WHERE city = same_city
  Level 3: median(coordinate) WHERE state = same_state
  ```
- **Final nulls**: **0**

### `land_space`
- **Raw nulls**: ~10,700
- **Already converted from acres to sqft in Step 2**
- **Median fill**:
  ```
  Level 1: city_median(land_space)
  Level 2: state_median(land_space)
  ```
  Negative values (9 rows) were also replaced with the city median.
- **Final nulls**: **0**, **Negative values**: **0**

### `agency_name`
- **Raw nulls**: ~16,000
- **Fill**: All nulls replaced with `"Unknown Agency"` for clean grouping in dashboards
- **Final nulls**: **0**

---

## Step 11: Outlier Capping (99th Percentile)

| Metric | Cap Value | Purpose |
|---|---|---|
| `Sale_Price_Capped` | ~$4,598,490 | Prevents $100M+ luxury homes from skewing means/regressions |
| `Living_Space_Capped` | ~7,192 sqft | Prevents extreme mansions from distorting visualizations |

The raw uncapped values are preserved in `Sale_Price` and `Living_Space_SqFt` for full-range analysis.

---

## Step 12: Derived Columns

| Derived Column | Formula | Purpose |
|---|---|---|
| `Sale_Price` | Renamed from raw `price` | Clear analytical name |
| `Sale_Price_Capped` | `Sale_Price.clip(upper=99th_pct)` | Outlier-safe price for visualization |
| `Living_Space_Capped` | `Living_Space_SqFt.clip(upper=99th_pct)` | Outlier-safe space |
| `Price_Per_SqFt` | `Sale_Price / Living_Space_SqFt` | Key density metric (replaces Zillow's inconsistent `price_per_unit`) |

---

## Imputation Formula Reference Table

| Target Column | Formula | Grouping | Fallback |
|---|---|---|---|
| `Living_Space_SqFt` (Tier 1) | `bedrooms × median(sqft/bedroom)` | City | National median |
| `Living_Space_SqFt` (Tier 2) | `price ÷ median(price/sqft)` | City → State | National median |
| `Bedrooms` | `round(space ÷ median(sqft/bedroom))` | City | National median |
| `Bathrooms` | `round(space ÷ median(sqft/bathroom))` | City | National median |
| `latitude / longitude` | `median(coord)` | Postcode → City → State | State centroid |
| `land_space` | `median(land_space)` | City → State | State median |
| `street_name` | Regex group 1 from `address` | — | `"Unknown Street"` |
| `city` | Regex group 2 from `address` | — | `"Unknown City"` |
| `agency_name` | Direct fill | — | `"Unknown Agency"` |

---

## Final Clean Dataset — All 19 Columns

| # | Column | Type | Nulls | Zeros | Source |
|---|---|---|---|---|---|
| 1 | `property_id` | int | 0 | 0 | Original |
| 2 | `address` | string | 0 | — | Original |
| 3 | `street_name` | string | 0 | — | Regex recovery |
| 4 | `city` | string | 0 | — | Regex recovery |
| 5 | `state` | string | 0 | — | Original |
| 6 | `latitude` | float | 0 | 0 | Hierarchical centroid |
| 7 | `longitude` | float | 0 | 0 | Hierarchical centroid |
| 8 | `postcode` | string | 0 | — | Pre-filtered |
| 9 | `Bedrooms` | float | 0 | 0 | Tier 3 + clamp [1,10] |
| 10 | `Bathrooms` | float | 0 | 0 | Ratio impute + clamp [1,10] |
| 11 | `Living_Space_SqFt` | float | 0 | 0 | Tier 1+2 imputation |
| 12 | `land_space` | float | 0 | 0 | Acres conv + median fill |
| 13 | `property_type` | string | 0 | — | LOTs filtered |
| 14 | `property_status` | string | 0 | — | Original |
| 15 | `agency_name` | string | 0 | — | "Unknown Agency" fill |
| 16 | `Sale_Price` | float | 0 | 0 | Renamed from `price` |
| 17 | `Sale_Price_Capped` | float | 0 | 0 | 99th percentile cap |
| 18 | `Living_Space_Capped` | float | 0 | 0 | 99th percentile cap |
| 19 | `Price_Per_SqFt` | float | 0 | 0 | Derived: Sale_Price ÷ Space |

**Total: 19 columns | 0 nulls | 0 infinities | 0 invalid zeros**

---

## Dependencies

Listed in `requirements.txt`:
- `pandas` — Data manipulation
- `numpy` — Numerical operations
- `matplotlib` — Plotting
- `seaborn` — Statistical visualization
- `scipy` — Hypothesis testing
- `statsmodels` — Regression analysis
- `notebook` — Jupyter notebook support
