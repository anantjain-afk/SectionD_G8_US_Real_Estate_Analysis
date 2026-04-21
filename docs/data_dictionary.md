# Data Dictionary — US Real Estate Analysis

This document provides a comprehensive comparison between the **Raw Dataset** (pre-cleaning) and the **Analytical Dataset** (post-cleaning). The pipeline transforms a noisy, incomplete sample into a production-ready file for Tableau and statistical modeling.

---

## 1. Summary of Transformation

| Metric | Raw (Pre-Cleaning) | Processed (Post-Cleaning) | Change Reasoning |
| :--- | :--- | :--- | :--- |
| **Total Rows** | 80,000 | **59,581** | Removed LOTs and records with invalid postcodes/prices (source: `raw_extracted_data.csv`). |
| **Total Columns**| 28 | **19** | Dropped metadata, redundant unit columns, and high-null fields. |
| **Data Health** | ~20% Nulls in rooms/space | **0% Nulls** | All missing values imputed via hierarchical medians. |
| **Invalid Zeros** | ~7,000 (beds/baths/space) | **0** | Zeros treated as `NaN` and recovered using median ratios. |
| **Consistency** | Acres + SqFt mixed | **SqFt Only** | Standardized all land area measurements to Square Feet. |

---

## 2. Detailed Column Mapping & Cleaning Logic

### 🌍 Identification & Location
| Column | Raw State | Processed State | Detailed Cleaning Action |
| :--- | :--- | :--- | :--- |
| **property_id** | Unique Int | Unique Int | Kept as the primary key. |
| **address** | Full string | Full string | Preserved for reference and used for regex recovery. |
| **street_name** | 22 Nulls | **0 Nulls** | Recovered missing values by parsing `address` string with regex. |
| **city** | Complete | **Complete** | Standardized casing and recovered missing values via `address` parsing. |
| **state** | 1 Null | **0 Nulls** | Standardized to US 2-letter codes. |
| **postcode** | 2 Nulls | **0 Nulls** | Rows with null postcodes were dropped as they cannot be mapped. |
| **latitude** | 9,415 Nulls | **0 Nulls** | Imputed via **Hierarchical Centroid**: Postcode median → City median → State median. |
| **longitude** | 9,415 Nulls | **0 Nulls** | Imputed via **Hierarchical Centroid**: Postcode median → City median → State median. |

### 🏠 Property Features
| Column | Raw State | Processed State | Detailed Cleaning Action |
| :--- | :--- | :--- | :--- |
| **Bedrooms** | 20,563 Nulls + 965 Zeros | **0 Nulls / Zeros** | (1) Treated `0` as `NaN`. (2) Imputed using `Living_Space / Median_SqFt_Per_Bed`. (3) Clamped to **[1, 10]**. |
| **Bathrooms** | 16,952 Nulls + 4,385 Zeros| **0 Nulls / Zeros** | (1) Treated `0` as `NaN`. (2) Imputed using `Living_Space / Median_SqFt_Per_Bath`. (3) Clamped to **[1, 10]**. |
| **Living_Space_SqFt**| 20,064 Nulls + 1,637 Zeros| **0 Nulls / Zeros** | (1) Treated `0` as `NaN`. (2) Imputed from Bedrooms (Tier 1) or Price (Tier 2). |
| **land_space** | 11,321 Nulls | **0 Nulls** | (1) Converted Acres → SqFt. (2) Replaced negative values and nulls with city-level medians. |
| **property_type** | 7 types (incl. LOT) | **Residential Only** | **Dropped LOTs** (20,418 rows) to focus analysis on buildings/dwellings. |
| **property_status**| FOR_SALE / SOLD | FOR_SALE / SOLD | Preserved. Used to segment market types in Tableau. |
| **agency_name** | 20,771 Nulls | **0 Nulls** | All missing broker names filled with **"Unknown Agency"** for clean categorical grouping. |

### 💰 Financials & Derived Metrics
| Column | Raw State | Processed State | Detailed Cleaning Action |
| :--- | :--- | :--- | :--- |
| **Sale_Price** | `price` column | `Sale_Price` | Renamed for clarity. Filtered out any $0 or negative values. |
| **Sale_Price_Capped**| (New Metric) | Max ~$4.6M | Capped at the **99th percentile** to prevent extreme luxury home skewing average trends. |
| **Living_Space_Capped**| (New Metric) | Max ~7,200 sqft | Capped at the **99th percentile** for stable visualization of bulk market density. |
| **Price_Per_SqFt** | Inconsistent | Recalculated | Calculated as `Sale_Price / Living_Space_SqFt` to ensure mathematical consistency. |

---

## 3. Discarded Columns (Post-Cleaning)

| Column | Reason for Exclusion |
| :--- | :--- |
| **property_url** | Non-analytical string metadata. |
| **listing_age** | Corrupted data: all values were `-1`. |
| **RunDate** | Redundant: single scrape date (`2022-04-24`) for 100% of rows. |
| **apartment** | 97% Null. Insufficient data for building-type analysis. |
| **broker_id** | Internal Zillow database IDs; no market value. |
| **year_build** | 100% Null in the 80k sample. |
| **total_num_units**| 100% Null in the 80k sample. |
| **agent_info** | `agent_name` and `agent_phone` were 100% null/private. |
| **land_space_unit**| Redundant after all land space was converted to Square Feet. |
| **price_per_unit** | Inaccurate raw calculation; replaced by our `Price_Per_SqFt`. |
| **is_owned_by_zillow**| 100% false/null variation; non-discriminate flag. |
