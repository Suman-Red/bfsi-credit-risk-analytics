import os
import re
from pathlib import Path
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text

# database login credentials for mysql workbench
MYSQL_USER = "root"
MYSQL_PASSWORD = "0000"
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DATABASE = "bfsi_credit_risk"

# loading raw loan application data
base_dir = Path(__file__).resolve().parent
df = pd.read_csv(base_dir / "raw_indian_credit_data.csv")

# removing duplicate loan applications
initial_rows = len(df)
df = df.drop_duplicates(subset=["customer_id", "loan_id"]).copy()
print(f"Removed {initial_rows - len(df)} duplicate loan applications")

# cleaning currency symbols, commas, and formatting from stated income
def clean_currency(val):
    if pd.isna(val): return np.nan
    s = re.sub(r"(?i)rs\.?|inr|/-\s*$", "", str(val))
    cleaned = re.sub(r"[^\d.]", "", s)
    try:
        num = float(cleaned)
        return num if num >= 100_000 else np.nan
    except ValueError:
        return np.nan

df["annual_income_inr"] = df["stated_annual_income"].apply(clean_currency)
df["annual_income_inr"] = df["annual_income_inr"].fillna(df.groupby("employment_type")["annual_income_inr"].transform("median"))
df["annual_income_inr"] = df["annual_income_inr"].fillna(df["annual_income_inr"].median())

# capping extreme income typos (1st to 99th percentile)
df["annual_income_inr"] = df["annual_income_inr"].clip(df["annual_income_inr"].quantile(0.01), df["annual_income_inr"].quantile(0.99))

# fixing age typos to retail lending limits (21 to 65)
median_age = int(df["age"].median())
df["age"] = df["age"].apply(lambda x: median_age if x < 21 or x > 65 else x)

# standardizing spelling errors across 12 major indian cities
city_cleaning_rules = {
    r"(?i).*(bangalore|blr|bengaluru|blore).*": "Bengaluru",
    r"(?i).*(bombay|mumbai).*": "Mumbai",
    r"(?i).*(delhi|ncr|gurgaon|noida).*": "Delhi NCR",
    r"(?i).*(hyd|hyderabad|cyberabad|secunderabad).*": "Hyderabad",
    r"(?i).*(pune|poona).*": "Pune",
    r"(?i).*(madras|chennai).*": "Chennai",
    r"(?i).*(calcutta|kolkata).*": "Kolkata",
    r"(?i).*(ahmedabad|amd|amdavad).*": "Ahmedabad",
    r"(?i).*(jaipur|jpr|pink city).*": "Jaipur",
    r"(?i).*(lucknow|lko).*": "Lucknow",
    r"(?i).*(chandigarh|chd|tricity).*": "Chandigarh",
    r"(?i).*(kochi|cochin|ernakulam).*": "Kochi"
}
for pattern, clean_city in city_cleaning_rules.items():
    df["applicant_city"] = df["applicant_city"].replace(pattern, clean_city, regex=True)

# mapping cities into tier 1 and tier 2 lending categories
tier1_metros = ["Bengaluru", "Mumbai", "Delhi NCR", "Hyderabad", "Chennai", "Kolkata"]
df["city_tier"] = df["applicant_city"].apply(lambda x: "Tier 1" if x in tier1_metros else "Tier 2")

# filling missing cibil scores using employment sector medians
df["employment_type"] = df["employment_type"].fillna("Salaried - Private")
df["is_cibil_imputed"] = df["cibil_score"].isna().astype(int)
df["cibil_score"] = df["cibil_score"].fillna(df.groupby("employment_type")["cibil_score"].transform("median")).round().astype(int)
df["credit_card_utilization_pct"] = df["credit_card_utilization_pct"].fillna(df["credit_card_utilization_pct"].median()).round(1)

# labeling cibil score risk tiers (prime, near prime, subprime, deep subprime)
def assign_cibil_band(score):
    if score >= 750: return "Prime (750+)"
    if score >= 650: return "Near Prime (650-749)"
    if score >= 550: return "Subprime (550-649)"
    return "Deep Subprime (<550)"
df["cibil_tier"] = df["cibil_score"].apply(assign_cibil_band)

# calculating reducing-balance monthly emi and debt burden ratio (foir)
df["monthly_income_inr"] = np.round(df["annual_income_inr"] / 12.0, 2)
monthly_interest_rate = (df["interest_rate_pct"] / 100.0) / 12.0
tenure_months = df["loan_tenure_months"]
loan_amount = df["applied_loan_amount"]

# reducing-balance loan installment formula
df["calculated_monthly_emi"] = np.round(
    loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** tenure_months) / (((1 + monthly_interest_rate) ** tenure_months) - 1), 2
)
df["total_monthly_obligations"] = np.round(df["existing_monthly_emi"] + df["calculated_monthly_emi"], 2)
df["foir_dti_ratio"] = np.round(df["total_monthly_obligations"] / df["monthly_income_inr"], 4)
df["foir_bucket"] = df["foir_dti_ratio"].apply(
    lambda x: "<=30% (Low Debt)" if x <= 0.30 else ("31-50% (Moderate Debt)" if x <= 0.50 else ">50% (Overleveraged)")
)

# splitting cleaned data into star schema relational tables
dim_customers = df[["customer_id", "age", "applicant_city", "city_tier", "employment_type", "annual_income_inr"]].copy()

dim_bureau_profile = df[["customer_id", "cibil_score", "cibil_tier", "is_cibil_imputed", "active_credit_lines", "historical_dpd_90", "credit_card_utilization_pct"]].copy()
dim_bureau_profile.insert(0, "bureau_profile_id", [f"BUR_{i:06d}" for i in range(1, len(dim_bureau_profile) + 1)])

fact_loans = df[["loan_id", "customer_id", "application_date", "applied_loan_amount", "loan_tenure_months", "interest_rate_pct", "calculated_monthly_emi", "foir_dti_ratio", "foir_bucket", "loan_purpose", "default_status"]].copy()
fact_loans.rename(columns={"applied_loan_amount": "sanctioned_loan_amount_inr", "default_status": "is_default"}, inplace=True)

# saving clean csv files
dim_customers.to_csv(base_dir / "dim_customers.csv", index=False)
dim_bureau_profile.to_csv(base_dir / "dim_bureau_profile.csv", index=False)
fact_loans.to_csv(base_dir / "fact_loans.csv", index=False)

# pushing clean tables directly into mysql workbench database
try:
    server_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}"
    server_engine = create_engine(server_url)
    with server_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE};"))
        conn.commit()
    
    db_engine = create_engine(f"{server_url}/{MYSQL_DATABASE}")
    dim_customers.to_sql("dim_customers", db_engine, if_exists="replace", index=False, chunksize=5000)
    dim_bureau_profile.to_sql("dim_bureau_profile", db_engine, if_exists="replace", index=False, chunksize=5000)
    fact_loans.to_sql("fact_loans", db_engine, if_exists="replace", index=False, chunksize=5000)
    print(f"ETL pipeline complete: pushed 3 clean tables into MySQL Workbench database '{MYSQL_DATABASE}'.")
except Exception as e:
    print("ETL complete! Saved clean CSVs locally.")
    print(f"MySQL Note: Could not connect to MySQL Workbench ({e}).")
