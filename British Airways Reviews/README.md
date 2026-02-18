# British Airways Reviews Analysis

Interactive Tableau dashboard analyzing 1,300+ British Airways customer reviews to uncover service trends by aircraft, route, country, and traveler type. Built with dynamic parameters, geographic maps, and cross-filters for business insights.

## Project Overview
This dashboard visualizes British Airways review data (ratings 1-10 across 7 metrics) from ~1,300 verified trips. Key features:
- **Dynamic Metrics**: Parameter dropdown switches between Overall Rating, Seat Comfort, Cabin Staff Service, Entertainment, Food & Beverages, Ground Service, Value for Money.
- **Aircraft Analysis**: Grouped categories (Boeing 777, A320 family, A380, etc.) with bar charts showing average scores and review volume.
- **Geographic View**: Maps by departure country/continent with color-coded performance.
- **Time Trends**: Monthly averages and date-flown filters.
- **Interactive Filters**: Route, seat type, traveler type (Business, Couple, Solo), recommendation status.

## Key Insights
- A320 flights score higher on Entertainment (avg 6.2) vs Boeing 777 (5.1).
- Ground Service dips for long-haul routes (>8hrs).
- Business class consistently tops Seat Comfort (8.1 avg).

## Tech Stack & Features
✅ Tableau Desktop 2025.3 (Parameters, LOD calcs, Actions, Extracts)
✅ Data Prep: CSV relationships (reviews ↔ countries)
✅ Visuals: Maps, Bar charts, Line trends, Heatmaps
✅ Interactivity: Cross-filters, Highlight Actions
✅ Files: .twb (source), .twbx (packaged), raw CSVs

## Setup Instructions
1. Download `.twbx` (easiest) or `.twb` + CSVs.
2. Open in Tableau Desktop/Public ≥2025.1.
3. Refresh extracts if needed (`Ctrl+R`).
4. Publish to Tableau Public for sharing.
