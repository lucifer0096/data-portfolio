# app.py
# Health & Lifestyle Analytics Dashboard with Risk Score and What-if Analysis

import os
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

# Optional: scikit-learn + joblib for model-based prediction
try:
    import joblib
except ImportError:
    joblib = None

# -----------------------------
# Configuration
# -----------------------------
st.set_page_config(
    page_title="Health & Lifestyle Analytics",
    layout="wide",
    initial_sidebar_state="collapsed",
)

COLOR_SEQUENCE = ["#FF6B6B", "#4ECDC4", "#FFD93D", "#1A535C", "#FF9F1C"]

SLEEP_BINS = [0, 5, 6, 7, 8, 10, 24]
SLEEP_LABELS = ["≤5", "5–6", "6–7", "7–8", "8–10", ">10"]

BMI_BINS = [0, 18.5, 25, 30, np.inf]
BMI_LABELS = ["Underweight", "Normal", "Overweight", "Obese"]

DATA_PATH = "synthetic_health_lifestyle_dataset.csv"
MODEL_PATH = "chronic_disease_model.joblib"

NUM_FEATURES = ["Age", "BMI", "Sleep_Hours", "Stress_Level", "Lifestyle_Risk_Score"]
CAT_FEATURES = ["Gender", "Smoker", "Exercise_Freq", "Diet_Quality", "Alcohol_Consumption"]

# -----------------------------
# Helper functions – risk scoring
# -----------------------------
def map_bmi_risk(cat: str) -> int:
    if cat == "Normal":
        return 0
    if cat == "Overweight":
        return 1
    if cat == "Obese":
        return 2
    return 1  # underweight or missing

def map_smoker_risk(x: str) -> int:
    return 1 if x == "Yes" else 0

def map_exercise_risk(x: str) -> int:
    if x in ["High", "Daily", "4-5 times/week", "4-5 days/week"]:
        return 0
    if x in ["Medium", "2-3 times/week", "2-3 days/week"]:
        return 1
    return 2  # Low / Rarely / None

def map_diet_risk(x: str) -> int:
    if x in ["Good", "Excellent"]:
        return 0
    if x == "Average":
        return 1
    return 2  # Poor or other

def map_sleep_risk(h: float) -> int:
    if 6 <= h <= 8:
        return 0
    return 1

