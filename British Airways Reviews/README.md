# British Airways Reviews Analysis

Interactive Tableau dashboard analyzing 1,300+ British Airways customer reviews to uncover service trends by aircraft, route, country, and traveler type. Built with dynamic parameters, geographic maps, and cross-filters for stakeholder-facing exploration.

## Dataset

- **Scope:** ~1,300 verified trip reviews, rated 1–10 across 7 service metrics
- **Fields:** aircraft type, route, seat type, traveler type, recommendation status, date flown, departure country

## Tools & Skills

- Tableau Desktop (parameters, LOD calculations, actions, extracts)
- Data prep: relating review and country reference tables
- Visualization: maps, bar charts, line trends, heatmaps
- Interactivity: cross-filters, highlight actions

## Business Questions

- How does perceived service quality vary by aircraft type and route length?
- Where are the geographic strengths and weaknesses in customer experience?
- Which traveler segments report the highest and lowest satisfaction?

## Approach

1. **Dynamic metrics** — a parameter dropdown switches the view between Overall Rating, Seat Comfort, Cabin Staff Service, Entertainment, Food & Beverages, Ground Service, and Value for Money.
2. **Aircraft analysis** — grouped categories (Boeing 777, A320 family, A380, etc.) compared by average score and review volume.
3. **Geographic view** — maps by departure country/continent, color-coded by performance.
4. **Time trends** — monthly averages with date-flown filtering.
5. **Interactive filters** — route, seat type, traveler type, and recommendation status, all cross-filtered.

## Key Insights

- A320 flights score higher on Entertainment (avg. 6.2) than Boeing 777 (avg. 5.1).
- Ground Service ratings dip noticeably on long-haul routes (8+ hours).
- Business class consistently leads on Seat Comfort (avg. 8.1).

## How to Use

**Open locally:**
1. Download `Project.twbx` (self-contained) or `Project.twb` plus the `Data` folder.
2. Open in Tableau Desktop or Tableau Public (2025.1+).
3. Refresh extracts if needed (`Ctrl+R`).

**Publish to Tableau Public** *(not yet published — planned)*:
1. Open `Project.twbx` in Tableau Desktop.
2. Sign in via **Server → Tableau Public → Save to Tableau Public As...**
3. Give the workbook a public-facing title and save. Tableau Public re-extracts and uploads all data automatically, since `.twbx` is self-contained.
4. Copy the published view URL and add it to this README under a **Live Dashboard** link near the top.

## Future Improvements

- Add sentiment analysis on free-text review comments.
- Break out ground service by airport rather than just route length.
- Publish to Tableau Public with a direct link in this README (see above).
