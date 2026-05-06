import pandas as pd


# ------------------------------------------------------------
# Beginner-Friendly Loan Risk Scoring Logic
# ------------------------------------------------------------
# This script creates a simple risk score using:
# - income
# - credit history
# - loan amount
# - dependents
#
# Output:
# - risk_score
# - risk_category: Low Risk, Medium Risk, or High Risk
# ------------------------------------------------------------


INPUT_FILE = "dataset/cleaned/banking_loan_data_cleaned.csv"
OUTPUT_FILE = "dataset/cleaned/banking_loan_data_with_risk_score.csv"


def calculate_risk_score(row):
    """Calculate risk score for one applicant."""
    score = 0

    # 1. Income risk
    # Lower income means lower repayment capacity.
    if row["applicant_income"] < 3000:
        score += 3
    elif row["applicant_income"] < 6000:
        score += 2
    else:
        score += 1

    # 2. Credit history risk
    # Credit history of 0 means no/poor credit history, which is risky.
    if row["credit_history"] == 0:
        score += 4
    else:
        score += 1

    # 3. Loan amount risk
    # Higher loan amounts can increase repayment pressure.
    if row["loan_amount"] > 250:
        score += 3
    elif row["loan_amount"] > 120:
        score += 2
    else:
        score += 1

    # 4. Dependents risk
    # More dependents may mean higher household expenses.
    dependents = str(row["dependents"]).replace("+", "")

    if dependents.isdigit():
        dependents = int(dependents)
    else:
        dependents = 0

    if dependents >= 3:
        score += 3
    elif dependents >= 1:
        score += 2
    else:
        score += 1

    return score


def classify_risk(score):
    """Convert numeric risk score into a business-friendly risk category."""
    if score <= 5:
        return "Low Risk"
    elif score <= 9:
        return "Medium Risk"
    else:
        return "High Risk"


def main():
    df = pd.read_csv(INPUT_FILE)

    required_columns = [
        "applicant_income",
        "credit_history",
        "loan_amount",
        "dependents",
    ]

    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Create risk score and risk category columns.
    df["risk_score"] = df.apply(calculate_risk_score, axis=1)
    df["risk_category"] = df["risk_score"].apply(classify_risk)

    print("Risk category distribution:")
    print(df["risk_category"].value_counts())

    print("\nAverage values by risk category:")
    print(
        df.groupby("risk_category")[
            ["applicant_income", "loan_amount", "credit_history"]
        ].mean().round(2)
    )

    df.to_csv(OUTPUT_FILE, index=False)
    print("\nDataset with risk score exported to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()