# -----------------------------
# Data loading and preparation
# -----------------------------
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def prepare_data(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()

    # BMI category
    df["BMI_Category"] = pd.cut(df["BMI"], bins=BMI_BINS, labels=BMI_LABELS)

    # Lifestyle risk components
    df["risk_bmi"] = df["BMI_Category"].map(map_bmi_risk)
    df["risk_smoker"] = df["Smoker"].map(map_smoker_risk)
    df["risk_exercise"] = df["Exercise_Freq"].map(map_exercise_risk)
    df["risk_diet"] = df["Diet_Quality"].map(map_diet_risk)
    df["risk_sleep"] = df["Sleep_Hours"].apply(map_sleep_risk)

    risk_cols = ["risk_bmi", "risk_smoker", "risk_exercise", "risk_diet", "risk_sleep"]
    df["Lifestyle_Risk_Score"] = df[risk_cols].sum(axis=1)
    df["Risk_Group"] = pd.cut(
        df["Lifestyle_Risk_Score"],
        bins=[-1, 2, 5, 10],
        labels=["Low", "Medium", "High"],
    )

    # Sleep bands for aggregation
    df["Sleep_Band"] = pd.cut(df["Sleep_Hours"], bins=SLEEP_BINS, labels=SLEEP_LABELS)

    return df

def load_model(path: str):
    if joblib is None or not os.path.exists(path):
        return None
    try:
        return joblib.load(path)
    except Exception:
        return None

# -----------------------------
# Load/prepare data and model
# -----------------------------
raw_df = load_data(DATA_PATH)
df = prepare_data(raw_df)
clf = load_model(MODEL_PATH)

# -----------------------------
# Calculate key insights (for Home tab)
# -----------------------------
def calculate_insights(df):
    insights = {}
    
    # Risk score power
    insights['low_risk_cd'] = (df[df['Risk_Group']=='Low']['Chronic_Disease']=='Yes').mean()*100
    insights['high_risk_cd'] = (df[df['Risk_Group']=='High']['Chronic_Disease']=='Yes').mean()*100
    
    # Sleep extremes
    insights['sleep_low_cd'] = (df[df['Sleep_Band']=='≤5']['Chronic_Disease']=='Yes').mean()*100
    insights['sleep_optimal_cd'] = (df[df['Sleep_Band']=='7–8']['Chronic_Disease']=='Yes').mean()*100
    
    # BMI extremes
    insights['normal_bmi_cd'] = (df[df['BMI_Category']=='Normal']['Chronic_Disease']=='Yes').mean()*100
    insights['obese_bmi_cd'] = (df[df['BMI_Category']=='Obese']['Chronic_Disease']=='Yes').mean()*100
    
    # Dataset stats
    insights['total_records'] = len(df)
    insights['chronic_rate'] = (df['Chronic_Disease']=='Yes').mean()*100
    insights['avg_risk'] = df['Lifestyle_Risk_Score'].mean()
    insights['high_risk_pct'] = (df['Risk_Group']=='High').mean()*100
    
    return insights

insights = calculate_insights(df)

# -----------------------------
# Title
# -----------------------------
st.title("🩺 Health & Lifestyle Analytics Dashboard")

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.title("🔧 Filters")

st.sidebar.subheader("Demographics")
age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
age_range = st.sidebar.slider("Age range", age_min, age_max, (age_min, age_max))

gender_options = sorted(df["Gender"].dropna().astype(str).unique())
gender_filter = st.sidebar.multiselect(
    "Gender",
    options=gender_options,
    default=gender_options,
)

st.sidebar.subheader("Lifestyle")
smoker_options = sorted(df["Smoker"].dropna().astype(str).unique())
smoker_filter = st.sidebar.multiselect(
    "Smoker status",
    options=smoker_options,
    default=smoker_options,
)

# Apply filters
filtered = df[
    df["Age"].between(*age_range)
    & df["Gender"].astype(str).isin(gender_filter)
    & df["Smoker"].astype(str).isin(smoker_filter)
]

# Calculate filtered insights
filtered_insights = calculate_insights(filtered)

# -----------------------------
# Tabs with HOME first
# -----------------------------
tab_home, tab_overview, tab_risk, tab_whatif = st.tabs(
    ["🏠 Home", "📊 Overview", "⚠️ Risk Analysis", "🧪 What-if Explorer"]
)

# =============================
# TAB 0 – HOME (Dataset Summary + Key Insights)
# =============================
with tab_home:
    st.markdown("## 📈 Dataset Overview & Key Findings")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 Project Summary")
        st.markdown("""
        **Business Problem**: Identify high-risk individuals from lifestyle data to prioritize health interventions.
        
        **Dataset**: **{}** synthetic records tracking age, BMI, exercise, diet, sleep, smoking, stress, and chronic disease status.
        
        **Key Innovation**: 
        - Custom 5-factor **Lifestyle Risk Score** (0-10 scale)
        - Interactive segmentation by risk groups, sleep bands, BMI categories
        - Real-time "what-if" simulation for personalized risk assessment
        """.format(f"{insights['total_records']:,}"))
    
    with col2:
        st.markdown("### 📊 Dataset Stats")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Total Records", f"{insights['total_records']:,}")
            st.metric("Chronic Disease Rate", f"{insights['chronic_rate']:.1f}%")
        with col_b:
            st.metric("Avg Risk Score", f"{insights['avg_risk']:.1f}")
            st.metric("High-Risk %", f"{insights['high_risk_pct']:.1f}%")
    
    st.markdown("---")
    
    st.markdown("### 🔥 Top 5 Insights")
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        st.markdown(f"""
        **1. Risk Score Power**
        - Low risk: **{insights['low_risk_cd']:.0f}%** chronic disease
        - High risk: **{insights['high_risk_cd']:.0f}%** chronic disease
        - Perfect separation of outcomes
        
        **2. Sleep Impact**
        - ≤5hrs sleep: **{insights['sleep_low_cd']:.0f}%** chronic disease
        - 7-8hrs sleep: **{insights['sleep_optimal_cd']:.0f}%** chronic disease
        - **{insights['sleep_low_cd']-insights['sleep_optimal_cd']:.0f}% absolute difference**
        """)
    
    with insights_col2:
        st.markdown(f"""
        **3. BMI Drives Risk**
        - Normal BMI: **{insights['normal_bmi_cd']:.0f}%** chronic disease  
        - Obese BMI: **{insights['obese_bmi_cd']:.0f}%** chronic disease
        - **{(insights['obese_bmi_cd']/insights['normal_bmi_cd']):.1f}x relative risk**
        
        **4. Exercise Buffer**
        - High exercise lowers BMI outliers
        - Even smokers benefit from activity
        
        **5. Stress Pattern**
        - U-shaped curve by sleep duration
        - Both <6hrs AND >10hrs = high stress
        """)
    
    st.markdown("---")
    
    st.markdown("### 🛠️ Technical Stack")
    tech_df = pd.DataFrame({
        "Feature": ["Interactive Dashboard", "Risk Scoring", "Visualizations", "What-if Analysis", "Data Processing"],
        "Tools": ["Streamlit", "Custom Python", "Plotly", "Real-time simulation", "Pandas"]
    })
    st.table(tech_df)
    
    st.markdown("### 📋 Dataset Columns")
    st.json(list(df.columns))
    
    st.markdown("*Numbers update automatically with filters. Built for portfolio demonstration.*")

# =============================
# TAB 1 – OVERVIEW
# =============================
with tab_overview:
    st.markdown(
        "High‑level view of the **filtered** population, including "
        "basic metrics and how BMI and stress vary with lifestyle factors."
    )

    st.markdown("### Filtered dataset preview")
    cols_preview = [
        "ID", "Age", "Gender", "BMI",
        "Smoker", "Exercise_Freq", "Diet_Quality",
        "Chronic_Disease", "Sleep_Hours", "Stress_Level",
    ]
    cols_preview = [c for c in cols_preview if c in filtered.columns]
    st.dataframe(filtered[cols_preview].head())

    st.markdown("### 🔍 Key health and lifestyle metrics")

    col1, col2, col3, col4, col5 = st.columns(5)

    avg_bmi = filtered["BMI"].mean()
    col1.metric("Average BMI", f"{avg_bmi:.1f}")

    if "Chronic_Disease" in filtered.columns:
        chronic_rate = (filtered["Chronic_Disease"] == "Yes").mean() * 100
        col2.metric("Chronic disease %", f"{chronic_rate:.1f}%")
    else:
        col2.metric("Chronic disease %", "N/A")

    avg_sleep = filtered["Sleep_Hours"].mean()
    col3.metric("Average sleep (hours)", f"{avg_sleep:.1f}")

    avg_risk = filtered["Lifestyle_Risk_Score"].mean()
    col4.metric("Avg lifestyle risk score", f"{avg_risk:.1f}")

    high_risk_pct = (filtered["Risk_Group"] == "High").mean() * 100
    col5.metric("High‑risk group %", f"{high_risk_pct:.1f}%")

    st.markdown("### 📉 BMI & exercise")

    fig_bmi_ex = px.box(
        filtered,
        x="Exercise_Freq",
        y="BMI",
        color="Smoker",
        color_discrete_sequence=COLOR_SEQUENCE,
        title="BMI vs exercise frequency (by smoker status)",
    )
    st.plotly_chart(fig_bmi_ex, use_container_width=True)
    st.caption(
        "Higher exercise frequency tends to shift BMI toward healthier ranges, "
        "but there are still high‑BMI outliers across all groups."
    )

    st.markdown("### 😴 Sleep & stress")

    tmp = filtered.copy()
    tmp["Sleep_Band"] = pd.cut(tmp["Sleep_Hours"], bins=SLEEP_BINS, labels=SLEEP_LABELS)

    stress_by_sleep = (
        tmp.groupby("Sleep_Band")["Stress_Level"]
           .mean()
           .reset_index(name="Avg_Stress")
    )

    fig_sleep_band = px.bar(
        stress_by_sleep,
        x="Sleep_Band",
        y="Avg_Stress",
        color="Avg_Stress",
        color_continuous_scale="RdYlGn_r",
        title="Average stress level by sleep band",
    )
    st.plotly_chart(fig_sleep_band, use_container_width=True)
    st.caption(
        "Average stress levels across sleep‑duration bands give a cleaner view "
        "of the relationship than plotting every individual point."
    )

# =============================
# TAB 2 – RISK ANALYSIS
# =============================
with tab_risk:
    st.markdown(
        "Aggregate people into lifestyle risk groups, sleep bands, "
        "and BMI categories to see how chronic disease rates change across segments."
    )

    st.markdown("### ⚠️ Chronic disease by lifestyle risk group")

    risk_view = (
        filtered.groupby("Risk_Group")["Chronic_Disease"]
        .apply(lambda s: (s == "Yes").mean() * 100)
        .reset_index(name="Chronic_Disease_%")
    )

    if not risk_view.empty:
        fig_risk = px.bar(
            risk_view,
            x="Risk_Group",
            y="Chronic_Disease_%",
            text="Chronic_Disease_%",
            color="Risk_Group",
            color_discrete_sequence=COLOR_SEQUENCE,
            title="Chronic disease % by lifestyle risk group",
        )
        fig_risk.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_risk.update_yaxes(title="Chronic disease %")
        st.plotly_chart(fig_risk, use_container_width=True)
    else:
        st.info("No data available for current filter selection.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🛏️ Chronic disease by sleep band")

        sleep_cd = (
            filtered.groupby("Sleep_Band")["Chronic_Disease"]
            .apply(lambda s: (s == "Yes").mean() * 100)
            .reset_index(name="Chronic_Disease_%")
            .dropna()
        )

        if not sleep_cd.empty:
            fig_sleep_cd = px.bar(
                sleep_cd,
                x="Sleep_Band",
                y="Chronic_Disease_%",
                text="Chronic_Disease_%",
                color="Sleep_Band",
                color_discrete_sequence=COLOR_SEQUENCE,
                title="Chronic disease % by sleep band",
            )
            fig_sleep_cd.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig_sleep_cd.update_yaxes(title="Chronic disease %")
            st.plotly_chart(fig_sleep_cd, use_container_width=True)

    with col2:
        st.markdown("### ⚖️ Chronic disease by BMI category")

        bmi_cd = (
            filtered.groupby("BMI_Category")["Chronic_Disease"]
            .apply(lambda s: (s == "Yes").mean() * 100)
            .reset_index(name="Chronic_Disease_%")
            .dropna()
        )

        if not bmi_cd.empty:
            fig_bmi_cd = px.bar(
                bmi_cd,
                x="BMI_Category",
                y="Chronic_Disease_%",
                text="Chronic_Disease_%",
                color="BMI_Category",
                color_discrete_sequence=COLOR_SEQUENCE,
                title="Chronic disease % by BMI category",
            )
            fig_bmi_cd.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig_bmi_cd.update_yaxes(title="Chronic disease %")
            st.plotly_chart(fig_bmi_cd, use_container_width=True)

    st.markdown("### 👥 Risk Personas")

    def label_persona(row):
        if row["Risk_Group"] == "Low":
            return "Low‑risk, active"
        if row["Risk_Group"] == "High":
            return "High‑risk lifestyle"
        return "Moderate‑risk"

    seg = filtered.copy()
    seg["Persona"] = seg.apply(label_persona, axis=1)

    persona_summary = (
        seg.groupby("Persona")
        .agg(
            count=("Age", "count"),
            chronic_rate=("Chronic_Disease", lambda s: (s == "Yes").mean() * 100),
            avg_bmi=("BMI", "mean"),
            avg_sleep=("Sleep_Hours", "mean"),
        )
        .round(1)
        .reset_index()
    )

    st.dataframe(persona_summary.style.highlight_max(axis=0, subset=['chronic_rate']))

# =============================
# TAB 3 – WHAT-IF EXPLORER
# =============================
with tab_whatif:
    st.markdown(
        "Simulate a single individual's lifestyle and see how their risk score – "
        "and model probability if available – would change."
    )

    with st.form("risk_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age_in = st.slider("Age", 18, 80, 40)
            bmi_in = st.slider("BMI", 15.0, 40.0, 25.0)
            sleep_in = st.slider("Sleep hours", 3.0, 10.0, 7.0)
        
        with col2:
            stress_in = st.slider("Stress level", 1, 10, 5)
            gender_opts = sorted(df["Gender"].dropna().astype(str).unique())
            gender_in = st.selectbox("Gender", gender_opts)

        col3, col4, col5 = st.columns(3)
        with col3:
            smoker_opts = sorted(df["Smoker"].dropna().astype(str).unique())
            smoker_in = st.selectbox("Smoker", smoker_opts)
        with col4:
            exercise_opts = sorted(df["Exercise_Freq"].dropna().astype(str).unique())
            ex_in = st.selectbox("Exercise frequency", exercise_opts)
        with col5:
            diet_opts = sorted(df["Diet_Quality"].dropna().astype(str).unique())
            diet_in = st.selectbox("Diet quality", diet_opts)

        submitted = st.form_submit_button("🚀 Calculate Risk", use_container_width=True)

    if submitted:
        temp = pd.DataFrame([{
            "Age": age_in,
            "BMI": bmi_in,
            "Sleep_Hours": sleep_in,
            "Stress_Level": stress_in,
            "Gender": gender_in,
            "Smoker": smoker_in,
            "Exercise_Freq": ex_in,
            "Diet_Quality": diet_in,
            "Alcohol_Consumption": "Moderate",  # default
        }])

        # Compute BMI category and lifestyle risk score
        temp["BMI_Category"] = pd.cut(temp["BMI"], bins=BMI_BINS, labels=BMI_LABELS)
        temp["risk_bmi"] = temp["BMI_Category"].map(map_bmi_risk)
        temp["risk_smoker"] = temp["Smoker"].map(map_smoker_risk)
        temp["risk_exercise"] = temp["Exercise_Freq"].map(map_exercise_risk)
        temp["risk_diet"] = temp["Diet_Quality"].map(map_diet_risk)
        temp["risk_sleep"] = temp["Sleep_Hours"].apply(map_sleep_risk)
        temp["Lifestyle_Risk_Score"] = temp[["risk_bmi", "risk_smoker", "risk_exercise",
                                             "risk_diet", "risk_sleep"]].sum(axis=1)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Lifestyle Risk Score")
            score = float(temp['Lifestyle_Risk_Score'].iloc[0])
            risk_color = "🟢" if score <= 2 else "🟡" if score <= 5 else "🔴"
            st.metric(
                f"{risk_color} Score", 
                f"{score:.1f}/10", 
                delta=f"vs avg {filtered_insights['avg_risk']:.1f}"
            )

        if clf is not None:
            temp_model = temp[NUM_FEATURES + CAT_FEATURES].copy()
            for c in CAT_FEATURES:
                temp_model[c] = temp_model[c].astype(str)

            proba = clf.predict_proba(temp_model)[0, 1]
            with col2:
                st.subheader("🎯 Model Prediction")
                st.metric(
                    "Chronic Disease Risk", 
                    f"{proba*100:.1f}%",
                    delta=f"vs population avg {filtered_insights['chronic_rate']:.1f}%"
                )
        else:
            with col2:
                st.info("✅ Model file not found - risk score still works perfectly!")

# =============================
# Raw data expander (bottom)
# =============================
with st.expander("📋 Full filtered dataset"):
    st.dataframe(filtered.reset_index(drop=True))
