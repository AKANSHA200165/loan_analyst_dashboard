# Dataset

Place all project data files here.

## Suggested Organization

- `raw/` - original dataset files downloaded from the source
- `cleaned/` - cleaned or transformed files, if created later

## Example Dataset Fields

A banking loan risk dataset may include:

- Customer ID
- Age
- Income
- Employment status
- Credit score
- Loan amount
- Loan purpose
- Interest rate
- Loan term
- Approval status
- Default status

## Notes

Keep raw data unchanged. Any cleaning steps should be documented in the main README or reports folder.

## Cleaning Script

Use the pandas cleaning script at `scripts/clean_loan_dataset.py`.

Default input:

```text
dataset/raw/banking_loan_data.csv
```

Default output:

```text
dataset/cleaned/banking_loan_data_cleaned.csv
```

## Included Sample Files

- `raw/banking_loan_data.csv` - sample banking loan dataset
- `cleaned/banking_loan_data_cleaned.csv` - cleaned sample dataset
- `cleaned/banking_loan_data_with_risk_score.csv` - cleaned dataset with beginner-friendly risk categories
