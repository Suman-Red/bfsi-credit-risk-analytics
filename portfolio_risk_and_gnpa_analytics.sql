-- =============================================================================
-- PORTFOLIO RISK & GROSS NPA (GNPA) ANALYTICS
-- Database: MySQL Workbench (`bfsi_credit_risk`)
-- Structured as Business Questions Asked by Credit Risk Managers & Underwriters
-- =============================================================================

CREATE DATABASE bfsi_credit_risk;
USE bfsi_credit_risk;

-- =============================================================================
-- VERIFICATION: Are all 25,000 loan records loaded into each table?
-- =============================================================================
SELECT 'dim_customers' AS table_name, COUNT(*) AS total_rows FROM dim_customers
UNION ALL
SELECT 'dim_bureau_profile' AS table_name, COUNT(*) AS total_rows FROM dim_bureau_profile
UNION ALL
SELECT 'fact_loans' AS table_name, COUNT(*) AS total_rows FROM fact_loans;


-- =============================================================================
-- BUSINESS QUESTIONS & ANALYTICAL SQL QUERIES
-- =============================================================================

-- -----------------------------------------------------------------------------
-- QUESTION 1: Which loan purposes (e.g. medical, wedding, education) are driving
--             our highest default volume and Gross NPA % across the portfolio?
-- -----------------------------------------------------------------------------
SELECT 
    f.loan_purpose,
    COUNT(f.loan_id) AS total_disbursed_loans,
    ROUND(SUM(f.sanctioned_loan_amount_inr) / 10000000.0, 2) AS total_portfolio_crores,
    ROUND(SUM(CASE WHEN f.is_default = 1 THEN f.sanctioned_loan_amount_inr ELSE 0 END) / 10000000.0, 2) AS gross_npa_crores,
    -- Gross NPA % = (Total Default Value / Total Disbursed Value) * 100
    ROUND((SUM(CASE WHEN f.is_default = 1 THEN f.sanctioned_loan_amount_inr ELSE 0.0 END) * 100.0) / 
           SUM(f.sanctioned_loan_amount_inr), 2) AS gnpa_ratio_pct,
    ROUND(AVG(f.is_default) * 100.0, 2) AS default_count_pct
FROM fact_loans f
GROUP BY f.loan_purpose
ORDER BY gnpa_ratio_pct DESC;


-- -----------------------------------------------------------------------------
-- QUESTION 2: How dangerous is it when a borrower has both a low CIBIL score (<650)
--             and an overleveraged monthly debt burden (FOIR > 50%)?
-- -----------------------------------------------------------------------------
SELECT 
    b.cibil_tier,
    f.foir_bucket,
    COUNT(f.loan_id) AS total_borrowers,
    ROUND(SUM(f.sanctioned_loan_amount_inr) / 10000000.0, 2) AS total_book_crores,
    ROUND(AVG(f.is_default) * 100.0, 2) AS default_rate_pct
FROM fact_loans f
JOIN dim_bureau_profile b ON f.customer_id = b.customer_id
GROUP BY b.cibil_tier, f.foir_bucket
ORDER BY 
    CASE b.cibil_tier
        WHEN 'Deep Subprime (<550)' THEN 1
        WHEN 'Subprime (550-649)' THEN 2
        WHEN 'Near Prime (650-749)' THEN 3
        WHEN 'Prime (750+)' THEN 4
        ELSE 5
    END,
    f.foir_bucket;


-- -----------------------------------------------------------------------------
-- QUESTION 3: In which cities and employment sectors (salaried vs gig vs self-employed)
--             are our bad loans most heavily concentrated?
-- -----------------------------------------------------------------------------
SELECT 
    c.city_tier,
    c.employment_type,
    COUNT(f.loan_id) AS total_borrowers,
    ROUND(AVG(c.annual_income_inr), 0) AS avg_annual_income_inr,
    ROUND(AVG(b.credit_card_utilization_pct), 1) AS avg_card_utilization_pct,
    ROUND(AVG(f.is_default) * 100.0, 2) AS default_rate_pct
FROM fact_loans f
JOIN dim_customers c ON f.customer_id = c.customer_id
JOIN dim_bureau_profile b ON f.customer_id = b.customer_id
GROUP BY c.city_tier, c.employment_type
ORDER BY c.city_tier, default_rate_pct DESC;


