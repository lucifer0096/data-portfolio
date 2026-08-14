# Data Analyst Portfolio

![Tableau](https://img.shields.io/badge/Tableau-E97627?style=flat&logo=tableau&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat&logo=powerbi&logoColor=black)
![Excel](https://img.shields.io/badge/Excel-217346?style=flat&logo=microsoftexcel&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![R](https://img.shields.io/badge/R-276DC3?style=flat&logo=r&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue)

Portfolio of analytics projects by **Rahul Bhaskaran**, covering end-to-end work across Excel, Power BI, Tableau, SQL, R, Python, and Streamlit. Projects turn messy business and open data into decision-ready insights, dashboards, and interactive apps.

## About Me

- **Role:** Data Analyst / Application Specialist
- **Location:** New Zealand · India

This repository collects personal and practice projects used to build and demonstrate skills in data analysis, visualization, dashboard design, and analytics consulting.

## Featured Live Apps

- **[NZ Jobs Dashboard](https://lucifer0096-nz-jobs-dashboard-app.streamlit.app/)** — a live Streamlit app with an automated GitHub Actions data-refresh pipeline, not just a static analysis.
- **[Health & Lifestyle Analytics Dashboard](TODO-add-streamlit-cloud-url-here)** — a live Streamlit app with an interactive risk-scoring "what-if" explorer.

## Projects

| Project | Tools | Dataset | Key Deliverables |
|---|---|---|---|
| [British Airways Reviews](British%20Airways%20Reviews) | Tableau | 1,300+ BA customer reviews | Dynamic service-rating dashboard: aircraft performance, geographic maps, parameter switching, route/seat/traveler cross-filters |
| [Kevin Cookie Company Sales Analysis](Cookie%20Company%20Data%20Analysis) | Tableau, Excel | Cookie company orders & customers | Sales dashboard: daily revenue, revenue by country, top customers, rush-shipment analysis, business recommendations |
| [Telco Customer Churn Explorer](Telco%20Customer%20Churn%20Explorer) | Excel, R, R Shiny | Telco Customer Churn dataset | End-to-end churn analysis — Excel pivots → R replication → interactive Shiny app |
| [Online Retail Sales & CLV Analysis](Online%20Retail%20Sales%20Analysis) | Excel | Online retail transactions | Revenue performance, customer lifetime value tiers, segmentation, time/geography patterns |
| [NZ Retail Sales Dashboard](NZ%20Retail%20Sales%20Dashboard) | Excel | Stats NZ (19 regions, 2012–2025) | Regional sales trends with pivot slicers, line/bar charts, growth heatmap |
| [Hiring Pipeline & Applicant Insights Dashboard](Hiring%20Pipeline%20%26%20Applicant%20Insights%20Dashboard%20%28Tableau%29) | Tableau | 73k+ Stack Overflow developers | Employment funnel, threshold-based filters, experience/education and gender-age breakdowns |
| [Health & Lifestyle Analytics](Health-and-Lifestyle-Analysis) | Python, Pandas, Streamlit, Plotly | Lifestyle survey data | Full EDA, feature engineering, lifestyle risk score, interactive Streamlit dashboard. **[Live app](TODO-add-streamlit-cloud-url-here)** |
| [NBA 2024/25 Player Impact & Awards Analysis](NBA%202k24-25%20Analysis) | Excel | 16k+ NBA player game logs | Player impact metrics, MVP/DPOY-style ranking, role-based insights |
| [Global Holocene Volcano Explorer](Global%20Holocene%20Volcano%20Explorer%20%28Shiny%29) | R, R Shiny, Leaflet | Smithsonian GVP Holocene volcano list | Geospatial risk explorer with interactive map, filters, and glossary |
| [Paris Airbnb Regulation Impact Analysis](Airbnb%20Listing%20Analysis) | Python, Pandas, Seaborn, Jupyter | 279k global Airbnb listings | Policy impact analysis: −78% new hosts, +35% prices post-2015 cap; time-series + cross-city benchmarking |
| [NZ Jobs Dashboard](NZ-Jobs-Dashboard) | Python, Pandas, Streamlit, GitHub Actions | NZ analyst roles (OpenJobData) | **[Live app](https://lucifer0096-nz-jobs-dashboard-app.streamlit.app/)** — filterable job explorer with automated data-refresh pipeline |

## How to Navigate This Repo

1. Start with the **Projects** table above and open the folder for the project you're interested in.
2. Read the project's own `README.md` for context, dataset details, assumptions, and approach.
3. Open the associated Excel / Power BI / Tableau / R / Python files to explore the analysis, dashboards, and apps.

## Skills Demonstrated

- **Data preparation:** large-scale cleaning (279k+ Airbnb rows, 73k+ developer records), multi-year regional aggregation, review-data normalization, feature engineering, ETL-style joins, parquet-based pipelines, automated refresh workflows
- **Analysis:** customer segmentation, cohort analysis, parameter-driven scenarios, time-series growth, risk scoring, policy-impact quantification, churn analysis, service-performance diagnostics, job-market exploration
- **Visualization:** executive KPI dashboards, Excel slicers/heatmaps, R Shiny apps, Tableau dashboards (maps, parameters, actions), Power BI, dual-axis time-series, Streamlit apps
- **Tooling:** Excel (pivot tables, slicers), SQL, Power BI, Tableau, Python (Pandas, Streamlit), R (Shiny), GitHub Actions, cross-tool workflows, business-analyst-style documentation

## Repository Notes

Most projects are static analysis portfolios; several include interactive dashboards or apps. The NZ Jobs Dashboard also includes an automated GitHub Actions workflow that refreshes app data and verifies the deployed app can read the updated outputs.

## License

This repository is licensed under the [MIT License](LICENSE).

## Source Credit

The **NZ Jobs Dashboard** uses job-listing data from [OpenJobData](https://openjobdata.com) ([documentation](https://openjobdata.com/documentation)).
