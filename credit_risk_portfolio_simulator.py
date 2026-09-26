import random
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import pandas as pd

# setting random seed so our sample results are reproducible
np.random.seed(42)
random.seed(42)
num_borrowers = 25000
out_file = Path(__file__).resolve().parent / "raw_indian_credit_data.csv"

# major 12 indian cities and common branch spelling mistakes
cities = [
    "Mumbai", "Delhi NCR", "Bengaluru", "Hyderabad", "Chennai", "Kolkata",
    "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Chandigarh", "Kochi"
]
city_spelling_mistakes = {
    "Mumbai": ["Mumbai", "Bombay", "mumbai", "MUMBAI", "Bombay City"],
    "Delhi NCR": ["Delhi NCR", "New Delhi", "Delhi", "delhi", "NCR", "Gurgaon", "Noida"],
    "Bengaluru": ["Bengaluru", "Bangalore", "BLR", "bengaluru", "bangalore ", "Blore"],
    "Hyderabad": ["Hyderabad", "HYD", "hyderabad", "Cyberabad", "Secunderabad"],
    "Chennai": ["Chennai", "Madras", "chennai", "CHENNAI"],
    "Kolkata": ["Kolkata", "Calcutta", "kolkata", "Calcutta City"],
    "Pune": ["Pune", "pune", "PUNE", "Poona"],
    "Ahmedabad": ["Ahmedabad", "ahmedabad", "AMD", "Amdavad"],
    "Jaipur": ["Jaipur", "jaipur", "JPR", "Pink City"],
    "Lucknow": ["Lucknow", "lucknow", "LKO"],
    "Chandigarh": ["Chandigarh", "chandigarh", "CHD", "Tricity"],
    "Kochi": ["Kochi", "Cochin", "kochi", "Ernakulam"]
}
employment_sectors = ["Salaried - MNC", "Salaried - Private", "Salaried - PSU/Govt", "Self-Employed Professional", "MSME / Small Business", "Gig Economy Worker"]
loan_reasons = ["Debt Consolidation", "Home Renovation", "Medical Emergency", "Wedding/Family Event", "Business Expansion", "Two-Wheeler/Vehicle", "Education Expense"]

# generating borrower demographics and financial profiles
customer_ids = [f"IND_CUST_{100000 + i}" for i in range(num_borrowers)]
loan_ids = [f"LN_IN_{20240000 + i}" for i in range(num_borrowers)]
application_dates = [(datetime(2024, 1, 1) + timedelta(days=int(d))).strftime("%Y-%m-%d") for d in np.random.randint(0, 730, num_borrowers)]
borrower_ages = np.random.normal(36, 9, num_borrowers).astype(int)
annual_incomes = np.round(np.random.exponential(650000, num_borrowers) + 250000, -3)

# bimodal cibil credit score distribution (prime vs subprime)
prime_scores = np.random.normal(760, 45, int(num_borrowers * 0.70))
subprime_scores = np.random.normal(610, 60, num_borrowers - int(num_borrowers * 0.70))
cibil_scores = np.concatenate([prime_scores, subprime_scores])
np.random.shuffle(cibil_scores)
cibil_scores = np.clip(np.round(cibil_scores), 300, 900)

# loan amounts, repayment tenures, interest rates, and existing obligations
loan_amounts = np.random.choice([50000, 100000, 200000, 350000, 500000, 750000, 1000000, 1500000, 2000000], num_borrowers, p=[0.10, 0.15, 0.20, 0.15, 0.15, 0.10, 0.08, 0.04, 0.03])
loan_tenures = np.random.choice([12, 24, 36, 48, 60, 84], num_borrowers, p=[0.10, 0.20, 0.35, 0.20, 0.10, 0.05])
interest_rates = np.round(np.random.uniform(9.5, 24.0, num_borrowers), 2)
existing_monthly_debt = np.round(np.random.uniform(0, 0.40, num_borrowers) * (annual_incomes / 12.0), -2)
active_credit_cards_and_loans = np.random.poisson(3, num_borrowers)
past_90_dpd_delinquencies = np.random.choice([0, 1, 2, 3], num_borrowers, p=[0.82, 0.11, 0.05, 0.02])
credit_card_utilization = np.round(np.random.beta(2, 5, num_borrowers) * 100, 1)

# estimating default risk: high foir, subprime cibil, and past 90+ dpd delinquencies drive defaults
monthly_income = annual_incomes / 12.0
monthly_rate = (interest_rates / 100.0) / 12.0
monthly_emi = loan_amounts * monthly_rate * ((1 + monthly_rate) ** loan_tenures) / (((1 + monthly_rate) ** loan_tenures) - 1)
debt_burden_ratio = (existing_monthly_debt + monthly_emi) / monthly_income

risk_logits = (
    -3.2
    + 2.8 * (debt_burden_ratio > 0.50)
    + 2.1 * (cibil_scores < 650)
    + 1.8 * (past_90_dpd_delinquencies > 0)
    + 1.2 * (credit_card_utilization > 75)
    - 0.8 * (cibil_scores >= 750)
)
default_probabilities = 1.0 / (1.0 + np.exp(-risk_logits))
default_outcomes = np.random.binomial(1, default_probabilities)

# introducing messy real-world data issues: city typos and dirty currency strings
messy_city_entries = [random.choice(city_spelling_mistakes[random.choice(cities)]) for _ in range(num_borrowers)]
messy_income_strings = []
for inc in annual_incomes:
    rand_chance = random.random()
    if rand_chance < 0.15: messy_income_strings.append(f"Rs. {int(inc):,}/-")
    elif rand_chance < 0.25: messy_income_strings.append(f"{int(inc)} INR")
    elif rand_chance < 0.35: messy_income_strings.append(f" {int(inc)} ")
    else: messy_income_strings.append(str(int(inc)))

# assembling into raw dataframe
df = pd.DataFrame({
    "customer_id": customer_ids, "loan_id": loan_ids, "application_date": application_dates,
    "age": borrower_ages, "applicant_city": messy_city_entries, "employment_type": np.random.choice(employment_sectors, num_borrowers),
    "stated_annual_income": messy_income_strings, "cibil_score": cibil_scores, "active_credit_lines": active_credit_cards_and_loans,
    "historical_dpd_90": past_90_dpd_delinquencies, "credit_card_utilization_pct": credit_card_utilization, "existing_monthly_emi": existing_monthly_debt,
    "applied_loan_amount": loan_amounts, "loan_tenure_months": loan_tenures, "interest_rate_pct": interest_rates,
    "loan_purpose": np.random.choice(loan_reasons, num_borrowers), "default_status": default_outcomes
})

# adding missing bureau scores, accidental age typos, and duplicate application attempts
df.loc[df.sample(frac=0.04, random_state=42).index, "cibil_score"] = np.nan
df.loc[df.sample(frac=0.02, random_state=42).index, "credit_card_utilization_pct"] = np.nan
df.loc[df.sample(frac=0.015, random_state=42).index, "employment_type"] = np.nan
df.loc[df.sample(n=60, random_state=42).index, "age"] = [random.choice([-10, 0, 140, 192, 5]) for _ in range(60)]
df = pd.concat([df, df.sample(n=250, random_state=42)], ignore_index=True)

# saving raw loan dataset for the data analyst cleansing pipeline
df.to_csv(out_file, index=False)
print(f"Portfolio simulation complete: created {len(df):,} loan records across 12 cities in '{out_file.name}'")
