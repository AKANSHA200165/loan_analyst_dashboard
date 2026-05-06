# Power BI Dashboard Design Guide

## Dashboard Title

Banking Loan Risk Analysis Dashboard

## Dashboard Goal

Help stakeholders quickly understand loan approval patterns, rejection risk, and customer segments that may require closer review.

## Recommended Page Layout

Use a clean single-page executive dashboard layout.

```text
 ------------------------------------------------------------
| Banking Loan Risk Analysis Dashboard                        |
| Filters: Gender | Education | Property Area | Credit History |
 ------------------------------------------------------------
| Total Applicants | Approval Rate | Rejection Rate | Avg Income |
| Avg Loan Amount                                           |
 ------------------------------------------------------------
| Credit History Impact          | Loan Status by Education    |
| Clustered Column Chart         | Stacked Bar Chart            |
 ------------------------------------------------------------
| Loan Status by Property Area   | Gender-wise Loan Analysis    |
| Stacked Column Chart           | Donut or Clustered Bar Chart |
 ------------------------------------------------------------
| Risk Summary / Key Insights                                  |
 ------------------------------------------------------------
```

## KPI Cards

Place KPI cards across the top of the dashboard. Use large numbers with short labels.

### 1. Total Applicants

Best visual: Card

Suggested DAX:

```DAX
Total Applicants = COUNTROWS(loans)
```

### 2. Loan Approval Rate

Best visual: Card

Suggested DAX:

```DAX
Approved Loans =
CALCULATE(
    COUNTROWS(loans),
    loans[loan_status] = "Y"
)

Approval Rate =
DIVIDE([Approved Loans], [Total Applicants], 0)
```

Format as percentage.

### 3. Rejection Rate

Best visual: Card

Suggested DAX:

```DAX
Rejected Loans =
CALCULATE(
    COUNTROWS(loans),
    loans[loan_status] = "N"
)

Rejection Rate =
DIVIDE([Rejected Loans], [Total Applicants], 0)
```

Format as percentage.

### 4. Average Income

Best visual: Card

Suggested DAX:

```DAX
Average Income = AVERAGE(loans[applicant_income])
```

### 5. Average Loan Amount

Best visual: Card

Suggested DAX:

```DAX
Average Loan Amount = AVERAGE(loans[loan_amount])
```

## Main Visuals

### 1. Credit History Impact

Best visual: Clustered column chart

Fields:

- X-axis: `credit_history`
- Y-axis: count of applicants
- Legend: `loan_status`

Purpose:

Shows whether applicants with good credit history are more likely to be approved.

Professional insight to mention:

Applicants with positive credit history usually show stronger approval rates, making credit history one of the most important risk indicators.

### 2. Loan Status by Education

Best visual: 100% stacked bar chart

Fields:

- Y-axis: `education`
- X-axis: count of applicants
- Legend: `loan_status`

Purpose:

Compares approval and rejection percentages for graduate and non-graduate applicants.

Professional insight to mention:

Education may influence loan approval indirectly through income level, employment stability, and repayment capacity.

### 3. Loan Status by Property Area

Best visual: Stacked column chart

Fields:

- X-axis: `property_area`
- Y-axis: count of applicants
- Legend: `loan_status`

Purpose:

Shows how approvals and rejections vary across urban, semiurban, and rural areas.

Professional insight to mention:

Property area can help identify geographic approval patterns and possible regional risk differences.

### 4. Gender-wise Loan Analysis

Best visual: Clustered bar chart

Fields:

- Y-axis: `gender`
- X-axis: count of applicants
- Legend: `loan_status`

Alternative visual: Donut chart if showing only applicant share by gender.

Purpose:

Compares application volume and approval outcomes by gender.

Professional insight to mention:

Gender-wise analysis helps review customer distribution and identify whether approval outcomes are balanced across applicant groups.

### 5. Income and Loan Amount Relationship

Best visual: Scatter chart

Fields:

- X-axis: `applicant_income`
- Y-axis: `loan_amount`
- Legend: `loan_status`
- Size: optional count of applicants

Purpose:

Shows whether higher income applicants request larger loans and whether rejected loans cluster in high loan amount ranges.

## Interactive Filters

Place slicers at the top or left side of the dashboard.

Recommended slicers:

- Gender
- Education
- Property area
- Credit history
- Dependents
- Loan status

Slicer style:

- Use dropdown slicers for fields with many categories.
- Use button or tile slicers for fields with few categories.
- Keep slicers aligned and consistent.

## Professional Layout Tips

- Use a white or very light background.
- Use dark text for readability.
- Use one accent color for approved loans and one alert color for rejected loans.
- Keep KPI cards in the first row.
- Use consistent chart titles such as "Loan Status by Education".
- Avoid cluttered legends and unnecessary gridlines.
- Format currency fields with separators.
- Format approval and rejection rates as percentages.

## Suggested Color Palette

- Approved loans: green
- Rejected loans: red or orange
- Neutral charts: blue or gray
- Background: white or light gray
- Text: dark gray

## Dashboard Story Flow

1. Start with overall KPIs.
2. Show approval and rejection patterns.
3. Explain credit history impact.
4. Compare customer segments by education, property area, and gender.
5. Use filters to explore specific risk groups.

## Final Dashboard Checklist

- KPI cards are visible at the top.
- All charts have clear titles.
- Slicers work correctly.
- Numbers are formatted properly.
- Charts use consistent approved/rejected colors.
- Dashboard fits on one page without scrolling.
- Screenshots are exported to the `screenshots` folder for portfolio use.

