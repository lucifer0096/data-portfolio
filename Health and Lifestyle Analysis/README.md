# Health & Lifestyle Analytics Dashboard

Interactive health and lifestyle risk dashboard built from a full exploratory data analysis (EDA) notebook and deployed as a Streamlit app.

## Project Goal

Identify and explore high-risk individuals in a synthetic population of 7,500 adults using lifestyle, BMI, sleep, stress, and chronic-disease data. The project follows a typical analyst pipeline: raw CSV → EDA in Jupyter → feature engineering → interactive Streamlit dashboard.

## Dataset

- **Source:** [Health & Lifestyle Dataset (Kaggle)](https://www.kaggle.com/datasets/sahilislam007/health-and-lifestyle-dataset) — synthetic
- **Size:** 7,500 records, 13 raw input fields (age, gender, BMI, smoking, exercise, diet, alcohol, sleep, stress, chronic disease, etc.), 22 features after engineering
- **Baseline stats:** ~19.3% chronic disease prevalence; ~16.4% flagged high-risk by lifestyle score

## Tools & Skills

| Layer | Tools |
|---|---|
| EDA | Python, Pandas, NumPy, Matplotlib/Seaborn |
| Feature engineering | Pandas |
| Dashboard | Streamlit, Plotly |
| Optional ML | scikit-learn, joblib |

## Approach

### 1. Exploratory data analysis (`Project.ipynb`)
- Data loading, cleaning, and type handling
- Distributions for BMI, age, sleep, stress, and lifestyle categories
- BMI category creation and weight-status profiling
- Smoking, exercise, diet, and alcohol pattern analysis
- Correlation analysis across numeric variables
- Chronic disease rates by smoking status, BMI category, and other segments
- Construction of a Lifestyle Risk Score and risk personas

### 2. Feature engineering
- `BMI_Category` (Underweight / Normal / Overweight / Obese)
- Risk components: `risk_bmi`, `risk_smoker`, `risk_exercise`, `risk_diet`, `risk_sleep`
- `Lifestyle_Risk_Score` (sum of the 5 components, 0–10 scale)
- `Risk_Group` (Low / Medium / High)
- `Sleep_Band` (≤5, 5–6, 6–7, 7–8, 8–10, >10 hours)
- `Persona` labels (e.g. "Low-risk, active", "High-risk lifestyle")

These transformations are implemented in the notebook and reused in `app.py`.

### 3. Streamlit dashboard (`app.py`)

- **Home** — project summary, live dataset stats, top-insights narrative, tech stack table
- **Overview** — filtered dataset preview, KPI tiles, BMI vs. exercise boxplots, stress by sleep band
- **Risk Analysis** — chronic disease % by Risk Group / Sleep Band / BMI Category, persona summary table
- **What-if Explorer** — interactive sliders for a hypothetical person; computes BMI category, risk components, and Lifestyle Risk Score live, with an optional model-based probability if a trained model file is present

## Key Insights

- Baseline chronic disease prevalence is 19.3%, with ~1,230 individuals (16.4%) flagged high-risk.
- The 5-factor Lifestyle Risk Score cleanly separates Low/Medium/High tiers, with rising chronic disease rates across tiers.
- High-risk individuals average a BMI of ~30.3 vs. ~23.2 for low-risk, making weight a clear intervention target.
- Population averages (BMI ~26.0, sleep ~7 hours, risk score ~3.9/10) suggest a generally healthy sample with a meaningful at-risk minority.
- Higher exercise frequency shifts BMI toward healthier ranges for both smokers and non-smokers, though with substantial overlap.
- Chronic disease rates are flat across sleep bands, but stress follows a U-shape — higher at both short (<6h) and long (>10h) sleep durations.

## How to Run Locally

```bash
git clone https://github.com/lucifer0096/data-portfolio.git
cd "data-portfolio/Health and Lifestyle Analysis"
pip install -r requirements.txt
streamlit run app.py
```

Optionally, open `Project.ipynb` to review the full EDA.

## Future Improvements

- Train and persist a proper ML classifier (logistic regression or gradient boosting) for the What-if tab.
- Add more filters (diet quality, exercise level, BMI category) and cohort comparisons.
- Log user interactions to understand how people explore risk factors.
