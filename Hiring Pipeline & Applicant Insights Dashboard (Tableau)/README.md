# Hiring Pipeline & Applicant Insights Dashboard

Interactive Tableau dashboard analyzing 73,462 Stack Overflow developer survey responses (53% baseline employment rate), with dynamic threshold filtering across experience, education, and gender/age segments.

## Dataset

- **Source:** Stack Overflow developer survey extract, 73,462 records
- **Fields:** years of experience, education level, gender, age band, employment status

## Tools & Skills

- Tableau Public (parameters, filters, heatmaps)
- ETL of a 73k-row CSV into parameter-driven analytics
- Threshold-based filtering via a parameter slider

## Business Questions

- How does employment likelihood vary with experience and education?
- Which demographic segments have the highest and lowest employment rates?
- How does the applicant pool change as the employment-rate threshold is adjusted?

## Approach

1. Cleaned and loaded the 73k-row developer dataset into Tableau.
2. Built a parameter-driven threshold slider (40–70%) to filter the pool by employment rate.
3. Built three breakdown views: experience level, education level, and gender × age (heatmap).

## Key Insights

- Developers with 20+ years of experience have the highest employment rate (65%).
- Master's-degree holders are employed at 58% vs. 48% for those with no higher education.
- Men under 35 form the largest single segment (42k developers) with a 55% employment rate.
- Raising the threshold above 60% narrows the pool to roughly the top 25% most experienced developers.

## How to Use

**Open locally:**
1. Keep `Project.twb` and the `Data` folder together (Tableau connects to the CSV via a relative path).
2. Open `Project.twb` in Tableau Desktop or Tableau Public.
3. Adjust the threshold slider to explore different employment-rate cutoffs.
4. Use the Experience Level filter to see how segment composition changes.

**Publish to Tableau Public** *(not yet published — planned)*:
1. Open `Project.twb` in Tableau Desktop (with the `Data` folder alongside it).
2. Sign in via **Server → Tableau Public → Save to Tableau Public As...** — this packages the CSV into the published workbook automatically, since `.twb` alone is a live connection, not a self-contained file.
3. Give the workbook a public-facing title and save.
4. Copy the published view URL and add it to this README under a **Live Dashboard** link near the top.

## Future Improvements

- Add a role/title breakdown (e.g. data analyst vs. software engineer) alongside experience and education.
- Publish to Tableau Public with a direct link in this README (see above).
