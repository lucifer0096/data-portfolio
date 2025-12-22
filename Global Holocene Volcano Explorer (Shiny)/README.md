# Global Holocene Volcanoes – Interactive Risk & Glossary Map (Shiny)

Interactive Shiny application built on the Smithsonian Institution Global Volcanism Program Holocene volcano list. The app lets users explore volcanoes worldwide, filter by activity evidence and a simple risk band, and view structured glossary information about key volcanic terms.

---

## 📂 Dataset

- **Source:** Global Volcanism Program, Smithsonian Institution – *Volcanoes of the World* (v. 5.3.2; 30 Sep 2025) Holocene volcano list  
- **Access:** Holocene Volcano search page – https://volcano.si.edu/search_volcano.cfm  
- **Citation:**  
  Global Volcanism Program, 2025. *Volcanoes of the World* (v. 5.3.2; 30 Sep 2025). Smithsonian Institution, compiled by Venzke, E. https://doi.org/10.5479/si.GVP.VOTW5-2025.5.3  

- **Scope:** Global coverage of Holocene volcanoes (last ~10,000 years) with geographic, tectonic, and descriptive attributes.

**Key fields used in this app**

- *Location:* Country, Latitude, Longitude, Volcanic Region Group, Volcanic Region  
- *Morphology:* Volcano Landform, Primary Volcano Type  
- *Activity:* Activity Evidence, Last Known Eruption  
- *Physical / tectonic context:* Elevation (m), Tectonic Setting, Dominant Rock Type  

A derived **Risk** field is created in this project as a simple band (**High / Medium / Low / Unknown**) based on *Activity Evidence* for visualisation and filtering.

---

## 🛠️ Tools & skills

- **R** for data handling and reactive programming  
- **Shiny** for the multi‑tab interactive web application (map + glossary)  
- **Leaflet** for interactive web mapping, markers, clustering, and legends  
- Data cleaning and feature engineering in R (creating the **Risk** band and preparing the `volcanos.csv` input file)

---

## ❓ Business / analysis questions

- Where are Holocene volcanoes located globally, and how do they cluster by country and tectonic setting?  
- How does the distribution of volcanoes change when filtered by activity evidence or simple risk band?  
- How can key volcanic terms (landform, primary type, tectonic setting, activity evidence) be presented clearly for non‑experts while exploring the map?

---

## 🔎 Approach

### 1. Data preparation

- Downloaded the Holocene volcano list from the Global Volcanism Program search interface and exported it to a CSV (`volcanos.csv`) for use in R.  
- Imported the CSV into R without altering original column names (to retain spaces used in the GVP schema).  
- Created a derived **Risk** variable from *Activity Evidence*, grouping volcanoes into High, Medium, Low, and Unknown bands for easier communication in the map.

### 2. Application design (UI)

- Built a Shiny `fluidPage` layout with a title panel and two tabs:
  - **Map** – main interactive map and filters  
  - **Info / Glossary** – textual explanations and reference images  
- Added sidebar filters in the Map tab:
  - Country (All or one country)  
  - Activity Evidence (All or one GVP evidence category)  
  - Risk level (All or one of the derived risk bands)

### 3. Reactive filtering & summary

- Implemented a `reactive()` expression that subsets the volcano dataset based on selected country, activity evidence, and risk band.  
- Displayed a dynamic summary text (`Volcanoes shown: n`) above the map to clarify the current filter impact.

### 4. Mapping & visualisation

- Used **leaflet** to create an interactive base map with circle markers at each volcano’s latitude/longitude.  
- Colour‑coded markers by **Risk** using a discrete palette and added a legend explaining the bands.  
- Enabled marker clustering for dense regions to keep the map usable at global zoom levels.  
- Configured pop‑ups with rich information for each volcano, including name, country, region, landform, primary type, activity evidence, risk level, last known eruption, elevation, tectonic setting, and dominant rock type.

### 5. Glossary & documentation

- Added an **Info / Glossary** tab with bullet‑point definitions of important dataset fields:
  - Volcanic Region Group, Volcanic Region, Volcano Landform, Primary Volcano Type  
  - Activity Evidence, Risk, Last Known Eruption, Elevation (m)  
  - Tectonic Setting, Dominant Rock Type, Latitude / Longitude  
- Embedded reference images (`Image1.png`, `Image2.png`) summarising volcano types and tectonic settings.  
- Included an **“About this app”** section explaining purpose and authorship (Rahul Bhaskaran, Data Analyst).

---

## 🔥 Key insights

- The global map highlights strong clustering of Holocene volcanoes along plate boundaries (subduction and rift zones), especially in the Pacific “Ring of Fire”.  
- Filtering by **Activity Evidence** and **Risk** quickly reveals regions with dense clusters of recently active or well‑constrained volcanoes versus areas with uncertain or no Holocene activity.  
- The simple risk banding and glossary help non‑specialist users interpret complex volcanic metadata (activity evidence, tectonic setting, rock type) while exploring the map interactively.

---

## 🧪 How to use

### Run the app locally

1. Ensure R and the packages `shiny` and `leaflet` are installed.  
2. Place `volcanos.csv`, `app.R` (or the script containing this code), and images (`Image1.png`, `Image2.png`) in the same project directory.  
3. From R or RStudio, run:

source("app.R")

### Explore the **Map** tab

- Use **Country** to focus on a single country or keep **All** for a global view.  
- Adjust **Activity evidence** to see how the map changes for different evidence categories.  
- Use **Risk level** to highlight volcanoes in High / Medium / Low / Unknown bands.  
- Click markers to view detailed pop‑ups for each volcano.

### Use the **Info / Glossary** tab

- Read concise definitions of key dataset terms.  
- Examine reference images summarising volcano types and tectonic settings.  
- Review the “About this app” section for a quick explanation of the project’s goals.

---

## 🚀 Future improvements

- Replace any absolute CSV path in the code with a project‑relative path and prepare for deployment (e.g. shinyapps.io).  
- Refine the risk model by incorporating population exposure, proximity to settlements, or eruption frequency.  
- Add additional filters (e.g. elevation bands, tectonic setting, dominant rock type).  
- Provide summary charts alongside the map (e.g. volcano counts by risk level and country) using **plotly** or **ggplot2**.  
- Implement bookmarking or URL parameters so specific filter combinations can be shared directly.
