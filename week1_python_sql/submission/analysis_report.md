# Analysis Report

## Overview

This report summarizes the key findings from the cleaned customer dataset. The analysis includes data cleaning, SQL insights, and visual trends.

---

## Data Cleaning Summary

- Removed rows with missing or invalid:
  - Emails
  - Age (e.g. over 100)
  - Country (e.g. "Future Country")
  - Amounts (e.g. negative numbers)
  - Dates in the future
- Cleaned file saved as `cleaned_data.csv`

---

## SQL Insights

- **Most popular product categories**:
  - Electronics
  - Clothing
  - Home & Garden

- **Average spending per country**:
- UK: 300.0
- USA: 204.3
- Spain: 151.67
- Canada: 148.71
- Australia: 95.83

- **Highest spending customer**: David Kim (599.99)
- **Number of active customers**: 29

## Dashboard Observations

- Sales increase near end of the year (Nov–Dec)
- Most customers are aged 25–35
- Majority of purchases come from the USA

## Recommendations

- Focus ads on 25–35 age group
- Promote top-selling categories
- Monitor and clean out invalid future data entries
