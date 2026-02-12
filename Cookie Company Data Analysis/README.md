# Kevin Cookie Company Sales Analysis

**Business Problem**: Kevin Cookie Company needs actionable insights into sales performance across international markets to optimize customer targeting, identify high-value opportunities, and improve operational efficiency.

## Executive Summary
Interactive Tableau dashboard analyzing ~200 orders from 50 customers across United States, Canada, United Kingdom, and Germany (2024-2025 data). Key focus: revenue trends, geographic performance, top customers, and daily sales patterns with cross-filtering.

## Business Context
**Stakeholder**: Sales Director seeking data-driven decisions for:
- Market expansion prioritization
- Top customer retention strategies  
- Rush shipment profitability analysis
- Seasonal demand forecasting

**Data Source**: https://onedrive.live.com/view.aspx?resid=B09F9559F6A16B6C%21103060&authkey=%21AMDmrXy5mgOxF3g

Customers (50 records): Customer ID, Name, Country
Orders (200 records): Order ID, Customer ID, Order Date, Cookies Shipped, Revenue, Rush Shipment

## Problem Statement
**Primary Business Questions**:
1. Which countries generate highest revenue per cookie?
2. Who are the top 10 customers by revenue?
3. What are daily/weekly sales patterns?
4. Do rush shipments improve profitability?

↓ Cross-filters: Country ↔ Customer


## Dashboard Components
| Visualization | Purpose | Key Features |
|---------------|---------|--------------|
| **Daily Cookies** | Volume trends | Date heat map, country filter |
| **Daily Revenue** | Revenue patterns | Date heat map, customer filter |
| **Country Map** | Geo-performance | Revenue color encoding, click-to-filter |
| **Top Customers** | Account analysis | Descending revenue sort, country filter |

## Key Expected Insights
United States dominates revenue (after "U.S." standardization)

Top 5 customers likely drive 40%+ total revenue

Rush shipments correlate with higher average order value

Clear daily/weekly sales seasonality patterns


## Technical Implementation
Data Flow: Excel (.xlsx) → Tableau Extract (.hyper) → Dashboard (.twb)

Data Preparation:

Customer ID (1:M relationship join)

Country standardization: REPLACE("U.S.", "United States")

Aggregations: SUM(Revenue), SUM(Cookies Shipped)

Date truncation: Day level for heatmaps


## Business Recommendations Framework
1. Market Focus: Prioritize Top 3 countries by revenue/cookie

2. Customer Strategy: VIP program for Top 10 revenue accounts

3. Operations: Review rush shipment pricing/profitability

4. Forecasting: Target identified seasonal peak periods


## Setup Instructions
```bash
1. Place Kevin_Cookie_Company_Data.xlsx and Project.twb in same folder
2. Open Project.twb in Tableau Desktop (2025.3+)
3. File → Open → Project.twb (auto-connects Excel data)
4. Interact: Click countries/customers to cross-filter all views
5. Publish: Tableau Public/Server for stakeholder sharing

