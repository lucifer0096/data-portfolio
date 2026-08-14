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

A derived **Risk** field (High / Medium / Low / Unknown) is built from *Activity Evidence* for visualization and filtering.

## Tools & Skills

- R for data handling and reactive programming
- Shiny for the multi-tab interactive application (map + glossary)
- Leaflet for interactive mapping, marker clustering, and legends
- Feature engineering: deriving the Risk band and preparing `volcanos.csv`

## Business / Analysis Questions

- Where are Holocene volcanoes located globally, and how do they cluster by country and tectonic setting?
- How does the distribution change when filtered by activity evidence or risk band?
- How can key volcanic terms be presented clearly to non-experts while exploring the map?

## Approach

1. **Data preparation** — exported the Holocene volcano list from the GVP search interface to `volcanos.csv`, imported into R preserving original column names, and derived the Risk band from Activity Evidence.
2. **Application design** — built a Shiny `fluidPage` with two tabs: **Map** (main interactive view and filters) and **Info / Glossary** (definitions and reference images).
3. **Reactive filtering** — a `reactive()` expression subsets the dataset by country, activity evidence, and risk band, with a live "Volcanoes shown: n" summary.
4. **Mapping** — Leaflet circle markers color-coded by Risk, clustered for dense regions, with rich per-volcano popups (name, country, region, landform, type, activity evidence, risk, last eruption, elevation, tectonic setting, rock type).
5. **Glossary** — a dedicated tab defining key dataset fields, with reference images and an About section.

## Key Insights

- Holocene volcanoes cluster strongly along plate boundaries, especially the Pacific "Ring of Fire."
- Filtering by Activity Evidence and Risk quickly separates well-documented, recently active regions from areas with uncertain or no Holocene activity.
- The simplified risk banding and glossary make dense volcanic metadata approachable for non-specialist users.

## How to Use

1. Ensure R and the `shiny` and `leaflet` packages are installed.
2. Place `volcanos.csv`, `app.R` (or the script containing this code), and the reference images in the same directory.
3. From R or RStudio, run:

```r
source("app.R")
```

4. In the **Map** tab, use the Country, Activity Evidence, and Risk Level filters, and click markers for detail popups.
5. In the **Info / Glossary** tab, review field definitions and reference images.

## Future Improvements

- Replace any absolute CSV paths with project-relative paths and deploy to shinyapps.io.
- Refine the risk model with population exposure, proximity to settlements, or eruption frequency.
- Add filters for elevation band, tectonic setting, and dominant rock type.
- Add summary charts (volcano counts by risk level and country) alongside the map.
- Support shareable filter states via URL parameters.
