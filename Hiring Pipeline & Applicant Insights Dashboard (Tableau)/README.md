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

*Verified directly against `Data/stackoverflow_full.csv` — two of the original four claims here were wrong and have been corrected below.*

- Men under 35 form the largest single segment (44,343 developers) with a 55.2% employment rate — matches the original claim.
- **Corrected:** developers with 20+ years of professional experience have essentially the same employment rate as the overall population (~52%, vs. a 53.6% baseline) — not the standout high-employment segment the dashboard originally claimed (previously stated as 65%).
- **Corrected — direction was backwards:** NoHigherEd respondents have a *higher* employment rate (58.9%) than Master's-degree holders (48.6%), and PhD holders have the lowest rate of any group (28.6%) — the opposite of what was previously claimed. This dataset can't say why (self-selection into further study, a "PhD == still in academia" effect, correlation with age/field, etc. are all plausible and none are controlled for here), but the direction in the data is clear.
- Raising the threshold above 60% narrows the pool to roughly the top 25% most experienced developers *(this claim describes the parameter/filter mechanic itself, not a data finding, and wasn't independently re-checked)*.
- **Caveat:** this is a single cross-sectional survey, not a controlled study — experience, education, age, and country are all correlated with each other, so none of these rates should be read as the isolated causal effect of one factor. A developer with a PhD is also, on average, older and in a different mix of countries/roles than one with NoHigherEd; the 28.6% PhD employment rate likely reflects some mix of those factors, not "getting a PhD reduces your employability."

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
- Control for confounds (age, country) when comparing education or experience groups — e.g. a simple logistic regression with multiple predictors, rather than one-way breakdowns, would separate out each factor's independent association with employment.
- Publish to Tableau Public with a direct link in this README (see above).
