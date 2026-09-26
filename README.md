<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0B1020,50:24124D,100:0A5FFF&height=95&section=header" />

### Credit Risk Intelligence

**Retail Banking Analytics • Credit Risk • SQL • Power BI**

`25K+ Loan Records` · `GNPA` · `CIBIL` · `FOIR` · `Portfolio Risk`

</div>

---

## Project Description

**Credit Risk Intelligence** is an end-to-end BFSI data analytics project focused on analyzing retail lending risk, borrower credit quality, portfolio exposure, and default behavior.

The project uses **Python, Pandas, MySQL, SQL, and Power BI** to simulate, clean, model, analyze, and visualize retail loan data.

Python was used for data generation and ETL, MySQL was used for storing and analyzing structured data, and Power BI was used to build an interactive credit risk dashboard. :chatgpt-content-reference{index="0"}

---

## Objectives

- Analyze borrower credit risk
- Monitor loan portfolio exposure
- Identify high-risk borrower segments
- Study CIBIL and FOIR patterns
- Analyze default and GNPA trends
- Build a professional Power BI dashboard
- Create a complete analytics workflow from raw data to business insights

---

## Dataset Information

The project contains **25,000+ synthetic retail loan records** designed to simulate real-world banking data.

### Main Data Areas

#### Borrower Information

- Customer ID
- Age
- Applicant City
- Employment Type
- Annual Income

#### Credit Bureau Information

- CIBIL Score
- Active Credit Lines
- 90+ DPD History
- Credit Card Utilization

#### Loan Information

- Loan ID
- Loan Amount
- Loan Tenure
- Interest Rate
- Existing EMI
- Loan Purpose
- Application Date

The raw dataset also includes realistic data-quality issues such as inconsistent city names, missing CIBIL scores, currency formatting noise, and age outliers. :chatgpt-content-reference{index="1"}

---

## Data Cleaning & ETL

Data preparation was performed using **Python and Pandas**.

### Key Steps

- Removed duplicate records
- Cleaned currency values
- Handled missing income values
- Corrected age outliers
- Standardized city names
- Imputed missing CIBIL scores
- Created CIBIL risk categories
- Calculated EMI
- Calculated FOIR / DTI
- Split the cleaned data into analytical tables
- Loaded the final data into MySQL

The cleaned data was converted into a structured star-schema model for further analysis. :chatgpt-content-reference{index="2"}

---

## Data Model

The project uses a simple analytical data model with three main tables:

### `dim_customers`

Contains borrower demographics, city information, employment type, and annual income.

### `dim_bureau_profile`

Contains CIBIL score, credit history, credit utilization, and bureau-related risk information.

### `fact_loans`

Contains loan amount, EMI, FOIR, loan purpose, interest rate, tenure, and default status.

**Relationship**

`dim_customers → fact_loans ← dim_bureau_profile`

---

## SQL Analysis

SQL was used to answer key credit-risk and portfolio questions.

### Key Analyses

### 1. Portfolio KPI Summary

Calculated total loans, portfolio value, average values, and overall portfolio metrics.

### 2. GNPA by City

Measured Gross NPA concentration across different cities.

### 3. CIBIL × FOIR Risk Matrix

Compared borrower credit quality against repayment capacity.

### 4. High-Risk Borrower Queue

Used **CTEs and DENSE_RANK()** to identify high-risk borrowers.

### 5. Default Rate by Employment Type

Analyzed how default patterns vary across employment sectors.

### 6. Expected Credit Loss

Estimated portfolio credit loss exposure.

### 7. Risk Segmentation

Combined CIBIL, FOIR, DPD history, and borrower characteristics to identify risk segments. :chatgpt-content-reference{index="3"}

---

## Power BI Dashboard

A **3-page interactive Power BI dashboard** was created to visualize portfolio risk and lending performance. :chatgpt-content-reference{index="4"}

### Portfolio Overview

- Gross Portfolio Exposure
- Total Loans
- GNPA %
- Performing vs Default Loans
- Loan Purpose Distribution

### Risk & Default Analytics

- Monthly Default Trends
- CIBIL × FOIR Risk Matrix
- Default Rate by Employment Type
- Portfolio Risk Indicators

### Bureau & Geographic Intelligence

- GNPA by City
- Average CIBIL Score
- Credit Utilization Analysis
- Geographic Risk Comparison

### Dashboard Filters

- City
- Employment Type
- Loan Purpose
- CIBIL Tier
- FOIR Bucket
- Date Range

---

## Key Banking Metrics

### CIBIL Score

Used to evaluate borrower creditworthiness.

### FOIR / DTI

Measures how much of a borrower's income is already committed to debt obligations.

`FOIR = (Existing EMI + New EMI) / Monthly Income`

### GNPA %

Measures the proportion of the lending portfolio represented by defaulted loans.

`GNPA % = Defaulted Loan Value / Total Portfolio Value × 100`

### Expected Credit Loss

Used to estimate potential losses from borrower defaults.

---

## Key Insights

The project helps identify:

- High-risk borrower groups
- Overleveraged customers
- Cities with higher default exposure
- Risk differences across employment groups
- CIBIL and FOIR combinations associated with higher risk
- Portfolio areas requiring closer monitoring

---

## Tools & Technologies

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat-square&logo=powerbi&logoColor=black)

</div>

- Python
- Pandas
- NumPy
- MySQL
- SQLAlchemy
- SQL
- Power BI
- DAX
- Jupyter Notebook

---

## Project Deliverables

- Synthetic Credit Risk Dataset
- Python Data Generation Script
- Python ETL Pipeline
- Jupyter Notebook
- MySQL Star Schema
- SQL Analytics
- Power BI Dashboard
- Project Documentation

---

## Skills Demonstrated

`Data Cleaning` · `ETL` · `SQL` · `Data Modeling` · `Credit Risk Analytics` · `Power BI` · `DAX` · `Business Intelligence`

---

## Conclusion

This project demonstrates a complete **credit risk analytics workflow**, starting from raw lending data and ending with portfolio-level business insights.

Using **Python, SQL, MySQL, and Power BI**, the project analyzes borrower risk, credit quality, defaults, GNPA, and exposure while presenting the results through an executive-style dashboard.

---

<div align="center">

**Data → Risk → Insight**

`BFSI Analytics` · `Credit Risk` · `Power BI`

</div>
