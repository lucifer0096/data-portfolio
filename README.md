# Data Analyst Portfolio – Excel, Power BI, Tableau, SQL, R, Python, Streamlit

Portfolio of analytics projects by **Rahul Bhaskaran**, showcasing end-to-end work across Excel, Power BI, **Tableau**, SQL, R, Python, and Streamlit. Projects focus on turning messy business and open data into clear, decision-ready insights, dashboards, and interactive apps.

---

## About me

- **Name:** Rahul Bhaskaran  
- **Role:** Data Analyst / Application Specialist  
- **Location:** New Zealand · India  

This repository collects personal and practice projects used to build skills in data analysis, visualisation, dashboard design, and analytics consulting.

---

## Projects

| Project | Tools | Dataset | Key Deliverables |
|---------|-------|---------|------------------|
| **British Airways Reviews** | **Tableau** | 1,300+ BA customer reviews | Dynamic service ratings dashboard: aircraft performance (A320 vs 777), geographic maps, metric parameter switching, cross-filters for route/seat/traveler insights |
| **Kevin Cookie Company Sales Analysis** | **Tableau, Excel** | Cookie company orders & customers | Business-focused sales dashboard: daily cookies & revenue, revenue by country, top customers, rush vs standard shipment behaviour, plus BA-style problem framing and recommendations |
| **Telco Customer Churn** | **Excel, R Shiny** | Telco Customer Churn | End-to-end churn analysis – Excel pivots → R replication → interactive Shiny app for contract/service/demographic patterns |
| **Online Retail Sales & CLV** | **Excel** | Online retail transactions | Revenue performance, customer lifetime value tiers, segmentation, time/geography patterns |
| **NZ Retail Sales Dashboard** | **Excel** | Stats NZ (19 regions, 2012–2025) | Regional sales trends with pivot slicers, line/bar charts, and growth heatmap highlighting Auckland |
| **Dev Employment Analytics** | Excel, **Tableau** | 73k Stack Overflow devs | Employment funnel, threshold-based filters (40–70%), experience/education and gender–age breakdowns |
| **Health & Lifestyle Analytics** | Python, Pandas, Streamlit, Plotly | Lifestyle survey data | E2E EDA, feature engineering, lifestyle risk score, interactive health-risk dashboard with what-if controls |
| **NBA 2024/25 Player Impact** | **Excel** | NBA 2k24–25 player stats | Player impact metrics, MVP/DPOY-style ranking, role-based insights |
| **Volcano Explorer** | **R Shiny**, Leaflet | Global Holocene volcanoes | Geospatial risk explorer with interactive map, filtering and glossary |
| **Paris Airbnb Regulation** | **Pandas, Seaborn, Jupyter** | **279k global Airbnb** | **Policy impact**: -78% hosts +35% prices post-2015 cap. Time-series + € benchmarking |
| **NZ Jobs Dashboard** | Python, Pandas, Streamlit, GitHub Actions | NZ analyst roles subset from OpenJobData | Live Streamlit dashboard for analyst, BI, reporting, and data roles in New Zealand; filterable job explorer; automated data refresh and verification workflow; parquet-based app pipeline. [Live app](https://lucifer0096-nz-jobs-dashboard-app.streamlit.app/) |

---

## Featured live app

- **NZ Jobs Dashboard:** https://lucifer0096-nz-jobs-dashboard-app.streamlit.app/

---

## How to navigate this repo

1. Start with the **Projects** table above and open the folder for the project you're interested in.  
2. Read the project-level `README.md` for context, dataset details, assumptions, and screenshots.  
3. Open the associated Excel / Power BI / Tableau / R / Python files to explore the analysis, models, dashboards, and apps.  

---

## Skills demonstrated

- **Data preparation:** 279k+ row cleaning (Airbnb), NZ retail aggregation (19 regions × 14 years), **1,300+ review normalization** (BA), feature engineering, ETL-style joins between customer/order tables, data type and country standardisation, parquet-based dataset preparation, and workflow-driven refresh pipelines  
- **Analysis:** Customer segmentation, cohort analysis, parameter-driven scenarios, time-series growth, risk scoring models, **policy impact quantification (Airbnb)**, **service performance diagnostics (BA)**, sales performance diagnostics, churn prediction, and job-market exploration through role grouping and filtering  
- **Visualization:** Executive KPI dashboards, Excel slicers/heatmaps, **R Shiny apps**, **Tableau dashboards (maps, parameters, actions)**, Power BI DAX measures, **dual-axis time-series**, and Streamlit dashboards for interactive data exploration  
- **Tooling:** Excel (pivot tables, slicers), **SQL**, Power BI/Tableau, Python (Pandas, Streamlit), R (Shiny), GitHub Actions, cross-tool workflows, **€ cross-city normalization**, **aircraft grouping + geo-mapping**, business-analyst style documentation and storytelling  

---

## Repository notes

Some projects are static analysis portfolios, while others include interactive dashboards or apps. The NZ Jobs Dashboard project also includes an automated GitHub Actions workflow for refreshing app data and verifying that the deployed app can read updated outputs.

---

## Source credit

The **NZ Jobs Dashboard** uses job-listing data from **OpenJobData**.  
Source: https://openjobdata.com  
Documentation: https://openjobdata.com/documentation
