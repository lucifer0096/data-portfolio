# Paris Airbnb Regulation Impact Analysis (2015) – Policy Effect Quantification

Interactive Jupyter analysis quantifying Paris' 120-day rental cap impact using 279k global Airbnb listings (65k Paris focus). Reveals -78% new host drop and +35% price rise post-regulation, benchmarked against top cities.

📂 **Dataset**
[Source: Maven Analytics Airbnb Listing Analysis](https://mavenanalytics.io/guided-projects/airbnb-listing-analysis) – 279k global listings scraped ~2021 (ISO-8859-1 encoding).
**Scope**: Paris (64,690 listings, 23% total) benchmarked vs top 10 cities (NYC, Sydney, Rome, Rio etc.).
**Key fields**:
- `host_since`: Host join date (datetime → time-series)
- `neighbourhood`: Paris arrondissements (80+ groups)
- `city`: Global coverage (Paris, NYC etc.)
- `price`: Nightly € (raw + `price_eur` normalized)
- `accommodates`: Capacity (0-16 guests)

**Prep**: € conversion (Paris=1.0, Sydney=0.61, NYC=0.92), filters (`price>0`, `accommodates>0`), outliers excluded (€12k errors).

🛠️ **Tools & Skills**
- Pandas ETL (groupby, resample 'YE', query/filtering)
- Seaborn/Matplotlib EDA visuals (barh, dual-axis time-series)
- Time-series analysis (host_since yearly aggregation)
- Cross-city € normalization/benchmarking
- Data quality (54 zero-accommodates, 62 zero-price → COVID validation)

❓ **Business Questions**
**Hosts**: Did 2015 regulation discourage new listings?  
**Guests**: Did supply squeeze hurt affordability?  
**Policy**: How did 120-day cap reshape Paris vs peers?

🔎 **Approach**
1. **Data Cleaning**: 279k CSV → datetime `host_since` → Paris filter → € normalization.
2. **Paris Deep-Dive**: Neighborhood agg (Elysee €210 vs Menilmontant €75), capacity scaling.
3. **Time-Series**: Yearly resample → hosts count + avg price → dual-axis plot (2015 line).
4. **Cross-City**: Top 10 € avg/capacity pivot → 6-panel comparison.
5. **COVID Overlay**: 2020 cliff validates regulation signal.

🔥 **Key Insights**
- **Regulation**: Hosts -78% post-2015 (4,500→900/yr), prices +35% (€110→€150+).
- **Paris Unique**: Sharpest drop vs peers (Sydney/NYC steady).
- **Neighborhoods**: Elysee 3x Menilmontant (€210 vs €75).
- **Supply Effect**: Pro hosts dominate recovery (€150+ post-COVID).

🧪 **How to Use**
```bash
pip install -r requirements.txt
jupyter notebook Project.ipynb

EDA scroll: Quality → time-series → cross-city.

Dual-axis (~Cell 20): 2015 signal clear.

Static view: Project.html.

🚀 Future Improvements

Folium map (Paris € heatmaps—top5 sample).

Streamlit dashboard (pre/post toggles).

Stats tests (t-test pre/post-2015).

Power BI (slicers/DAX time-intelligence).

Monthly data → causal regression.

text
