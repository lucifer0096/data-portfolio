# 🩺 Health & Lifestyle Analytics Dashboard

Interactive health & lifestyle risk dashboard built from a full exploratory data analysis (EDA) notebook and deployed as a Streamlit app.

---

## 🎯 Project goal

Identify and explore **high‑risk individuals** in a synthetic population of **7,500 adults** using lifestyle, BMI, sleep, stress, and chronic disease information. The project shows how to go from:

> Raw CSV → EDA in Jupyter → Feature engineering → Interactive Streamlit dashboard.

---

## 📊 Key dataset facts

- 7,500 synthetic patient records  
- 13 raw input fields (age, gender, BMI, smoking, exercise, diet, alcohol, sleep, stress, chronic disease, etc.)  
- 22 total features after engineering (e.g. BMI category, lifestyle risk components, risk group, sleep bands)  
- Overall chronic disease prevalence: **~19.3%**  
- High‑risk segment (by lifestyle risk score): **~16.4%** of the population  

---

## 🔍 Main insights

- **Chronic disease prevalence:** 19.3% baseline rate across 7,500 patients, with around 1,230 high‑risk individuals (16.4%) flagged for closer attention.  
- **Risk score segmentation:** A custom 5‑factor Lifestyle Risk Score (BMI, smoking, exercise, diet, sleep) creates Low‑, Medium‑, and High‑risk patient tiers with slightly higher chronic disease rates as risk increases.  
- **BMI and weight status:** The High‑risk group has a clearly higher average BMI (about 30.3) than the Low‑risk group (about 23.2), making excess weight a key intervention target.  
- **Population health profile:** Average BMI ~26.0, sleep ~7 hours, and risk score ~3.9/10 suggest a generally healthy sample with a meaningful at‑risk minority.  
- **Exercise and BMI:** Higher exercise frequency shifts BMI distributions toward healthier ranges for both smokers and non‑smokers, though there is still substantial overlap and many outliers.  
- **Sleep and stress:** Chronic disease rates are fairly flat across sleep bands, but stress displays a U‑shaped pattern, with higher stress at both short (<6 hours) and long (>10 hours) sleep durations.  

These insights are first derived in the notebook and then made explorable in the app.

---

## 🧱 Features & architecture

### 1. Exploratory data analysis (Jupyter)

The `Project.ipynb` notebook covers:

- Data loading, cleaning, and type handling  
- Distributions for key variables (BMI, age, sleep, stress, lifestyle categories)  
- BMI category creation and weight‑status profiling  
- Smoking, exercise, diet, and alcohol patterns  
- Correlations between numeric variables (BMI, age, stress, sleep)  
- Chronic disease rates by smoking status, BMI category, and other segments  
- Construction of a **Lifestyle Risk Score** and **risk personas**  

### 2. Feature engineering

Key engineered columns include:

- `BMI_Category` (Underweight / Normal / Overweight / Obese)  
- Risk components: `risk_bmi`, `risk_smoker`, `risk_exercise`, `risk_diet`, `risk_sleep`  
- `Lifestyle_Risk_Score` (sum of the 5 components, 0–10 scale)  
- `Risk_Group` (Low / Medium / High)  
- `Sleep_Band` (≤5, 5–6, 6–7, 7–8, 8–10, >10 hours)  
- `Persona` labels (e.g. “Low‑risk, active”, “High‑risk lifestyle”)  

These transformations are implemented both in the notebook and reused inside `app.py`.

### 3. Streamlit dashboard

The interactive app (`app.py`) exposes the analysis in four tabs:

- **🏠 Home**  
  - Project summary and business context  
  - Live dataset stats (record count, chronic disease %, average risk score, high‑risk %)  
  - “Top insights” narrative and technical stack table  

- **📊 Overview**  
  - Filtered dataset preview  
  - KPI tiles (average BMI, chronic disease %, avg sleep, avg risk score, high‑risk %)  
  - BMI vs exercise frequency (split by smoker) using boxplots  
  - Average stress level by sleep band  

- **⚠️ Risk Analysis**  
  - Chronic disease % by lifestyle Risk Group  
  - Chronic disease % by Sleep Band  
  - Chronic disease % by BMI Category  
  - Persona summary table (counts, chronic rate, average BMI, average sleep)  

- **🧪 What‑if Explorer**  
  - Sliders/selectors for age, BMI, sleep hours, stress level, gender, smoking, exercise, diet, etc.  
  - On submit, computes BMI category, risk components, and Lifestyle Risk Score for that hypothetical person  
  - Optionally, if a trained model file is present, displays a simple model‑based chronic disease probability  

---

## 🛠️ Tech stack

| Layer         | Tools / Libraries    |
|--------------|----------------------|
| EDA          | Python, Pandas, NumPy, Matplotlib/Seaborn (as relevant in the notebook) |
| Dashboard    | Streamlit, Plotly    |
| Feature eng. | Pandas               |
| Optional ML  | scikit‑learn, joblib |

---

## 🚀 How to run locally

1. **Clone the repository**  

2. **Create and activate a virtual environment (optional but recommended)**  

3. **Install dependencies**  

4. **Run the Streamlit app**  

5. **(Optional) Explore the notebook**  

---

## 📂 Repository structure

.
├── Project.ipynb # Full EDA and feature engineering
├── app.py # Streamlit dashboard
├── synthetic_health_lifestyle_dataset.csv
├── requirements.txt # Python dependencies
├── README.md # This file
└── /images or screenshots (optional)

---

## 💡 Possible extensions

- Train and persist a proper ML classifier (e.g. logistic regression, gradient boosting) for chronic disease prediction and plug it into the What‑if tab.  
- Add more filters (diet quality, exercise level, BMI category) and cohort comparisons.  
- Log interactions or selections to understand how users explore risk factors.  

This project is designed to showcase end‑to‑end data work: **EDA → feature engineering → risk scoring → interactive app**.
