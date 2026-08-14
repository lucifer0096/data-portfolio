# Telco Customer Churn Explorer

End-to-end customer churn analysis using the Telco Customer Churn dataset: starting from a raw CSV, through an Excel workbook with pivot-table analysis, then R replication, and finally an interactive Shiny app.

## Overview

The goal is to understand which customers are more likely to churn and how churn varies across contracts, services, and demographics. The workflow mirrors a typical analyst process: explore in Excel first, translate the same logic into reproducible R code, then expose the insights through a Shiny dashboard.

## Dataset

- **Source:** [Telco Customer Churn dataset (Kaggle)](https://www.kaggle.com/code/farazrahman/telco-customer-churn-logisticregression/input)
- **Location in repo:** `Data/telco_customer_churn.csv`

## Files in This Folder

| File | Purpose |
|---|---|
| `Data/telco_customer_churn.csv` | Raw dataset |
| `telco_customer_churn.xlsx` | Excel workbook with pivot tables and charts |
| `telco_customer_churn.R` | R script for data loading and analysis |
| `app.R` | R Shiny app for interactive exploration |

## Tools & Skills

- Excel pivot tables and charts for initial churn exploration
- R (tidyverse) for reproducing the analysis in code
- R Shiny for an interactive, filterable dashboard

## Business Questions

- Which contract types, payment methods, and services are associated with higher churn?
- How does churn vary by tenure and customer demographics?
- Which customer segments should be prioritized for retention efforts?

## Approach

### 1. Excel analysis
Explored pivot tables showing churn by contract type, payment method, tenure group, and subscribed services, then built charts summarizing the main patterns.

### 2. R analysis (replicating the Excel work)
`telco_customer_churn.R` reads the raw CSV, cleans and prepares the data (type conversions, missing values, simple feature engineering), and recreates the key Excel pivot views using grouped summaries and plots.

### 3. Shiny app
`app.R` exposes the same insights interactively, letting users filter by tenure, contract type, payment method, and internet service, with churn KPIs and charts updating live.

## Key Insights

- Month-to-month contracts show the highest churn compared to one- and two-year contracts.
- Electronic check as a payment method correlates with elevated churn.
- Churn is highest among lower-tenure customers and declines as tenure increases.
- Customers without add-on services (e.g. tech support, online security) churn at a higher rate.

## How to Use

**Excel:**
1. Open `telco_customer_churn.xlsx`.
2. Review the pivot tables and charts summarizing churn drivers.

**R (replicating the Excel work):**

```r
install.packages(c("tidyverse", "shiny", "shinydashboard", "DT", "plotly"))
setwd("Telco Customer Churn Explorer")
source("telco_customer_churn.R")
```

**Shiny app:**

```r
source("telco_customer_churn.R")
shiny::runApp("app.R")
```

The app lets you:
- See headline churn KPIs.
- Filter by tenure, contract type, payment method, internet service, and other attributes.
- View plots and tables that update based on the selected segment.

## Future Improvements

- Add a simple predictive churn model (logistic regression) and surface its output in the Shiny app.
- Add cohort-based retention curves by signup month.

## Acknowledgements

Telco Customer Churn dataset used here for learning and portfolio purposes.
