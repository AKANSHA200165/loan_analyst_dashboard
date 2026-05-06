import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# ------------------------------------------------------------
# Banking Loan Dataset Exploratory Data Analysis
# ------------------------------------------------------------
# Before running:
# 1. Clean your dataset first using scripts/clean_loan_dataset.py.
# 2. Confirm the input file path below matches your cleaned CSV file.
# 3. Run this script from the project root folder:
#    python scripts/eda_loan_dataset.py
# ------------------------------------------------------------


INPUT_FILE = "dataset/cleaned/banking_loan_data_cleaned.csv"
OUTPUT_FOLDER = "screenshots"


sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (9, 5)


def find_column(df, possible_names):
    """Find the first matching column from a list of common column names."""
    for column in possible_names:
        if column in df.columns:
            return column
    return None


def save_chart(file_name):
    """Save the active matplotlib chart to the screenshots folder."""
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    output_path = os.path.join(OUTPUT_FOLDER, file_name)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.show()
    print(f"Chart saved to: {output_path}")


def print_missing_column_message(analysis_name, required_columns):
    print(f"\nSkipped {analysis_name}.")
    print("Missing required column. Check if your dataset has one of these names:")
    print(", ".join(required_columns))


def loan_approval_distribution(df):
    print("\n1. Loan Approval Distribution")

    approval_column = find_column(
        df,
        ["loan_status", "approval_status", "loan_approval", "approved"],
    )

    if approval_column is None:
        print_missing_column_message(
            "loan approval distribution",
            ["loan_status", "approval_status", "loan_approval", "approved"],
        )
        return

    approval_counts = df[approval_column].value_counts()
    print(approval_counts)

    sns.countplot(data=df, x=approval_column, order=approval_counts.index)
    plt.title("Loan Approval Distribution")
    plt.xlabel("Loan Approval Status")
    plt.ylabel("Number of Applications")
    save_chart("loan_approval_distribution.png")

    print("Insight:")
    print(
        "This chart shows whether the dataset has more approved or rejected loans. "
        "A very large difference between categories may mean the approval process is strict, "
        "or the dataset is imbalanced."
    )


def income_distribution(df):
    print("\n2. Income Distribution")

    income_column = find_column(
        df,
        ["income", "annual_income", "applicant_income", "customer_income"],
    )

    if income_column is None:
        print_missing_column_message(
            "income distribution",
            ["income", "annual_income", "applicant_income", "customer_income"],
        )
        return

    print(df[income_column].describe())

    sns.histplot(data=df, x=income_column, kde=True, bins=30)
    plt.title("Income Distribution")
    plt.xlabel("Income")
    plt.ylabel("Number of Applicants")
    save_chart("income_distribution.png")

    print("Insight:")
    print(
        "This chart shows how applicant income is spread across the dataset. "
        "If the distribution is right-skewed, most applicants have lower or middle incomes, "
        "while a smaller group has very high income."
    )


def credit_history_analysis(df):
    print("\n3. Credit History Analysis")

    credit_history_column = find_column(
        df,
        ["credit_history", "credit_score_band", "credit_history_status"],
    )

    approval_column = find_column(
        df,
        ["loan_status", "approval_status", "loan_approval", "approved"],
    )

    if credit_history_column is None:
        print_missing_column_message(
            "credit history analysis",
            ["credit_history", "credit_score_band", "credit_history_status"],
        )
        return

    print(df[credit_history_column].value_counts())

    if approval_column:
        sns.countplot(data=df, x=credit_history_column, hue=approval_column)
        plt.title("Credit History vs Loan Approval")
        plt.xlabel("Credit History")
        plt.ylabel("Number of Applications")
        plt.legend(title="Loan Approval")
    else:
        sns.countplot(data=df, x=credit_history_column)
        plt.title("Credit History Distribution")
        plt.xlabel("Credit History")
        plt.ylabel("Number of Applicants")

    save_chart("credit_history_analysis.png")

    print("Insight:")
    print(
        "Credit history is often one of the strongest indicators of loan approval. "
        "Applicants with positive credit history are usually expected to have higher approval rates."
    )


def loan_amount_trends(df):
    print("\n4. Loan Amount Trends")

    loan_amount_column = find_column(
        df,
        ["loan_amount", "loanamount", "requested_loan_amount"],
    )

    loan_term_column = find_column(
        df,
        ["loan_term", "loan_amount_term", "term"],
    )

    if loan_amount_column is None:
        print_missing_column_message(
            "loan amount trends",
            ["loan_amount", "loanamount", "requested_loan_amount"],
        )
        return

    print(df[loan_amount_column].describe())

    if loan_term_column:
        trend_data = (
            df.groupby(loan_term_column)[loan_amount_column]
            .mean()
            .reset_index()
            .sort_values(loan_term_column)
        )

        sns.lineplot(data=trend_data, x=loan_term_column, y=loan_amount_column, marker="o")
        plt.title("Average Loan Amount by Loan Term")
        plt.xlabel("Loan Term")
        plt.ylabel("Average Loan Amount")
        save_chart("loan_amount_trends.png")
    else:
        sns.boxplot(data=df, y=loan_amount_column)
        plt.title("Loan Amount Distribution")
        plt.ylabel("Loan Amount")
        save_chart("loan_amount_distribution.png")

    print("Insight:")
    print(
        "This analysis shows the typical loan size and whether loan amounts change by term. "
        "Higher loan amounts may carry more repayment risk, especially when combined with low income."
    )


def education_vs_loan_approval(df):
    print("\n5. Education vs Loan Approval")

    education_column = find_column(df, ["education", "education_level", "qualification"])
    approval_column = find_column(
        df,
        ["loan_status", "approval_status", "loan_approval", "approved"],
    )

    if education_column is None or approval_column is None:
        print("\nSkipped education vs loan approval.")
        print("Required columns include an education column and an approval/status column.")
        return

    education_approval = pd.crosstab(df[education_column], df[approval_column], normalize="index") * 100
    print(education_approval.round(2))

    education_approval.plot(kind="bar", stacked=True)
    plt.title("Education vs Loan Approval")
    plt.xlabel("Education")
    plt.ylabel("Percentage of Applicants")
    plt.legend(title="Loan Approval")
    save_chart("education_vs_loan_approval.png")

    print("Insight:")
    print(
        "This comparison shows whether approval rates differ by education level. "
        "If one education group has a much higher approval share, it may be linked to income, employment, "
        "or credit history differences."
    )


def correlation_heatmap(df):
    print("\n6. Correlation Heatmap")

    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.shape[1] < 2:
        print("\nSkipped correlation heatmap.")
        print("At least two numeric columns are needed for correlation analysis.")
        return

    correlation_matrix = numeric_df.corr()
    print(correlation_matrix.round(2))

    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
    plt.title("Correlation Heatmap")
    save_chart("correlation_heatmap.png")

    print("Insight:")
    print(
        "The heatmap shows relationships between numeric variables. "
        "Values close to 1 mean a strong positive relationship, values close to -1 mean a strong negative relationship, "
        "and values near 0 mean little or no linear relationship."
    )


def main():
    df = pd.read_csv(INPUT_FILE)

    print("Dataset loaded successfully.")
    print("Rows and columns:", df.shape)
    print("\nColumns available:")
    print(list(df.columns))

    loan_approval_distribution(df)
    income_distribution(df)
    credit_history_analysis(df)
    loan_amount_trends(df)
    education_vs_loan_approval(df)
    correlation_heatmap(df)

    print("\nEDA completed.")


if __name__ == "__main__":
    main()

