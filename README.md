# US Real Estate Market Analysis — DVA Capstone 2

---

## Project Overview

| Field | Details |
|---|---|
| **Project Title** | US Real Estate Market Analysis & Data Integrity Pipeline |
| **Sector** | Real Estate / PropTech |
| **Team ID** | _Group 8_ |
| **Section** | Section D |
| **Faculty Mentor** | _Archit Raj_ |
| **Institute** | Newton School of Technology |
| **Submission Date** | _29/04/2026_ |

---


## Business Problem

Real Estate is the world's largest asset class, where **Price per Square Foot (PPSF)** is the primary metric for valuation. Portfolio Managers and Real Estate Investors rely on clean, high-integrity data to make million-dollar acquisition decisions. However, publicly scraped listing data (Zillow-style) is notoriously "dirty" — plagued by missing room counts, inconsistent land units (Acres vs. SqFt), and invalid zero-values that make standard analysis unreliable. In our dataset of ~600,000 listings, **25% of key metrics** (bedrooms, bathrooms, living space) were missing or recorded as invalid zeros, creating a massive "Analytical Blind Spot."

**Core Business Question**

> How can investors identify undervalued properties and make accurate "Buy vs. Pass" decisions when 25% of the market data is hidden behind missing or invalid values?

**Decision Supported**

> This analysis enables stakeholders to make **precision market-entry and competitive pricing decisions** by providing a 100% clean dataset (Zero Nulls, Zero Infinities) with reliable PPSF benchmarks across 22 US states.

---

## Dataset

