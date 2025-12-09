# Online Retail Sales & Customer Lifetime Value Analysis (Excel)

Analyse online retail transactions to understand product performance, sales timing, geographic patterns, and customer lifetime value (CLV), and to identify high‑value customers and priority markets for growth.

---

## Dataset

- **Source:** Historical online retail transactions (non‑UK focused view plus global CLV analysis).  
  Dataset: https://www.kaggle.com/datasets/vijayuv/onlineretail/data?select=OnlineRetail.csv  
- **Size:** ~500k invoice lines aggregated to 4,372 unique customers.  
- **Key fields:** `InvoiceNo`, `CustomerID`, `Product`, `Quantity`, `UnitPrice`, `InvoiceDate` (date & hour), `Country`, derived NetSales, and CLV tiers.

---

## Tools & skills

- Excel data cleaning and preprocessing (working dataset derived from raw export).  
- Calculated columns for NetQuantity, NetSales, and customer‑level metrics (TotalRevenue, OrderCount, AvgOrderValue).  
- CLV tiering using percentile‑based thresholds (for example, High / Medium / Low value customers).  
- PivotTables and Excel dashboarding for product, time, country, and customer segmentation.

---

## Business questions

- Which products and categories drive the majority of revenue and order volume?  
- How do sales patterns vary by day of week, hour of day, and geography?  
- How is CLV distributed across the customer base, and which customers are truly high value?  
- Which regions and customer segments should be prioritised for marketing and retention?

---

## Approach

1. **Data preparation**  
   - Imported the full transactional dataset and standardised key fields.  
   - Created NetQuantity and NetSales measures and filtered out cancellations or invalid records where appropriate.

2. **Customer‑level modelling**  
   - Aggregated invoice lines to customer level, calculating TotalRevenue, OrderCount, and AvgOrderValue.  
   - Assigned CLV tiers using percentile‑based thresholds on TotalRevenue to separate high‑, mid‑, and low‑value customers.

3. **Segmentation and analysis**  
   - Built PivotTables by product, day/hour, country, and CLV tier.  
   - Analysed revenue contribution by hero products, high‑value customers, and key markets.  

4. **Dashboard & narrative**  
   - Designed an interactive Excel dashboard bringing together product, time, geography, and CLV views.  
   - Documented findings and recommendations in a dedicated “Insights” worksheet.

---

## Key insights

- A small group of hero products (for example, gift and homeware items) drives a large share of both quantity and revenue.  
- Sales are concentrated on specific days and peak between 10:00 and 14:00, indicating strong daytime trading patterns.  
- A handful of European markets (Netherlands, EIRE, Germany, France, Australia) account for most non‑UK revenue.  
- CLV is highly skewed: high‑CLV customers are a minority of the base but contribute the majority of total revenue.  
- High‑value customers are heavily concentrated in the UK, with additional high‑value pockets in Netherlands, Germany, France, and EIRE.

---

## How to use

- Open the Excel workbook in this folder (for example, `OnlineRetail Project.xlsx`).  
- Start with the **Info** tab for project overview, dataset summary, key insights, and navigation.  
- Use **Online Retail Full Dataset** to review raw transactional data.  
- Explore **Online Retail Working Dataset** for cleaned data and exploratory pivots (top products, sales by day/hour, country, repeat customers).  
- Use **CLV Analysis** for customer‑level tables, CLV tier calculations, and CLV‑related pivots (tiers, country vs tier).  
- Explore the **Dashboard** tab for combined product, time, geography, and CLV views, then read the **Insights** tab for narrative commentary.

---

## Future improvements

- Incorporate margin data to move from revenue‑based CLV to profit‑based CLV.  
- Add basic cohort and retention analysis to track customer behaviour over time.  
- Automate data refresh using Power Query or a database connection.  
- Build a companion Power BI report for richer interactivity and stakeholder sharing.