-- -----------------------------------------------------------------------------
-- QUESTION 4: Which active borrowers fall into our "gray area" underwriting queue
--             and need manual review by a credit officer before disbursement?
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_underwriter_queue AS
SELECT 
    f.loan_id,
    c.customer_id,
    c.applicant_city,
    c.employment_type,
    c.annual_income_inr,
    b.cibil_score,
    b.cibil_tier,
    b.credit_card_utilization_pct,
    f.sanctioned_loan_amount_inr,
    ROUND(f.foir_dti_ratio * 100.0, 1) AS foir_pct,
    f.loan_purpose,
    CASE 
        WHEN b.cibil_score BETWEEN 650 AND 720 AND f.foir_dti_ratio > 0.45 
            THEN 'Borderline CIBIL + Overleveraged'
        WHEN b.credit_card_utilization_pct > 80.0 AND f.sanctioned_loan_amount_inr > 500000 
            THEN 'High Revolving Debt Exposure'
        WHEN c.employment_type IN ('Gig Economy Worker', 'MSME / Small Business') AND f.sanctioned_loan_amount_inr > 750000 
            THEN 'High-Value Unsecured Self-Employed'
        ELSE 'General Manual Review'
    END AS triage_flag
FROM fact_loans f
JOIN dim_customers c ON f.customer_id = c.customer_id
JOIN dim_bureau_profile b ON f.customer_id = b.customer_id
WHERE 
    f.is_default = 0
    AND (
        (b.cibil_score BETWEEN 650 AND 720 AND f.foir_dti_ratio > 0.45)
        OR (b.credit_card_utilization_pct > 80.0 AND f.sanctioned_loan_amount_inr > 500000)
        OR (c.employment_type IN ('Gig Economy Worker', 'MSME / Small Business') AND f.sanctioned_loan_amount_inr > 750000)
    );


-- -----------------------------------------------------------------------------
-- QUESTION 5: How has our loan disbursement volume and monthly default rate
--             trended over time across origination vintages?
-- -----------------------------------------------------------------------------
SELECT 
    SUBSTRING(CAST(f.application_date AS CHAR(10)), 1, 7) AS origination_month,
    COUNT(f.loan_id) AS total_loans_originated,
    ROUND(SUM(f.sanctioned_loan_amount_inr) / 100000.0, 2) AS total_disbursed_lakhs,
    ROUND(AVG(b.cibil_score), 0) AS avg_vintage_cibil,
    ROUND(AVG(f.is_default) * 100.0, 2) AS default_rate_pct
FROM fact_loans f
JOIN dim_bureau_profile b ON f.customer_id = b.customer_id
GROUP BY SUBSTRING(CAST(f.application_date AS CHAR(10)), 1, 7)
ORDER BY origination_month;


-- -----------------------------------------------------------------------------
-- QUESTION 6: Within Tier 1 vs Tier 2 cities, what are the top 3 highest-risk
--             borrower employment profiles (ranked using Window DENSE_RANK)?
-- -----------------------------------------------------------------------------
WITH RiskRankingCTE AS (
    SELECT 
        c.city_tier,
        c.employment_type,
        COUNT(f.loan_id) AS total_loans,
        ROUND(AVG(f.is_default) * 100.0, 2) AS default_rate_pct,
        DENSE_RANK() OVER (
            PARTITION BY c.city_tier 
            ORDER BY AVG(f.is_default) DESC
        ) AS risk_rank
    FROM fact_loans f
    JOIN dim_customers c ON f.customer_id = c.customer_id
    GROUP BY c.city_tier, c.employment_type
)
SELECT 
    city_tier,
    employment_type,
    total_loans,
    default_rate_pct,
    risk_rank
FROM RiskRankingCTE
WHERE risk_rank <= 3
ORDER BY city_tier, risk_rank;


-- -----------------------------------------------------------------------------
-- QUESTION 7: If we apply the IFRS 9 / Basel formula (ECL = PD * LGD * EAD),
--             what is our estimated loan loss provision across each loan category?
-- -----------------------------------------------------------------------------
SELECT 
    f.loan_purpose,
    ROUND(SUM(f.sanctioned_loan_amount_inr) / 10000000.0, 2) AS total_exposure_crores,
    ROUND(AVG(f.is_default), 4) AS empirical_pd,
    0.45 AS regulatory_lgd, -- 45% standard Loss Given Default for unsecured retail loans
    -- Expected Loss = Sum(EAD * PD * LGD)
    ROUND(SUM(f.sanctioned_loan_amount_inr * CASE WHEN f.is_default = 1 THEN 1.0 ELSE 0.15 END * 0.45) / 100000.0, 2) AS estimated_loss_provision_lakhs
FROM fact_loans f
GROUP BY f.loan_purpose
ORDER BY estimated_loss_provision_lakhs DESC;