| Attribute | Details |
|---|---|
| **Source Name** | Zillow-style US Real Estate Listings (Scraped) |
| **Direct Access Link** | _[https://www.kaggle.com/datasets/polartech/500000-us-homes-data-for-sale-properties](https://www.kaggle.com/datasets/polartech/500000-us-homes-data-for-sale-properties)_ |
| **Row Count** | 600,000 (raw) → 80,000 (sampled) → 59,581 (final clean) |
| **Column Count** | 28 (raw) → 19 (final clean, all meaningful) |
| **Time Period Covered** | April 2022 (single scrape snapshot) |
| **Format** | CSV |

---

## Folder Structure

```
SectionD_G8_US_Real_Estate_Analysis/
├── data/
│   ├── raw/                 # Original and sampled raw data
│   │   ├── raw_data.csv     # Original dataset (~600k rows)
│   │   └── raw_extracted_data.csv # Representative 80k sample
│   └── processed/           # FINAL cleaned dataset
│       └── clean_data.csv   # analytical-ready (59,581 rows)
├── notebooks/
│   ├── 01_extraction.ipynb  # Data loading, profiling, sampling
│   ├── 02_cleaning.ipynb    # Step-by-step cleaning with formulas
│   ├── 03_eda.ipynb         # Exploratory analysis & visualizations
│   ├── 04_statistical_analysis.ipynb # Hypothesis tests & regression models
│   └── 05_final_load_prep.ipynb     # Final audit & Tableau readiness
├── scripts/
│   └── etl_pipeline.py      # Robust orchestrator — runs notebooks 01 & 02 in sequence
├── reports/
│   └── cleaning_report.csv  # Step-by-step cleaning log
├── tableau/                 # Dashboard screenshots & public links
├── docs/
│   └── data_dictionary.md   # Column-level data dictionary
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

> **Note:** The ETL pipeline (`etl_pipeline.py`) is a robust orchestrator with logging, config management, and automated verification. It executes `01_extraction.ipynb` and `02_cleaning.ipynb` programmatically using `nbconvert`. All data transformation code lives in the notebooks.

---

## KPI Framework

| KPI | Definition | Formula / Computation |
|---|---|---|
| Median Price Per SqFt (PPSF) | Primary valuation benchmark normalized across property sizes | `Sale_Price / Living_Space_SqFt` — computed in `03_eda.ipynb` |
| Data Recovery Rate | Percentage of missing data restored via hierarchical imputation | `(rows_recovered / total_null_rows) × 100` — computed in `02_cleaning.ipynb` |
| Market Status Ratio | Proportion of listings currently active vs. pending | `count(FOR_SALE) / total_listings` — computed in `03_eda.ipynb` |
| Median Sale Price (Capped) | Outlier-safe central price tendency per state/city | `Sale_Price.clip(upper=99th_pct).median()` — computed in `03_eda.ipynb` |

Document KPI logic clearly in `notebooks/04_statistical_analysis.ipynb` and `notebooks/05_final_load_prep.ipynb`.

---

## Tableau Dashboard

| Item | Details |
|---|---|
| **Dashboard URL** | [View on Tableau Public](https://public.tableau.com/app/profile/anant.jain2510/viz/DVA_capstone_tableau/Dashboard1) |
| **Executive View** | Geographic Market Overview — US map with price heatmap, top 15 states by median price, and scatter map of price hotspots |
| **Operational View** | Property Analysis — Sale price distribution by type, bedroom-bathroom heatmap, listing status breakdown, and property type pie chart |
| **Deep Dive View** | Pricing Deep Dive — $/SqFt distribution, agency performance bubbles, land size vs. price scatter, and state-level PPSF ranking |
| **Main Filters** | State, Property Type, Property Status, Bedrooms (slider), Price range |

Store dashboard screenshots in `tableau/screenshots/` and document the public links in `tableau/dashboard_links.md`.

---

## Analytical Pipeline

The project follows a structured 7-step workflow:

1. **Define** – Sector selected (Real Estate), problem statement scoped, mentor approval obtained.
2. **Extract** – Raw dataset sourced and committed to `data/raw/`; data dictionary drafted.
3. **Clean and Transform** – Cleaning pipeline built in `notebooks/02_cleaning.ipynb` and orchestrated via `scripts/etl_pipeline.py`.
4. **Analyze** – EDA and statistical analysis performed in notebooks `03` and `04`.
5. **Visualize** – Interactive Tableau dashboard built and published on Tableau Public.
6. **Recommend** – 3–5 data-backed business recommendations delivered.
7. **Report** – Final project report and presentation deck completed and exported to PDF in `reports/`.

---

## Data Engineering — Complete Cleaning Process

### Step 0: Pre-Extraction Filtering (before sampling)

| Filter | Condition | Reason |
|---|---|---|
| Zero-price removal | `price == 0` | Listings with $0 price are data-entry errors or unlisted properties |
| Placeholder ZIP removal | `postcode == '11111'` | Dummy postcode indicating missing/invalid address data |

After filtering, **80,000 rows** were randomly sampled and saved to `data/raw/raw_extracted_data.csv` using `random_state=42` for full reproducibility.

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

## Hierarchical Imputation — Column by Column

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

## Outlier Capping (99th Percentile)

| Metric | Cap Value | Purpose |
|---|---|---|
| `Sale_Price_Capped` | ~$4,598,490 | Prevents $100M+ luxury homes from skewing means/regressions |
| `Living_Space_Capped` | ~7,192 sqft | Prevents extreme mansions from distorting visualizations |

The raw uncapped values are preserved in `Sale_Price` and `Living_Space_SqFt` for full-range analysis.

---

## Derived Columns

| Derived Column | Formula | Purpose |
|---|---|---|
| `Sale_Price` | Renamed from raw `price` | Clear analytical name |
| `Sale_Price_Capped` | `Sale_Price.clip(upper=99th_pct)` | Outlier-safe price for visualization |
| `Living_Space_Capped` | `Living_Space_SqFt.clip(upper=99th_pct)` | Outlier-safe space |
| `Price_Per_SqFt` | `Sale_Price / Living_Space_SqFt` | Key density metric (replaces Zillow's inconsistent `price_per_unit`) |

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

## Key EDA Insights

1. **Single-Family Dominance:** 80% of the US residential market is Single-Family homes, making them the most stable investment class.
2. **Geographic Value Clusters:** California, Hawaii, and Colorado lead in Median Sale Price; cities like Ashton reach extreme density of $70,000+/SqFt.
3. **The Living Space Correlation:** A 0.7+ positive correlation between Living Space and Sale Price validates PPSF as the primary valuation metric.
4. **Agency Concentration:** Three agencies (Coldwell Banker, Compass, eXp Realty) dominate listing volume across 22 states.

---

## Advanced Analysis

- **Hypothesis Testing:** Welch's T-Test and Mann-Whitney U confirmed statistically significant price differences between property types (p < 0.05).
- **Regression Modeling:** OLS and Multiple Linear Regression quantified that each additional SqFt adds a predictable dollar value to sale price.
- **Market Segmentation (K-Means):** Identified 3 distinct tiers — Budget, Mid-Range, and Luxury — based on price-to-space clustering.
- **Predictive Forecasting (Random Forest):** Location (Lat/Long) and Living Space explain 70%+ of price variance (R² > 0.7).
- **Libraries Used:** `scipy`, `statsmodels`, `scikit-learn`.

---

## Business Recommendations

1. **Single-Family First Strategy:**
   - *Insight:* 80% market share with most stable PPSF benchmarks.
   - *Action:* Prioritize SFR acquisitions in "Mid-Range" clusters.
   - *Impact:* Increased portfolio liquidity and reduced valuation risk.

2. **Precision Geo-Targeting:**
   - *Insight:* Location is a 3x stronger predictor of price than bedroom count.
   - *Action:* Adopt "Geo-First" screening; flag listings priced 15% below predicted geographic value.
   - *Impact:* Identification of undervalued "Alpha" opportunities.

3. **Top-3 Agency Partnership:**
   - *Insight:* Coldwell Banker, Compass, and eXp control the majority of high-quality inventory.
   - *Action:* Form strategic "Preferred Investor" partnerships with these brokerages.
   - *Impact:* Early access to pre-listing inventory.

4. **PPSF Discipline in Bidding:**
   - *Insight:* 0.7+ correlation validates PPSF as the north-star metric.
   - *Action:* Implement a strict "PPSF Cap" policy; reject properties 1.5 SD above city-median PPSF.
   - *Impact:* Prevention of overpayment in "bubble" markets.

---

## Tech Stack

| Tool | Status | Purpose |
|---|---|---|
| Python + Jupyter Notebooks | Mandatory | ETL, cleaning, analysis, and KPI computation |
| Google Colab | Supported | Cloud notebook execution environment |
| Tableau Public | Mandatory | Dashboard design, publishing, and sharing |
| GitHub | Mandatory | Version control, collaboration, contribution audit |
| SQL | Optional | Initial data extraction only, if documented |

**Python Libraries:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `statsmodels`, `scikit-learn`, `nbconvert`, `ipykernel`

---

## Contribution Matrix

This table must match evidence in GitHub Insights, PR history, and committed files.

| Team Member | Dataset and Sourcing | ETL and Cleaning | EDA and Analysis | Statistical Analysis | Tableau Dashboard | Report Writing | PPT and Viva |
|---|---|---|---|---|---|---|---|
| _`Anant Jain`_ | Owner | - | - | - | Owner | - | - |
| _`Vipul Sharma`_ | Owner | Owner | Owner | - | - | - | - |
| _`Prince Singh`_ | - | Owner | - | - | - | - | - |
| _`Om Chimurkar`_ | - | - | - | Owner | - | - | Owner |
| _`Deepanshu Sharma`_ | Owner | - | - | - | - | Owner | - |
| _`Kaustubh Ranjan Sharma`_ | Owner | - | - | - | - | - | - |

*Declaration: We confirm that the above contribution details are accurate and verifiable through GitHub Insights, PR history, and submitted artifacts.*

**Team Lead Name:** Anant Jain

**Date:** 29/04/2026
