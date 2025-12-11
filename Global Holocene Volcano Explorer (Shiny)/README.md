# Global Holocene Volcanoes – Interactive Risk & Glossary Map (Shiny)

Interactive Shiny application built on the Smithsonian Institution Global Volcanism Program Holocene volcano list, allowing users to explore volcanoes worldwide, filter by activity evidence and a simple risk band, and view structured glossary information about key volcanic terms. [web:112][file:1]

---

## Dataset

- **Source:** Global Volcanism Program, Smithsonian Institution – “Volcanoes of the World (v. 5.3.2; 30 Sep 2025)” Holocene volcano list. Accessed via the Holocene Volcano search page: https://volcano.si.edu/search_volcano.cfm. [web:112][file:1]  
- **Citation (recommended by GVP):**  
  Global Volcanism Program, 2025. *Volcanoes of the World* (v. 5.3.2; 30 Sep 2025). Smithsonian Institution, compiled by Venzke, E. https://doi.org/10.5479/si.GVP.VOTW5-2025.5.3. [file:1]  
- **Scope:** Global coverage of Holocene volcanoes (last ~10,000 years) with geographic, tectonic, and descriptive attributes. [web:112][file:1]  
- **Key fields used in this app:**  
  - Location: `Country`, `Latitude`, `Longitude`, `Volcanic Region Group`, `Volcanic Region`.  
  - Morphology: `Volcano Landform`, `Primary Volcano Type`.  
  - Activity: `Activity Evidence`, `Last Known Eruption`.  
  - Physical / tectonic context: `Elevation (m)`, `Tectonic Setting`, `Dominant Rock Type`.  

A derived **Risk** field is created in this project as a simple band (High / Medium / Low / Unknown) based on `Activity Evidence` for visualisation and filtering.

---

## Tools & skills

- **R** for data handling and reactive programming. [web:115][web:116]  
- **Shiny** for building the multi‑tab interactive web application (map plus glossary). [web:116]  
- **Leaflet** for interactive web mapping, markers, clustering, and legends. [web:116][web:119]  
- Data cleaning and feature engineering in R (creating the `Risk` band and preparing the `volcanos.csv` input file).

---

## Business / analysis questions

- Where are Holocene volcanoes located globally, and how do they cluster by country and tectonic setting? [web:112][file:1]  
- How does the distribution of volcanoes change when filtered by activity evidence or simple risk band?  
- How can key volcanic terms (landform, primary type, tectonic setting, activity evidence) be presented clearly for non‑experts while exploring the map?

---

## Approach

1. **Data preparation**  
   - Downloaded the Holocene volcano list from the Global Volcanism Program search interface and exported it to a CSV (`volcanos.csv`) for use in R. [web:112][file:1]  
   - Imported the CSV into R without altering original column names (to retain spaces used in the GVP schema).  
   - Created a derived `Risk` variable from `Activity Evidence`, grouping volcanoes into High, Medium, Low, and Unknown bands for easier communication in the map.

2. **Application design (UI)**  
   - Built a Shiny `fluidPage` with a title panel and two tabs:  
     - **Map** – main interactive map and filters.  
     - **Info / Glossary** – textual explanations and reference images.  
   - Added three filter controls in the Map sidebar:  
     - Country (`All` or a specific country).  
     - Activity Evidence (`All` or one of the GVP evidence categories).  
     - Risk level (`All` or one of the derived risk bands).

3. **Reactive filtering & summary**  
   - Implemented a `reactive()` expression that subsets the volcano dataset based on the selected country, activity evidence, and risk band.  
   - Displayed a dynamic summary text (`Volcanoes shown: n`) above the map to clarify current filter impact.

4. **Mapping & visualisation**  
   - Used `leaflet` to create an interactive base map with circle markers at each volcano’s latitude/longitude. [web:116][web:119]  
   - Colour‑coded markers by `Risk` using a discrete colour palette and added a legend explaining the bands.  
   - Enabled marker clustering for dense regions to keep the map usable at global zoom levels.  
   - Configured pop‑ups showing rich information for each volcano, including name, country, region, landform, primary type, activity evidence, risk level, last known eruption, elevation, tectonic setting, and dominant rock type.

5. **Glossary & documentation**  
   - Added an **Info / Glossary** tab containing bullet‑point definitions of important dataset fields: Volcanic Region Group, Volcanic Region, Volcano Landform, Primary Volcano Type, Activity Evidence, Risk, Last Known Eruption, Elevation (m), Tectonic Setting, Dominant Rock Type, Latitude/Longitude.  
   - Embedded reference images (`Image1.png`, `Image2.png`) summarising volcano types and tectonic settings.  
   - Included an “About this app” section explaining purpose and authorship (Rahul Bhaskaran, Data Analyst).

---

## Key insights

- The global map highlights strong clustering of Holocene volcanoes along plate boundaries (subduction and rift zones), especially in the Pacific “Ring of Fire”. [web:112][file:1]  
- Filtering by **Activity Evidence** and **Risk** quickly reveals regions with dense clusters of recently active or well‑constrained volcanoes versus areas with uncertain or no Holocene activity.  
- The simple risk banding and glossary help non‑specialist users interpret complex volcanic metadata (activity evidence, tectonic setting, rock type) while exploring the map interactively.

---

## How to use

1. **Run the app locally**  
   - Ensure R and the packages `shiny` and `leaflet` are installed.  
   - Place `volcanos.csv`, `app.R` (or the script containing this code), and images (`Image1.png`, `Image2.png`) in the same project directory.  
   - From R or RStudio, run `shiny::runApp()` or `source("app.R")` to launch the app in a browser.

2. **Explore the Map tab**  
   - Use **Country** to focus on a single country or keep **All** for a global view.  
   - Adjust **Activity evidence** to see how the map changes for different evidence categories.  
   - Use **Risk level** to highlight volcanoes in High / Medium / Low / Unknown bands.  
   - Click markers to view detailed pop‑ups for each volcano.

3. **Use the Info / Glossary tab**  
   - Read concise definitions of key dataset terms and examine the reference images summarising volcano types and tectonic settings.  
   - Review the “About this app” section for a quick explanation of the project’s goals.

---

## Future improvements

- Replace the absolute CSV path in the code with a project‑relative path and prepare for deployment (for example, to shinyapps.io).  
- Refine the risk model by incorporating population exposure, proximity to settlements, or eruption frequency.  
- Add additional filters (for example, elevation bands, tectonic setting, dominant rock type).  
- Provide summary charts alongside the map (for example, volcano counts by risk level and country) using `plotly` or `ggplot2`.  
- Implement bookmarking or URL parameters so specific filter combinations can be shared directly.
