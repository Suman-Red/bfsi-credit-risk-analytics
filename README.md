# BFSI Credit Risk Analytics Pipeline

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.26-013243?style=for-the-badge&logo=numpy&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Workbench-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

<br/>

[![Stars](https://img.shields.io/github/stars/?style=social)](.)
[![Domain](https://img.shields.io/badge/Domain-BFSI%20%7C%20Retail%20Banking-8A2BE2?style=flat-square)](.)
[![Records](https://img.shields.io/badge/Dataset-25%2C000%2B%20Loan%20Records-success?style=flat-square)](.)
[![Cities](https://img.shields.io/badge/Coverage-12%20Indian%20Cities-blue?style=flat-square)](.)

<br/>

> **An end-to-end retail banking analytics portfolio project** — synthetic loan data generation, automated ETL cleaning, analytical SQL queries, and an executive Power BI dashboard, all modeled on real BFSI underwriting workflows across 12 major Indian cities.

</div>

---

## Pipeline at a Glance

```
                                                                        
   STEP 1              STEP 2                STEP 3         STEP 4     
                                                                        
  +--------+       +-------------+        +--------+      +---------+  
  |  RAW   |  -->  |  PANDAS ETL |  -->   |  SQL   | -->  | POWER   |  
  |  DATA  |       |  CLEANSING  |        | MYSQL  |      |   BI    |  
  | 25,000 |       |  PIPELINE   |        | QUERIES|      |  DASH   |  
  | LOANS  |       |             |        |        |      | BOARD   |  
  +--------+       +-------------+        +--------+      +---------+  
  Simulator.py     cleansing_pipeline    analytics.sql   Executive      
  NumPy / Pandas   .py  or  .ipynb      7 SQL Queries   3-Page Report  
                                                                        
```

---

## Table of Contents

- [Project Overview](#project-overview)
- [Pipeline Architecture](#pipeline-architecture)
- [Step 1 — Synthetic Data Generation](#step-1--synthetic-data-generation)
- [Step 2 — Python ETL & Cleansing](#step-2--python-etl--cleansing)
- [Step 3 — SQL Analytics (MySQL)](#step-3--sql-analytics-mysql)
- [Step 4 — Power BI Dashboard](#step-4--power-bi-dashboard)
- [Key Banking Concepts](#key-banking-concepts)
- [Getting Started](#getting-started)
- [Geographic Coverage](#geographic-coverage)
- [Tech Stack](#tech-stack)
- [Resume Bullets](#resume-bullets)

---

## Project Overview

This project demonstrates a complete **retail banking credit risk workflow** — the same pipeline used by Indian BFSI institutions (banks, NBFCs) to assess and monitor retail loan portfolios.

| # | Stage | Tool | Output |
|:--|:------|:-----|:-------|
| 1 | Synthetic Data Generation | Python + NumPy | `raw_indian_credit_data.csv` (25,250 rows) |
| 2 | ETL & Data Cleansing | Python + Pandas | `dim_customers.csv`, `dim_bureau_profile.csv`, `fact_loans.csv` |
| 3 | SQL Analytics | MySQL Workbench | GNPA %, risk matrices, triage queues |
| 4 | Executive Dashboard | Power BI Desktop | 3-page interactive report with 7 DAX measures |

---

## Pipeline Architecture

```
+------------------------------------------+
|   credit_risk_portfolio_simulator.py      |
|                                           |
|   NumPy bimodal CIBIL distribution        |
|   Exponential income distribution         |
|   Correlated default flag logic           |
|   Deliberate dirty data injection:        |
|     - City spelling typos                 |
|     - Currency string noise               |
|     - Age outliers                        |
|     - Null CIBIL scores                   |
|   Output: raw_indian_credit_data.csv      |
|           25,250 rows x 15 columns        |
+--------------------+---------------------+
                     |
                     v
+------------------------------------------+
|   credit_data_cleansing_pipeline          |
|   (.py  or  .ipynb)                       |
|                                           |
|   [1] Drop duplicate (customer, loan)     |
|   [2] Regex clean currency strings        |
|   [3] Cap age outliers  (21 - 65)         |
|   [4] Normalize 12 city names             |
|   [5] Impute CIBIL by employment sector   |
|   [6] Assign CIBIL tier labels            |
|   [7] Compute reducing-balance EMI        |
|   [8] Compute FOIR / DTI ratio            |
|   [9] Split into star schema tables       |
|  [10] Push to MySQL via SQLAlchemy        |
+----------+-------------------+-----------+
           |                   |
           v                   v
   +---------------+   +--------------------+
   |  Star Schema  |   | MySQL Workbench    |
   |               |   | bfsi_credit_risk   |
   | dim_customers |   |                    |
   | dim_bureau_   |   | dim_customers      |
   |   profile     |   | dim_bureau_profile |
   | fact_loans    |   | fact_loans         |
   +---------------+   +---------+----------+
                                 |
                                 v
              +------------------------------------------+
              |   portfolio_risk_and_gnpa_analytics.sql  |
              |                                          |
              |   Query 1:  DDL + Schema Setup           |
              |   Query 2:  Portfolio KPI Summary        |
              |   Query 3:  GNPA % by City               |
              |   Query 4:  CIBIL x FOIR Risk Matrix     |
              |   Query 5:  DENSE_RANK Triage Queue      |
              |   Query 6:  Employment Default Rates      |
              |   Query 7:  ECL Loss Estimation           |
              +-------------------+----------------------+
                                  |
                                  v
              +------------------------------------------+
              |   Power BI Desktop (.pbix)               |
              |                                          |
              |   Page 1:  Portfolio Overview            |
              |   Page 2:  Risk Trends & Defaults        |
              |   Page 3:  Bureau & Geo Intelligence     |
              |                                          |
              |   Star Schema Relationships:             |
              |   fact_loans (1:M) --> dim_customers     |
              |   fact_loans (1:1) --> dim_bureau_profile|
              |                                          |
              |   7 DAX Measures (_Measures table)       |
              +------------------------------------------+
```

---

## Step 1 — Synthetic Data Generation

**File:** [`credit_risk_portfolio_simulator.py`](credit_risk_portfolio_simulator.py)

This script generates **25,000 realistic but synthetic** retail loan application records — mimicking the kind of raw, messy data that comes out of real banking CRM/LOS systems.

### What it simulates

```
BORROWER DEMOGRAPHICS
+---------------------------+
| customer_id  (IND_CUST_*) |   Sequential unique IDs
| age          (skewed)     |   Normal dist., mean=36, includes outliers
| applicant_city            |   12 cities with deliberate spelling variants
| employment_type           |   6 sectors (MNC, PSU, MSME, Gig, etc.)
+---------------------------+

CREDIT BUREAU DATA
+---------------------------+
| cibil_score (bimodal)     |   70% Prime (mean=760), 30% Subprime (mean=610)
| active_credit_lines       |   Poisson(lambda=3)
| historical_dpd_90         |   82% have 0 delinquencies
| credit_card_utilization   |   Beta(2,5) x 100
+---------------------------+

LOAN APPLICATION DATA
+---------------------------+
| loan_id      (LN_IN_*)    |   Sequential loan IDs
| applied_loan_amount       |   Discrete bands: 50K to 20L
| loan_tenure_months        |   12, 24, 36, 48, 60, 84 months
| interest_rate_pct         |   Uniform(9.5, 24.0)
| existing_monthly_emi      |   Up to 40% of monthly income
| loan_purpose              |   7 categories
| application_date          |   Jan 2024 - Dec 2025 (730 days)
+---------------------------+

DELIBERATE DIRTY DATA (for ETL practice)
+----------------------------------+
| "Bombay" / "BLR" / "Calcutta"   |  City typos to normalize
| "Rs. 4,50,000/-" / "INR 450000" |  Currency format noise
| age = 15, age = 72              |  Out-of-policy age values
| cibil_score = NaN               |  ~8% missing bureau scores
+----------------------------------+
```

### Default flag logic (correlated)

```
Default Probability driven by:
   High FOIR  (>50%)       +++ weight
   Subprime CIBIL (<650)   +++ weight
   Past 90 DPD history     +++ weight
   --> sigmoid transform --> default_status (0 or 1)
```

---

## Step 2 — Python ETL & Cleansing

**Files:** [`credit_data_cleansing_pipeline.py`](credit_data_cleansing_pipeline.py) | [`credit_data_cleansing_pipeline.ipynb`](credit_data_cleansing_pipeline.ipynb)

A streamlined ~128-line production ETL pipeline that takes the raw dirty CSV and outputs clean, analysis-ready star schema tables.

### Transformation Steps

```
RAW INPUT (25,250 rows x 15 cols)
|
+-- [1] DEDUPLICATION
|       df.drop_duplicates(subset=["customer_id", "loan_id"])
|
+-- [2] CURRENCY SANITIZATION
|       Regex strips: "Rs.", "INR", "/-", commas, spaces
|       Values < 1,00,000 --> NaN (invalid income)
|       Fallback: group median by employment_type
|
+-- [3] INCOME OUTLIER CAPPING
|       Winsorize at 1st and 99th percentile
|
+-- [4] AGE OUTLIER CORRECTION
|       Age < 21 or > 65 --> replaced with median age
|       (RBI retail lending policy bounds)
|
+-- [5] CITY NAME NORMALIZATION (12 cities, ~30 variants)
|       Regex pattern map:
|       "Bombay"/"MUMBAI"/"Bombay City" --> "Mumbai"
|       "BLR"/"Bangalore"/"Blore"       --> "Bengaluru"
|       "Gurgaon"/"Noida"/"NCR"         --> "Delhi NCR"
|       ... (full 12-city coverage)
|
+-- [6] CITY TIER CLASSIFICATION
|       Tier 1 (Metro): 6 cities
|       Tier 2 (Growth): 6 cities
|
+-- [7] CIBIL SCORE IMPUTATION
|       Missing CIBIL filled with employment sector median
|       Flag column: is_cibil_imputed (0/1)
|
+-- [8] CIBIL TIER LABELING
|       750+    --> "Prime (750+)"
|       650-749 --> "Near Prime (650-749)"
|       550-649 --> "Subprime (550-649)"
|       <550    --> "Deep Subprime (<550)"
|
+-- [9] REDUCING-BALANCE EMI CALCULATION
|       EMI = P * r * (1+r)^n / ((1+r)^n - 1)
|       r = annual_rate / 12 / 100
|
+-- [10] FOIR / DTI RATIO
|        FOIR = (existing_emi + new_emi) / monthly_income
|        Bucket: <=30% | 31-50% | >50% (overleveraged)
|
+-- [11] STAR SCHEMA SPLIT
|        dim_customers      (6 cols)
|        dim_bureau_profile (8 cols, bureau_profile_id key)
|        fact_loans         (11 cols)
|
+-- [12] MYSQL PUSH via SQLAlchemy
         engine = create_engine("mysql+pymysql://...")
         df.to_sql(table, engine, if_exists="replace")
```

### Output Star Schema

```
                    +------------------+
                    |  dim_customers   |
                    +------------------+
                    | customer_id (PK) |
                    | age              |
                    | applicant_city   |
                    | city_tier        |
                    | employment_type  |
                    | annual_income_inr|
                    +--------+---------+
                             |
              +--------------+---------------+
              |                              |
    +---------+----------+      +-----------+-----------+
    |     fact_loans     |      | dim_bureau_profile    |
    +--------------------+      +-----------------------+
    | loan_id (PK)       |      | bureau_profile_id (PK)|
    | customer_id (FK)   |      | customer_id (FK)      |
    | application_date   |      | cibil_score           |
    | sanctioned_amount  |      | cibil_tier            |
    | loan_tenure_months |      | is_cibil_imputed      |
    | interest_rate_pct  |      | active_credit_lines   |
    | calculated_emi     |      | historical_dpd_90     |
    | foir_dti_ratio     |      | cc_utilization_pct    |
    | foir_bucket        |      +-----------------------+
    | loan_purpose       |
    | is_default         |
    +--------------------+
```

---

## Step 3 — SQL Analytics (MySQL)

**File:** [`portfolio_risk_and_gnpa_analytics.sql`](portfolio_risk_and_gnpa_analytics.sql)

7 production-grade analytical queries written for **MySQL Workbench** (`USE bfsi_credit_risk;`).

### Queries at a Glance

```
+-------+--------------------------------------------+----------------------------+
| Query | Business Question                          | SQL Techniques Used        |
+-------+--------------------------------------------+----------------------------+
|   1   | DDL: Create all 3 tables with constraints  | CREATE TABLE, PRIMARY KEY  |
|   2   | Portfolio KPI summary                      | COUNT, SUM, AVG, ROUND     |
|   3   | GNPA % by city (defaults vs sanctioned amt)| GROUP BY, CASE WHEN, ROUND |
|   4   | CIBIL tier x FOIR bucket risk matrix       | GROUP BY two dimensions    |
|   5   | Top 100 highest-risk borrower triage queue | CTE + DENSE_RANK()         |
|   6   | Default rate by employment sector          | GROUP BY, HAVING, ORDER BY |
|   7   | Expected Credit Loss (ECL) estimation      | JOIN, aggregate formulas   |
+-------+--------------------------------------------+----------------------------+
```

### Example: GNPA % by City (Query 3)

```sql
SELECT
    c.applicant_city,
    COUNT(f.loan_id)                                          AS total_loans,
    SUM(CASE WHEN f.is_default = 1 THEN 1 ELSE 0 END)        AS defaulted_loans,
    ROUND(
        SUM(CASE WHEN f.is_default = 1
                 THEN f.sanctioned_loan_amount_inr ELSE 0 END)
        / SUM(f.sanctioned_loan_amount_inr) * 100, 2
    )                                                         AS gnpa_pct
FROM fact_loans f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.applicant_city
ORDER BY gnpa_pct DESC;
```

### Example: Triage Queue with Window Function (Query 5)

```sql
WITH risk_scored AS (
    SELECT
        f.loan_id,
        f.customer_id,
        b.cibil_score,
        f.foir_dti_ratio,
        b.historical_dpd_90,
        DENSE_RANK() OVER (
            ORDER BY b.cibil_score ASC,
                     f.foir_dti_ratio DESC,
                     b.historical_dpd_90 DESC
        ) AS risk_rank
    FROM fact_loans f
    JOIN dim_bureau_profile b ON f.customer_id = b.customer_id
    WHERE f.is_default = 0   -- performing but high-risk
)
SELECT * FROM risk_scored WHERE risk_rank <= 100;
```

---

## Step 4 — Power BI Dashboard

**Reference:** [`credit_risk_powerbi_blueprint.md`](credit_risk_powerbi_blueprint.md)

A 3-page executive dashboard built in **Power BI Desktop**, connected directly to the `bfsi_credit_risk` MySQL database.

### Data Model (Star Schema in Power BI)

```
                 +---------------------+
                 |    _Measures        |  <-- Isolated DAX measure table
                 | (7 DAX measures)    |
                 +---------------------+

  +------------------+        +--------------------+
  |  dim_customers   |        | dim_bureau_profile |
  +------------------+        +--------------------+
  | customer_id (PK) |        | customer_id (FK)   |
  +--------+---------+        +---------+----------+
           |  1:M                       |  1:1
           |                            |
           +----------+  +--------------+
                      |  |
               +------+--+--------+
               |     fact_loans   |
               +------------------+
               | loan_id          |
               | customer_id (FK) |
               +------------------+
```

### 7 DAX Measures

```
Measure Name               Formula (simplified)
--------------------------+------------------------------------------
Gross Disbursed Amount     SUM(fact_loans[sanctioned_loan_amount_inr])
Total Loans                COUNTROWS(fact_loans)
Total Defaults             CALCULATE(COUNTROWS(), is_default=1)
GNPA Amount                CALCULATE(SUM(amount), is_default=1)
GNPA %                     DIVIDE([GNPA Amount], [Gross Disbursed Amount])
Default Rate %             DIVIDE([Total Defaults], [Total Loans])
Average CIBIL Score        AVERAGE(dim_bureau_profile[cibil_score])
```

### Dashboard Pages

```
+----------------------------------------------------------+
|  PAGE 1: Portfolio Overview                              |
|                                                          |
|  [KPI Card]        [KPI Card]       [KPI Card]           |
|  Gross Portfolio   Total Loans      GNPA %               |
|  Rs. X Cr          25,000+          X.XX%                |
|                                                          |
|  [Clustered Bar]                   [Donut Chart]         |
|  Performing vs Default by City     Loan Purpose Split    |
|                                                          |
|  [FILTERS] City | Employment Type | Loan Purpose         |
+----------------------------------------------------------+

+----------------------------------------------------------+
|  PAGE 2: Risk Trends & Default Analytics                 |
|                                                          |
|  [Line Chart]                      [Matrix / Heatmap]   |
|  Monthly Default Inflow Over Time  CIBIL Tier x FOIR     |
|                                                          |
|  [Bar Chart]                       [KPI Card]            |
|  Default Rate by Employment Sector  Default Rate %       |
|                                                          |
|  [FILTERS] Date Range | CIBIL Tier | FOIR Bucket         |
+----------------------------------------------------------+

+----------------------------------------------------------+
|  PAGE 3: Bureau & Geographic Intelligence                |
|                                                          |
|  [Treemap]                         [Column Chart]        |
|  GNPA Amount by City               Avg CIBIL by City     |
|                                                          |
|  [Bar Chart]                       [KPI Card]            |
|  CC Utilization Tier Distribution  Avg CIBIL Score       |
|                                                          |
|  [FILTERS] City Tier | CIBIL Tier                        |
+----------------------------------------------------------+
```

---

## Key Banking Concepts

### CIBIL Score Tiers (India — 300 to 900)

```
  300        550        650        750       900
   |----------|----------|----------|----------|
   [Deep Sub] [Subprime ] [NearPrime] [  Prime ]
   <550       550-649    650-749    750+
   High Risk  Monitored  Standard   Low Risk
```

### Formulas Implemented

**Reducing-Balance Monthly EMI**

$$\text{EMI} = P \times r \times \frac{(1+r)^n}{(1+r)^n - 1}$$

> $P$ = Principal Amount, $r$ = Monthly Interest Rate (`annual_rate / 12 / 100`), $n$ = Tenure in Months

**FOIR / DTI — Fixed Obligation to Income Ratio**

$$\text{FOIR} = \frac{\text{Existing Monthly EMIs} + \text{Proposed New EMI}}{\text{Net Monthly Income}}$$

> RBI retail benchmark: **<= 50%**. Borrowers above this are classified as **Overleveraged**.

**Gross Non-Performing Asset Ratio (GNPA %)**

$$\text{GNPA \%} = \frac{\text{Total Sanctioned Value of Defaulted Loans}}{\text{Total Sanctioned Portfolio Value}} \times 100$$

> RBI: Any loan with **90+ Days Past Due (DPD)** is classified as a Non-Performing Asset (NPA).

### FOIR Risk Buckets

```
  FOIR Bucket        Label             Risk Signal
  <=30%           "Low Debt"          Safe — strong repayment capacity
  31-50%          "Moderate Debt"     Standard — within RBI limit
  >50%            "Overleveraged"     High Risk — policy exception required
```

---

## Getting Started

### Prerequisites

```bash
pip install pandas numpy sqlalchemy pymysql
```

> MySQL Workbench must be running on `localhost:3306`. If unavailable, the pipeline still exports clean CSVs locally.

---

### Step 1 — Generate Raw Data

```powershell
python credit_risk_portfolio_simulator.py
```

Output: `raw_indian_credit_data.csv` — 25,250 records with intentional noise.

---

### Step 2 — Clean & Model the Data

**Option A — Python script:**
```powershell
python credit_data_cleansing_pipeline.py
```

**Option B — Interactive Jupyter notebook:**
```powershell
jupyter lab credit_data_cleansing_pipeline.ipynb
```

Outputs three clean CSV files + auto-pushes to MySQL:

```
dim_customers.csv        6 columns, one row per borrower
dim_bureau_profile.csv   8 columns, credit bureau data
fact_loans.csv          11 columns, one row per loan application
```

---

### Step 3 — Run SQL Queries (MySQL Workbench)

1. Open MySQL Workbench and connect to `localhost:3306`
2. Open `portfolio_risk_and_gnpa_analytics.sql`
3. Run queries individually by highlighting and pressing **Ctrl + Shift + Enter**

---

### Step 4 — Build the Power BI Report

1. Open **Power BI Desktop**
2. **Get Data** → MySQL Database → `localhost` → `bfsi_credit_risk`
3. Load all 3 tables (`dim_customers`, `dim_bureau_profile`, `fact_loans`)
4. Set relationships in **Model View** (see blueprint below)
5. Create `_Measures` table and add 7 DAX measures
6. Build the 3-page report layout

Full step-by-step guide: [`credit_risk_powerbi_blueprint.md`](credit_risk_powerbi_blueprint.md)

---

## Geographic Coverage

```
TIER 1 — METRO HUBS (6 cities)
+-----------------------------------------------------------+
| Mumbai      | Delhi NCR  | Bengaluru                     |
| Hyderabad   | Chennai    | Kolkata                       |
+-----------------------------------------------------------+
Normalized from: Bombay, New Delhi, Gurgaon, Noida, BLR,
Bangalore, Blore, Cyberabad, Secunderabad, Madras, Calcutta

TIER 2 — GROWTH HUBS (6 cities)
+-----------------------------------------------------------+
| Pune        | Ahmedabad  | Jaipur                        |
| Lucknow     | Chandigarh | Kochi                         |
+-----------------------------------------------------------+
Normalized from: Poona, AMD, Amdavad, JPR, Pink City,
LKO, CHD, Tricity, Cochin, Ernakulam
```

---

## Project Files

| File | Purpose |
| :--- | :--- |
| [`credit_risk_portfolio_simulator.py`](credit_risk_portfolio_simulator.py) | Generates 25,000 synthetic loan records with deliberate noise |
| [`credit_data_cleansing_pipeline.py`](credit_data_cleansing_pipeline.py) | Python ETL: 12-step cleansing + star schema export + MySQL push |
| [`credit_data_cleansing_pipeline.ipynb`](credit_data_cleansing_pipeline.ipynb) | Interactive Jupyter version of the ETL pipeline |
| [`portfolio_risk_and_gnpa_analytics.sql`](portfolio_risk_and_gnpa_analytics.sql) | 7 analytical SQL queries for MySQL Workbench |
| [`credit_risk_powerbi_blueprint.md`](credit_risk_powerbi_blueprint.md) | Power BI setup guide: relationships, DAX measures, report layout |

---

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| Data Simulation | Python 3.11, NumPy (bimodal dist), Pandas |
| ETL & Cleansing | Pandas, Regex (re), SQLAlchemy, PyMySQL |
| Data Warehouse | MySQL Workbench — `bfsi_credit_risk` database |
| SQL Analytics | MySQL — CTEs, Window Functions, GROUP BY, JOINs |
| BI & Reporting | Power BI Desktop — Star Schema, DAX, Slicers |
| Notebook | Jupyter Lab / VS Code Jupyter extension |

---

## Resume Bullets

> Copy-paste ready for your Data Analyst CV:

- Simulated **25,000+ synthetic retail loan applications** in Python (NumPy bimodal CIBIL distributions, correlated default logic, deliberate dirty data) to replicate real-world BFSI CRM/LOS data quality issues
- Built a **12-step Pandas ETL pipeline** handling currency regex sanitization, age capping, 12-city name normalization (~30 typo variants), CIBIL imputation by employment sector, and reducing-balance EMI/FOIR computation
- Designed and populated a **MySQL star schema** (`dim_customers`, `dim_bureau_profile`, `fact_loans`) via SQLAlchemy, authoring 7 analytical queries using CTEs, `DENSE_RANK()` window functions, and `CASE WHEN` logic to compute Gross NPA %, ECL loss, and underwriting triage queues
- Built a **3-page executive Power BI dashboard** with a star-schema data model, 7 DAX measures (GNPA %, Default Rate %, Average CIBIL), and interactive slicers for city, employment type, CIBIL tier, and FOIR bucket

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

<div align="center">

**BFSI Credit Risk Analytics** &nbsp;|&nbsp; Indian Retail Banking Domain &nbsp;|&nbsp; Portfolio Project

</div>
