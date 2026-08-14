# Paris Airbnb Regulation Impact Analysis

Jupyter analysis quantifying the impact of Paris's 2015 120-day short-term rental cap, using a 279k-row global Airbnb listings dataset (65k Paris-focused). Finds a 78% drop in new host growth and a 35% rise in nightly prices post-regulation, benchmarked against peer cities.

## Dataset

- **Source:** [Maven Analytics – Airbnb Listing Analysis](https://mavenanalytics.io/guided-projects/airbnb-listing-analysis) (279k global listings, scraped ~2021, ISO-8859-1 encoding)
- **Scope:** Paris (64,690 listings, 23% of total), benchmarked against 10 peer cities (NYC, Sydney, Rome, Rio, etc.)

**Key fields**

| Field | Description |
|---|---|
| `host_since` | Host join date (parsed to datetime for time-series) |
| `neighbourhood` | Paris arrondissements (80+ groups) |
| `city` | Global city coverage |
| `price` | Nightly rate in local currency, normalized to `price_eur` |
| `accommodates` | Listing capacity (0–16 guests) |

**Preparation:** currency conversion to EUR (Paris = 1.0, Sydney = 0.61, NYC = 0.92), filters for `price > 0` and `accommodates > 0`, and exclusion of outliers (listings priced above ~€12k).

## Tools & Skills

- Pandas ETL: `groupby`, yearly resampling, filtering/querying
- Seaborn/Matplotlib EDA (horizontal bar charts, dual-axis time-series)
- Time-series analysis on host growth by year
- Cross-city currency normalization and benchmarking
- Data quality checks (zero-accommodates and zero-price records, COVID-era validation)

## Business Questions

- Did the 2015 regulation discourage new host listings in Paris?
- Did the resulting supply squeeze reduce affordability for guests?
- How did the 120-day cap reshape Paris's market relative to peer cities?

## Approach

1. **Data cleaning** — parsed `host_since` to datetime, filtered to Paris, normalized prices to EUR.
2. **Paris deep-dive** — aggregated by neighbourhood (e.g. Élysée ~€210 vs. Ménilmontant ~€75) and by capacity.
3. **Time-series** — resampled host counts and average price by year, plotted on a dual axis with the 2015 regulation marked.
4. **Cross-city comparison** — built a pivot of average EUR price and capacity across the top 10 cities.
5. **COVID overlay** — used the 2020 demand cliff as an independent check that the 2015 signal isn't an artifact.

## Key Insights

- New host growth fell ~78% after 2015 (from ~4,500/year to ~900/year).
- Average nightly price rose ~35% (from ~€110 to ~€150+).
- Paris shows the sharpest post-regulation drop among peer cities; Sydney and NYC stayed comparatively steady.
- Neighbourhood prices vary roughly 3x between the most and least expensive areas (Élysée vs. Ménilmontant).
- Professional/multi-listing hosts dominate the post-COVID price recovery (€150+).

## How to Use

```bash
pip install -r requirements.txt
jupyter notebook Project.ipynb
```

Read the notebook top to bottom: data quality checks → time-series → cross-city comparison. The dual-axis regulation chart is roughly two-thirds of the way through the notebook.

## Future Improvements

- Add a Folium map of Paris with per-neighbourhood price heatmaps.
- Build a Streamlit dashboard with a pre/post-2015 toggle.
- Run formal statistical tests (t-test) on pre/post-2015 price and host-growth differences.
- Recreate the dashboard in Power BI using slicers and DAX time intelligence.
- Extend to monthly-granularity data to support causal regression analysis.
