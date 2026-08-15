# NZ Retail Sales Dashboard

Interactive Excel dashboard analyzing Stats NZ Retail Trade data (2012–2025) across 19 New Zealand regions.

[View the static PDF version](NZ_Retail_Sales_Dashboard.pdf)

## Dataset

- **Source:** [Stats NZ Retail Trade Survey via Figure.NZ](https://figure.nz/table/nlxHOcUAme9KJ0iX) (open license)
- **Scope:** 19 NZ regions, 2012–2025

## Tools & Skills

- Excel pivot tables with slicers (Year + Region filtering)
- Conditional formatting for growth heatmaps
- Chart design: line trends and bar comparisons

## Business Questions

- How has regional retail sales performance changed from 2012 to 2025?
- Which regions are growing fastest, and which are lagging?
- How does 2025 regional performance compare at a glance?

## Approach

1. Cleaned and standardized the Stats NZ regional retail trade data.
2. Built pivot tables with Year and Region slicers for interactive filtering.
3. Added a line chart for regional sales trends (2012–2025) and a bar chart for 2025 regional comparison.
4. Built a conditional-formatting heatmap to highlight regional growth (green = highest sales).

## Key Insights

- Auckland dominates 2025 retail sales, at roughly $45B NZD.
- Northland shows steady growth, from ~$2.1B (2012) to ~$3.7B (2025).
- The growth heatmap makes regional divergence in trajectory easy to spot at a glance.
- **Caveat:** these are nominal dollar figures, not adjusted for inflation or population. Part of every region's "growth" reflects NZ-wide price inflation over 2012–2025, and Auckland's lead is partly a function of it having the largest and fastest-growing population, not necessarily stronger per-capita retail performance. Read the rankings as nominal totals, not real growth or per-capita comparisons.

## Repository Files

| File | Description |
|---|---|
| `NZ_Retail_Sales_Dashboard.xlsx` | Interactive workbook (recommended) |
| `NZ_Retail_Sales_Dashboard.pdf` | Static version for quick viewing |

## How to Use

1. Download `NZ_Retail_Sales_Dashboard.xlsx`.
2. Use the Year and Region slicers to filter the pivot views.
3. Review the line/bar charts and growth heatmap for trends and comparisons.
4. Use the PDF for a quick, non-interactive view.

## Future Improvements

- Add a per-capita or population-adjusted sales view.
- Layer in a simple year-over-year growth-rate table alongside the heatmap.
