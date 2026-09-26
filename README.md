<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:050816,45:351063,100:0066FF&height=120&section=header&text=CREDIT%20RISK%20INTELLIGENCE&fontSize=28&fontColor=FFFFFF&fontAlignY=42&desc=Retail%20Banking%20%7C%20Risk%20Analytics%20%7C%20Power%20BI&descSize=13&descAlignY=68" />

<br>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)

<br>

### Portfolio Snapshot

<img src="https://img.shields.io/badge/25K%2B-LOAN_RECORDS-6C3BFF?style=for-the-badge"/>
<img src="https://img.shields.io/badge/12-INDIAN_CITIES-0066FF?style=for-the-badge"/>
<img src="https://img.shields.io/badge/3-DASHBOARD_PAGES-A020F0?style=for-the-badge"/>
<img src="https://img.shields.io/badge/7-SQL_ANALYSES-0078FF?style=for-the-badge"/>

</div>

---

### ✦ Project Overview

**Credit Risk Intelligence** is an end-to-end BFSI analytics project focused on retail lending, borrower risk and portfolio performance.

The project transforms raw loan data into structured analytical insights using:

> **Python → Pandas ETL → MySQL → SQL Analytics → Power BI**

The dataset contains **25,000+ synthetic loan records** across **12 Indian cities**, designed with realistic borrower, bureau and lending characteristics. :chatgpt-content-reference{index="0"}

---

### ✦ Dashboard

<p align="center">
  <img src="assets/dashboard_overview.png" width="100%" alt="Credit Risk Intelligence Dashboard"/>
</p>

<div align="center">

`Portfolio Exposure` • `GNPA` • `CIBIL` • `FOIR` • `Defaults`

</div>

---

### ✦ Dataset

#### 👤 Borrower Profile

`Customer ID` · `Age` · `City` · `Employment Type` · `Annual Income`

#### 💳 Credit Profile

`CIBIL Score` · `Credit Lines` · `DPD History` · `Credit Utilization`

#### 🏦 Loan Profile

`Loan Amount` · `Tenure` · `Interest Rate` · `EMI` · `Loan Purpose` · `Application Date`

#### ⚠ Data Quality

`Missing Values` · `City Variations` · `Age Outliers` · `Currency Noise`

---

### ✦ Data Preparation

The raw data was cleaned and transformed using **Python + Pandas**.

- Duplicate removal
- Missing-value handling
- Currency standardization
- Age outlier correction
- City normalization
- CIBIL imputation
- CIBIL risk segmentation
- EMI calculation
- FOIR /  DTI calculation
- Star-schema preparation

The pipeline then loads the analytical tables into MySQL for SQL analysis. :chatgpt-content-reference{index="1"}

---

### ✦ Data Model

| Table | Purpose |
|:--|:--|
| `dim_customers` | Borrower demographics, income and location |
| `dim_bureau_profile` | CIBIL, DPD and credit utilization |
| `fact_loans` | Loan exposure, EMI, FOIR and defaults |

<div align="center">

`dim_customers` → **fact_loans** ← `dim_bureau_profile`

</div>

---

### ✦ SQL Analytics

The analytical layer answers key portfolio-risk questions.

| # | Analysis |
|:--:|:--|
| `01` | Portfolio KPI Summary |
| `02` | GNPA by City |
| `03` | CIBIL × FOIR Risk Matrix |
| `04` | High-Risk Borrower Ranking |
| `05` | Default Rate by Employment |
| `06` | Expected Credit Loss |
| `07` | Risk Segmentation |

**SQL techniques**

`JOIN` · `GROUP BY` · `CASE WHEN` · `CTE` · `DENSE_RANK()` · `Window Functions`

:chatgpt-content-reference{index="2"}

---

### ✦ Power BI

The project includes a **3-page interactive executive dashboard**. :chatgpt-content-reference{index="3"}

#### `01` Portfolio Overview

> Exposure • Total Loans • GNPA • Loan Purpose • City Performance

#### `02` Risk & Defaults

> Default Trends • CIBIL × FOIR • Employment Risk • Default Rate

#### `03` Bureau & Geography

> GNPA by City • CIBIL • Credit Utilization • Geographic Risk

---

### ✦ Key Metrics

<div align="center">

| Metric | Purpose |
|:--|:--|
| **CIBIL** | Borrower credit quality |
| **FOIR / DTI** | Debt repayment capacity |
| **GNPA %** | Portfolio default exposure |
| **Default Rate** | Default frequency |
| **ECL** | Expected credit loss |

</div>

#### FOIR

```text
(Existing EMI + New EMI) / Monthly Income
