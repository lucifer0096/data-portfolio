# Kevin Cookie Company Sales Analysis

Interactive Tableau dashboard analyzing ~200 orders from 50 customers across the United States, Canada, United Kingdom, and Germany (2024–2025), built to support market-expansion and account-retention decisions.

## Business Context

**Stakeholder:** Sales Director seeking data-driven input on:
- Market expansion prioritization
- Top-customer retention strategy
- Rush-shipment profitability
- Seasonal demand patterns

**Data source:** [Kevin Cookie Company dataset](https://onedrive.live.com/view.aspx?resid=B09F9559F6A16B6C%21103060&authkey=%21AMDmrXy5mgOxF3g)

| Table | Records | Fields |
|---|---|---|
| Customers | 50 | Customer ID, Name, Country |
| Orders | 200 | Order ID, Customer ID, Order Date, Cookies Shipped, Revenue, Rush Shipment |

## Tools & Skills

- Tableau dashboarding (extracts, cross-filters, geo maps)
- Data prep: 1:M relationship join, country standardization (`REPLACE("U.S.", "United States")`), date truncation for heatmaps
- Aggregation: `SUM(Revenue)`, `SUM(Cookies Shipped)`

## Business Questions

1. Which countries generate the highest revenue per cookie?
2. Who are the top 10 customers by revenue?
3. What are the daily and weekly sales patterns?
4. Do rush shipments correlate with higher order value?

## Dashboard Components

| View | Purpose | Key Features |
|---|---|---|
| Daily Cookies | Volume trends | Date heatmap, country filter |
| Daily Revenue | Revenue patterns | Date heatmap, customer filter |
| Country Map | Geo-performance | Revenue color encoding, click-to-filter |
| Top Customers | Account analysis | Descending revenue sort, country filter |

All views are cross-filtered by country and customer.

## Key Insights

- The United States dominates total revenue after country-name standardization.
- The top 5 customers drive a disproportionate share of total revenue.
- Rush shipments correlate with higher average order value.
- Sales show clear daily/weekly seasonality.

## Business Recommendations

1. Prioritize the top 3 countries by revenue-per-cookie for market focus.
2. Build a VIP retention program around the top 10 revenue accounts.
3. Review rush-shipment pricing to capture the profitability premium.
4. Plan inventory and staffing around identified seasonal peaks.

## How to Use

**Open locally:**
1. Keep `Kevin_Cookie_Company_Data.xlsx` and `Project.twb` in the same folder (Tableau auto-connects to the Excel source).
2. Open `Project.twb` in Tableau Desktop 2025.3+.
3. Click any country or customer to cross-filter all views.

**Publish to Tableau Public** *(not yet published — planned)*:
1. Open `Project.twb` in Tableau Desktop (with `Kevin_Cookie_Company_Data.xlsx` in the same folder so the connection resolves).
2. Sign in via **Server → Tableau Public → Save to Tableau Public As...** — this packages the Excel data into the published workbook automatically, since `.twb` alone is a live connection, not a self-contained file.
3. Give the workbook a public-facing title and save.
4. Copy the published view URL and add it to this README under a **Live Dashboard** link near the top.

## Future Improvements

- Add a rush-vs-standard profitability breakdown as its own view.
- Layer in a simple seasonal forecast for the next quarter.
- Publish to Tableau Public with a direct link in this README (see above).
