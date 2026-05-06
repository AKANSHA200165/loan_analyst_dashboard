import pandas as pd


# ------------------------------------------------------------
# Banking Loan Dataset Cleaning Script
# ------------------------------------------------------------
# Before running:
# 1. Place your raw CSV file inside the dataset/raw folder.
# 2. Update INPUT_FILE if your file has a different name.
# 3. Run this script from the project root folder:
#    python scripts/clean_loan_dataset.py
# ------------------------------------------------------------


INPUT_FILE = "dataset/raw/banking_loan_data.csv"
OUTPUT_FILE = "dataset/cleaned/banking_loan_data_cleaned.csv"


def standardize_column_names(df):
    """Make column names easier to work with in Python, SQL, and Power BI."""
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
        .str.replace("/", "_", regex=False)
    )
    return df


def clean_categorical_columns(df):
    """Clean text columns so categories are consistent."""
    categorical_columns = df.select_dtypes(include=["object"]).columns

    for column in categorical_columns:
        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        # Replace common missing text values with pandas missing value.
        df[column] = df[column].replace(
            ["nan", "none", "null", "n/a", "na", ""],
            pd.NA
        )

    return df


def convert_common_data_types(df):
    """Convert common loan dataset columns to useful data types when present."""
    numeric_columns = [
        "age",
        "income",
        "annual_income",
        "loan_amount",
        "credit_score",
        "interest_rate",
        "loan_term",
        "debt_to_income_ratio",
    ]

    date_columns = [
        "application_date",
        "loan_date",
        "approval_date",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    for column in date_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    return df


def main():
    # Load the raw dataset.
    df = pd.read_csv(INPUT_FILE)

    print("Original dataset shape:", df.shape)

    # Standardize column names.
    df = standardize_column_names(df)

    # Clean categorical/text columns.
    df = clean_categorical_columns(df)

    # Convert numeric and date columns where possible.
    df = convert_common_data_types(df)

    # Remove duplicate records.
    duplicate_count = df.duplicated().sum()
    df = df.drop_duplicates()
    print("Duplicate records removed:", duplicate_count)

    # Remove rows with null values.
    # Beginner note: this is simple and strict. Later, you can replace missing
    # values with averages, medians, or modes depending on the business case.
    null_rows_count = df.isnull().any(axis=1).sum()
    df = df.dropna()
    print("Rows with null values removed:", null_rows_count)

    print("Cleaned dataset shape:", df.shape)

    # Show summary statistics for numeric columns.
    print("\nSummary statistics:")
    print(df.describe())

    # Show a quick summary of categorical columns.
    print("\nCategorical column summary:")
    categorical_columns = df.select_dtypes(include=["object", "category"]).columns
    for column in categorical_columns:
        print(f"\n{column}:")
        print(df[column].value_counts().head(10))

    # Export the cleaned dataset as a CSV file.
    df.to_csv(OUTPUT_FILE, index=False)
    print("\nCleaned dataset exported to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()

