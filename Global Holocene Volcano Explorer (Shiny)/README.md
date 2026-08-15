# Global Holocene Volcanoes – Interactive Risk & Glossary Map

Interactive R Shiny application built on the Smithsonian Institution's Global Volcanism Program Holocene volcano list. Lets users explore volcanoes worldwide, filter by activity evidence and a derived risk band, and view structured glossary information about key volcanic terms.

## Dataset

- **Source:** Global Volcanism Program, Smithsonian Institution — *Volcanoes of the World* (v. 5.3.2; 30 Sep 2025), Holocene volcano list
- **Access:** [GVP Holocene Volcano search](https://volcano.si.edu/search_volcano.cfm)
- **Citation:** Global Volcanism Program, 2025. *Volcanoes of the World* (v. 5.3.2; 30 Sep 2025). Smithsonian Institution, compiled by Venzke, E. https://doi.org/10.5479/si.GVP.VOTW5-2025.5.3
- **Scope:** Global coverage of Holocene volcanoes (last ~10,000 years) with geographic, tectonic, and descriptive attributes.

**Key fields**

| Category | Fields |
|---|---|
| Location | Country, Latitude, Longitude, Volcanic Region Group, Volcanic Region |
| Morphology | Volcano Landform, Primary Volcano Type |
| Activity | Activity Evidence, Last Known Eruption |
| Tectonic context | Elevation (m), Tectonic Setting, Dominant Rock Type |

A derived **Risk** field (High / Medium / Low / Unknown) is built from *Activity Evidence* for visualization and filtering. The mapping is one-to-one and consistent throughout the data (`Eruption Dated`/`Eruption Observed` → High, `Evidence Credible` → Medium, `Evidence Uncertain` → Low, `Unrest / Holocene` → Unknown), but the derivation itself was done outside this repo (likely in the source Excel file) before being exported to `Data/Volcanos.csv` — `app.R` only reads the pre-computed `Risk` column, it doesn't derive it. See the caveat under Approach.

## Tools & Skills

- R for data handling and reactive programming
- Shiny for the multi-tab interactive application (map + glossary)
- Leaflet for interactive mapping, marker clustering, and legends
- Data preparation: preparing `Data/Volcanos.csv` for use in R (the Risk band itself was derived upstream — see caveat under Approach)

## Business / Analysis Questions

- Where are Holocene volcanoes located globally, and how do they cluster by country and tectonic setting?
- How does the distribution change when filtered by activity evidence or risk band?
- How can key volcanic terms be presented clearly to non-experts while exploring the map?

## Approach

1. **Data preparation** — exported the Holocene volcano list from the GVP search interface to `Data/Volcanos.csv`, imported into R preserving original column names. **Caveat:** the Risk band already exists as a column in `Data/Volcanos.csv` when `app.R` reads it — the Activity Evidence → Risk derivation was done upstream (outside this repo, likely in the accompanying `Volcanos.xlsx.xlsx`), not by any script checked in here. `app.R` filters and displays the Risk column; it doesn't compute it.
2. **Application design** — built a Shiny `fluidPage` with two tabs: **Map** (main interactive view and filters) and **Info / Glossary** (definitions and reference images).
3. **Reactive filtering** — a `reactive()` expression subsets the dataset by country, activity evidence, and risk band, with a live "Volcanoes shown: n" summary.
4. **Mapping** — Leaflet circle markers color-coded by Risk, clustered for dense regions, with rich per-volcano popups (name, country, region, landform, type, activity evidence, risk, last eruption, elevation, tectonic setting, rock type).
5. **Glossary** — a dedicated tab defining key dataset fields, with reference images and an About section.

## Key Insights

- Holocene volcanoes cluster strongly along plate boundaries, especially the Pacific "Ring of Fire."
- Filtering by Activity Evidence and Risk quickly separates well-documented, recently active regions from areas with uncertain or no Holocene activity.
- The simplified risk banding and glossary make dense volcanic metadata approachable for non-specialist users.

## Project Structure

```text
Global Holocene Volcano Explorer (Shiny)/
├── app.R
├── Data/
│   └── Volcanos.csv
└── www/
    ├── Image1.png
    └── Image2.png
```

`www/` holds the images referenced from the Info/Glossary tab — Shiny only serves static assets from a folder with that exact name, relative to `app.R`.

## How to Use

**Run locally:**

1. Install R and the `shiny` and `leaflet` packages:

```r
install.packages(c("shiny", "leaflet"))
```

2. Open this folder in RStudio (or set it as your working directory), then run:

```r
shiny::runApp("app.R")
```

3. In the **Map** tab, use the Country, Activity Evidence, and Risk Level filters, and click markers for detail popups.
4. In the **Info / Glossary** tab, review field definitions and reference images.

**Deploy to shinyapps.io:**

1. Install and configure `rsconnect` with your shinyapps.io account token.
2. From this folder, run:

```r
rsconnect::deployApp()
```

## Future Improvements

- Add the Activity Evidence → Risk derivation as an actual R script in this repo, rather than relying on a pre-computed column, so the mapping is transparent and reproducible.
- Refine the risk model with population exposure, proximity to settlements, or eruption frequency.
- Distinguish "Unknown" Activity Evidence as a data-completeness gap in the UI, rather than presenting it as a normal risk category alongside High/Medium/Low.
- Explicitly bind the color palette to named risk levels (`c(High="red", Medium="orange", Low="yellow", Unknown="black")`) instead of positional matching, to guard against silent mis-coloring if the factor level order ever changes.
- Add filters for elevation band, tectonic setting, and dominant rock type.
- Add summary charts (volcano counts by risk level and country) alongside the map.
- Support shareable filter states via URL parameters.
