# Telco Customer Churn Explorer (Excel & R)

End‑to‑end customer churn analysis using the Telco Customer Churn dataset, starting from a raw CSV, then an Excel workbook with pivot‑table analysis and charts, followed by R replication and an interactive Shiny app.

## Project overview

The goal is to understand which customers are more likely to churn and how churn varies across contracts, services, and demographics.  
The workflow mirrors a typical analyst process: first explore in Excel, then translate the same logic into reproducible R code and finally expose the insights through a Shiny dashboard.

## Files in this folder

In the project root (in this order):

1. `telco_customer_churn.csv` – Raw dataset.  
2. `telco_customer_churn.xlsx` – Excel workbook with pivot tables and charts.  
3. `telco_customer_churn.R` – R script for data loading and analysis.  
4. `app.R` – R Shiny app for interactive exploration.

## Setup and installation (R)

1. Install R and (optionally) RStudio.  
2. Install required R packages (adjust if your script uses fewer/more):

install.packages(c(
"tidyverse",
"shiny",
"shinydashboard", # or bs4Dash if you used it
"DT",
"plotly"
))


3. Open this folder in RStudio or set the working directory to this folder in R.

## Excel analysis

1. Open `telco_customer_churn.xlsx` in Excel.  
2. Explore the pivot tables showing churn by contract type, payment method, tenure groups, and subscribed services.  
3. Review the charts/dashboard that summarize the main churn insights.

## R analysis (replicating the Excel work)

1. In RStudio (with the working directory set to this folder), run:

source("telco_customer_churn.R")


2. This script:

- Reads `telco_customer_churn.csv`.  
- Cleans and prepares the data (type conversions, missing values, simple feature engineering).  
- Recreates the key Excel pivot views using grouped summaries and plots.

## Shiny app

1. Make sure `telco_customer_churn.R` reads the CSV using a relative path, for example:

telco_raw <- readr::read_csv("telco_customer_churn.csv")


2. From the R console:

source("telco_customer_churn.R")
shiny::runApp("app.R")


3. The Shiny app lets you:

- See headline churn KPIs.  
- Filter customers by tenure, contract type, payment method, internet service, and other attributes.  
- View plots and tables that update based on the selected segment.

## Acknowledgements

- Telco Customer Churn dataset used here for learning and portfolio purposes.
https://www.kaggle.com/code/farazrahman/telco-customer-churn-logisticregression/input
