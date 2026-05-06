-- Banking Loan Risk Analysis
-- Beginner-friendly SQL queries with explanations

-- Assumed table name: loans
-- Common columns used:
-- applicant_id, gender, dependents, education, applicant_income,
-- loan_amount, credit_history, property_area, loan_status
--
-- Note:
-- Many beginner loan datasets use loan_status values like 'Y' and 'N'.
-- In these queries:
-- 'Y' means approved
-- 'N' means rejected


-- Preview the dataset.
-- This helps you quickly check column names and sample records.
SELECT *
FROM loans
LIMIT 10;


-- 1. Total applicants
-- Counts how many loan applications exist in the dataset.
SELECT
    COUNT(*) AS total_applicants
FROM loans;


-- 2. Approved vs rejected loans
-- Shows the number of approved and rejected loan applications.
SELECT
    loan_status,
    COUNT(*) AS total_applications
FROM loans
GROUP BY loan_status
ORDER BY total_applications DESC;


-- 2a. Approved vs rejected loans with percentages
-- Adds approval/rejection percentage for easier dashboard reporting.
SELECT
    loan_status,
    COUNT(*) AS total_applications,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM loans), 2) AS percentage_of_total
FROM loans
GROUP BY loan_status
ORDER BY total_applications DESC;


-- 3. Average applicant income
-- Calculates the average income of all applicants.
SELECT
    ROUND(AVG(applicant_income), 2) AS average_applicant_income
FROM loans;


-- 3a. Average applicant income by approval status
-- Helps compare whether approved applicants have higher average income.
SELECT
    loan_status,
    ROUND(AVG(applicant_income), 2) AS average_applicant_income
FROM loans
GROUP BY loan_status
ORDER BY average_applicant_income DESC;


-- 4. Applicants with high loan amounts
-- Finds applicants whose requested loan amount is above the dataset average.
SELECT
    applicant_id,
    applicant_income,
    loan_amount,
    loan_status
FROM loans
WHERE loan_amount > (
    SELECT AVG(loan_amount)
    FROM loans
)
ORDER BY loan_amount DESC;


-- 4a. Count of high loan amount applicants
-- Useful KPI showing how many applications are above the average loan amount.
SELECT
    COUNT(*) AS high_loan_amount_applicants
FROM loans
WHERE loan_amount > (
    SELECT AVG(loan_amount)
    FROM loans
);


-- 5. Loan approval by education
-- Shows how many graduate and non-graduate applicants were approved or rejected.
SELECT
    education,
    loan_status,
    COUNT(*) AS total_applications
FROM loans
GROUP BY education, loan_status
ORDER BY education, loan_status;


-- 5a. Loan approval rate by education
-- Calculates approval rate for each education group.
SELECT
    education,
    COUNT(*) AS total_applications,
    SUM(CASE WHEN loan_status = 'Y' THEN 1 ELSE 0 END) AS approved_loans,
    ROUND(
        100.0 * SUM(CASE WHEN loan_status = 'Y' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS approval_rate_percent
FROM loans
GROUP BY education
ORDER BY approval_rate_percent DESC;


-- 6. Credit history impact on loan approval
-- Compares approval rates for applicants with and without credit history.
SELECT
    credit_history,
    COUNT(*) AS total_applications,
    SUM(CASE WHEN loan_status = 'Y' THEN 1 ELSE 0 END) AS approved_loans,
    SUM(CASE WHEN loan_status = 'N' THEN 1 ELSE 0 END) AS rejected_loans,
    ROUND(
        100.0 * SUM(CASE WHEN loan_status = 'Y' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS approval_rate_percent
FROM loans
GROUP BY credit_history
ORDER BY approval_rate_percent DESC;


-- 7. Top risky customer categories
-- Risky categories are groups with high rejection rates.
-- This query groups customers by education, credit history, and property area.
SELECT
    education,
    credit_history,
    property_area,
    COUNT(*) AS total_applications,
    SUM(CASE WHEN loan_status = 'N' THEN 1 ELSE 0 END) AS rejected_loans,
    ROUND(
        100.0 * SUM(CASE WHEN loan_status = 'N' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS rejection_rate_percent
FROM loans
GROUP BY education, credit_history, property_area
HAVING COUNT(*) >= 5
ORDER BY rejection_rate_percent DESC, total_applications DESC
LIMIT 10;


-- 8. Gender-wise loan analysis
-- Shows total applications, approvals, rejections, and approval rate by gender.
SELECT
    gender,
    COUNT(*) AS total_applications,
    SUM(CASE WHEN loan_status = 'Y' THEN 1 ELSE 0 END) AS approved_loans,
    SUM(CASE WHEN loan_status = 'N' THEN 1 ELSE 0 END) AS rejected_loans,
    ROUND(
        100.0 * SUM(CASE WHEN loan_status = 'Y' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS approval_rate_percent
FROM loans
GROUP BY gender
ORDER BY total_applications DESC;


-- 9. Property area analysis
-- Compares approval rates across urban, semiurban, and rural property areas.
SELECT
    property_area,
    COUNT(*) AS total_applications,
    SUM(CASE WHEN loan_status = 'Y' THEN 1 ELSE 0 END) AS approved_loans,
    SUM(CASE WHEN loan_status = 'N' THEN 1 ELSE 0 END) AS rejected_loans,
    ROUND(
        100.0 * SUM(CASE WHEN loan_status = 'Y' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS approval_rate_percent
FROM loans
GROUP BY property_area
ORDER BY approval_rate_percent DESC;


-- 10. Dependents vs approval rate
-- Shows whether applicants with more dependents have different approval rates.
SELECT
    dependents,
    COUNT(*) AS total_applications,
    SUM(CASE WHEN loan_status = 'Y' THEN 1 ELSE 0 END) AS approved_loans,
    SUM(CASE WHEN loan_status = 'N' THEN 1 ELSE 0 END) AS rejected_loans,
    ROUND(
        100.0 * SUM(CASE WHEN loan_status = 'Y' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS approval_rate_percent
FROM loans
GROUP BY dependents
ORDER BY dependents;

