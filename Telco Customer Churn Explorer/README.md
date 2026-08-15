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
- R (dplyr, ggplot2, readr) for reproducing the analysis in code
- Logistic regression and random forest models (base R stats, randomForest)
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
`app.R` exposes the same insights interactively across two tabs:
- **Overview** — churn rate by contract, tenure band, and payment method, filterable live.
- **Model insights** — test-set accuracy, precision, recall, F1, and AUC (for the churn = "Yes" class) for both a logistic regression and a random forest model, plus key logistic-regression odds ratios and random forest variable importance.

## Key Insights

- Month-to-month contracts show the highest churn compared to one- and two-year contracts.
- Electronic check as a payment method correlates with elevated churn.
- Churn is highest among lower-tenure customers and declines as tenure increases.
- Customers without add-on services (e.g. tech support, online security) churn at a higher rate.
- On a held-out test set (~26% churn base rate), the logistic regression scores ~80% accuracy but only ~51% recall on churners (AUC ~0.83); the random forest scores ~77% accuracy with ~53% recall (AUC ~0.81). Accuracy alone would hide this: a model that always predicts "no churn" already scores ~74% accuracy without being useful, which is why the app surfaces precision/recall/F1/AUC rather than accuracy alone.

## How to Use

**Excel:**
1. Open `telco_customer_churn.xlsx`.
2. Review the pivot tables and charts summarizing churn drivers.

**R (replicating the Excel work):**

```r
install.packages(c("readr", "dplyr", "stringr", "ggplot2", "scales", "randomForest"))
setwd("Telco Customer Churn Explorer")
source("telco_customer_churn.R")
```

**Shiny app:**

```r
install.packages(c("shiny", "shinythemes", "dplyr", "ggplot2", "readr", "stringr", "scales", "randomForest"))
setwd("Telco Customer Churn Explorer")
shiny::runApp("app.R")
```

`app.R` sources `telco_customer_churn.R` itself, so you don't need to run it separately first. The app lets you:
- See churn rates broken out by contract, tenure band, and payment method.
- Filter by contract type, tenure band, and payment method.
- Review model accuracy and the strongest churn drivers from the logistic regression and random forest.

## Future Improvements

- Address class imbalance in training (~26% churn) with class weighting or resampling to improve recall on churners.
- Add tenure-based cohort/retention curves.
- Let users adjust the classification threshold and see precision/recall and the confusion matrix update live.
- Deploy to shinyapps.io for a live demo link.

## Acknowledgements

Telco Customer Churn dataset used here for learning and portfolio purposes.
