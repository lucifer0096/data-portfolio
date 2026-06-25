import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="NZ Analyst Jobs Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = Path("data/gold/analyst_roles.parquet")
DATASET_URL = "https://openjobdata.com"
DOCS_URL = "https://openjobdata.com/documentation"


def inject_custom_css():
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                max-width: 1280px;
            }

            .hero-card {
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 55%, #2563eb 100%);
                color: #f8fafc;
                padding: 2rem 2rem 1.8rem 2rem;
                border-radius: 22px;
                box-shadow: 0 14px 35px rgba(15, 23, 42, 0.22);
                margin-bottom: 1.25rem;
            }

            .hero-card h1 {
                margin: 0 0 0.55rem 0;
                font-size: 2.2rem;
                line-height: 1.12;
                letter-spacing: -0.02em;
                color: #ffffff;
            }

            .hero-card p {
                margin: 0.35rem 0;
                font-size: 1rem;
                color: #dbeafe;
            }

            .section-card {
                background: rgba(30, 41, 59, 0.72);
                border: 1px solid rgba(148, 163, 184, 0.22);
                border-radius: 18px;
                padding: 1.1rem 1.15rem;
                box-shadow: 0 6px 18px rgba(15, 23, 42, 0.12);
                height: 100%;
                color: #e2e8f0;
            }

            .section-card p {
                color: #e2e8f0;
                margin-bottom: 0.75rem;
                line-height: 1.55;
            }

            .section-title {
                font-size: 1.1rem;
                font-weight: 700;
                margin-bottom: 0.7rem;
                color: #f8fafc;
            }

            .credit-box {
                background: rgba(30, 41, 59, 0.65);
                border: 1px solid rgba(148, 163, 184, 0.22);
                border-radius: 18px;
                padding: 1rem 1.1rem;
                margin-top: 1rem;
                color: #e2e8f0;
            }

            .credit-box a {
                color: #60a5fa !important;
            }

            .small-note {
                color: #cbd5e1;
                font-size: 0.95rem;
                line-height: 1.55;
            }

            div[data-testid="stMetric"] {
                background: rgba(15, 23, 42, 0.72);
                border: 1px solid rgba(148, 163, 184, 0.22);
                border-radius: 16px;
                padding: 0.65rem 0.85rem;
                box-shadow: 0 4px 14px rgba(15, 23, 42, 0.10);
            }

            div[data-testid="stMetricLabel"] {
                color: #cbd5e1 !important;
            }

            div[data-testid="stMetricValue"] {
                color: #f8fafc !important;
            }

            div[data-testid="stMetricDelta"] {
                color: #93c5fd !important;
            }

            .stAlert {
                border-radius: 14px;
            }

            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
            }

            .stTabs [data-baseweb="tab"] {
                border-radius: 10px;
                padding: 10px 16px;
            }

            .stDownloadButton button,
            .stButton button {
                border-radius: 10px;
                font-weight: 600;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)

    for col in ["Date Posted", "Date Closed"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    text_cols = [
        "Job Group",
        "Job Title",
        "Department",
        "Job Type",
        "Work Setup",
        "Remote",
        "Job Status",
        "Application Link",
    ]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str)

    return df


def sidebar_navigation():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Home", "Data Explorer"],
        index=0,
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("Credits")
    st.sidebar.markdown(f"[OpenJobData homepage]({DATASET_URL})")
    st.sidebar.markdown(f"[Dataset documentation]({DOCS_URL})")

    return page


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df.copy()

    st.sidebar.markdown("---")
    st.sidebar.subheader("Filters")

    search_text = st.sidebar.text_input("Search job title")

    posted_dates = (
        filtered["Date Posted"].dropna()
        if "Date Posted" in filtered.columns
        else pd.Series(dtype="datetime64[ns]")
    )

    if not posted_dates.empty:
        min_posted = posted_dates.min().date()
        max_posted = posted_dates.max().date()

        selected_range = st.sidebar.date_input(
            "Date posted range",
            value=(min_posted, max_posted),
            min_value=min_posted,
            max_value=max_posted,
            format="YYYY-MM-DD",
        )

        if isinstance(selected_range, tuple) and len(selected_range) == 2:
            start_date, end_date = selected_range
            filtered = filtered[
                filtered["Date Posted"].dt.date.between(start_date, end_date)
            ]

    job_groups = st.sidebar.multiselect(
        "Job Group",
        sorted([x for x in filtered["Job Group"].dropna().unique() if x])
    )

    job_types = st.sidebar.multiselect(
        "Job Type",
        sorted([x for x in filtered["Job Type"].dropna().unique() if x])
    )

    work_setups = st.sidebar.multiselect(
        "Work Setup",
        sorted([x for x in filtered["Work Setup"].dropna().unique() if x])
    )

    remote_values = st.sidebar.multiselect(
        "Remote",
        sorted([x for x in filtered["Remote"].dropna().unique() if x])
    )

    statuses_available = sorted([x for x in filtered["Job Status"].dropna().unique() if x])
    default_status = ["Active"] if "Active" in statuses_available else []

    statuses = st.sidebar.multiselect(
        "Job Status",
        statuses_available,
        default=default_status
    )

    if search_text:
        filtered = filtered[
            filtered["Job Title"].str.contains(search_text, case=False, na=False)
        ]

    if job_groups:
        filtered = filtered[filtered["Job Group"].isin(job_groups)]

    if job_types:
        filtered = filtered[filtered["Job Type"].isin(job_types)]

    if work_setups:
        filtered = filtered[filtered["Work Setup"].isin(work_setups)]

    if remote_values:
        filtered = filtered[filtered["Remote"].isin(remote_values)]

    if statuses:
        filtered = filtered[filtered["Job Status"].isin(statuses)]

    sort_option = st.sidebar.selectbox(
        "Sort by",
        [
            "Newest posted",
            "Oldest posted",
            "Recently closed",
            "Job title A-Z",
        ]
    )

    if sort_option == "Newest posted":
        filtered = filtered.sort_values("Date Posted", ascending=False, na_position="last")
    elif sort_option == "Oldest posted":
        filtered = filtered.sort_values("Date Posted", ascending=True, na_position="last")
    elif sort_option == "Recently closed":
        filtered = filtered.sort_values("Date Closed", ascending=False, na_position="last")
    elif sort_option == "Job title A-Z":
        filtered = filtered.sort_values("Job Title", ascending=True, na_position="last")

    return filtered.reset_index(drop=True)


def build_metrics(df: pd.DataFrame):
    total_jobs = len(df)
    active_jobs = int((df["Job Status"] == "Active").sum()) if "Job Status" in df.columns else 0
    closed_jobs = int((df["Job Status"] == "Closed").sum()) if "Job Status" in df.columns else 0
    latest_posted = df["Date Posted"].max() if "Date Posted" in df.columns and not df.empty else pd.NaT

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Jobs shown", total_jobs)
    c2.metric("Active jobs", active_jobs)
    c3.metric("Closed jobs", closed_jobs)
    c4.metric(
        "Last Data Pull Date",
        latest_posted.strftime("%Y-%m-%d") if pd.notna(latest_posted) else "N/A"
    )


def jobs_by_group_chart(df: pd.DataFrame):
    if df.empty:
        st.warning("No data available for Job Group chart.")
        return

    chart_df = (
        df[df["Job Group"].astype(str).str.strip() != ""]
        .groupby("Job Group", dropna=False)
        .size()
        .reset_index(name="Jobs")
        .sort_values("Jobs", ascending=False)
    )

    if chart_df.empty:
        st.warning("No Job Group values available.")
        return

    st.bar_chart(chart_df, x="Job Group", y="Jobs", use_container_width=True)


def status_chart(df: pd.DataFrame):
    if df.empty:
        st.warning("No data available for status chart.")
        return

    chart_df = (
        df[df["Job Status"].astype(str).str.strip() != ""]
        .groupby("Job Status", dropna=False)
        .size()
        .reset_index(name="Jobs")
        .sort_values("Jobs", ascending=False)
    )

    if chart_df.empty:
        st.warning("No Job Status values available.")
        return

    st.bar_chart(chart_df, x="Job Status", y="Jobs", use_container_width=True)


def postings_over_time_chart(df: pd.DataFrame):
    if df.empty or "Date Posted" not in df.columns:
        st.warning("No posting date data available.")
        return

    temp = df.dropna(subset=["Date Posted"]).copy()
    if temp.empty:
        st.warning("No posting date data available.")
        return

    temp["Posted Day"] = temp["Date Posted"].dt.date
    chart_df = (
        temp.groupby("Posted Day")
        .size()
        .reset_index(name="Jobs")
        .sort_values("Posted Day")
    )

    st.line_chart(chart_df, x="Posted Day", y="Jobs", use_container_width=True)


def work_setup_chart(df: pd.DataFrame):
    if df.empty:
        st.warning("No data available for Work Setup chart.")
        return

    chart_df = (
        df[df["Work Setup"].astype(str).str.strip() != ""]
        .groupby("Work Setup", dropna=False)
        .size()
        .reset_index(name="Jobs")
        .sort_values("Jobs", ascending=False)
    )

    if chart_df.empty:
        st.warning("No Work Setup values available.")
        return

    st.bar_chart(chart_df, x="Work Setup", y="Jobs", use_container_width=True)


def render_home(df: pd.DataFrame):
    total_jobs = len(df)
    active_jobs = int((df["Job Status"] == "Active").sum()) if "Job Status" in df.columns else 0
    closed_jobs = int((df["Job Status"] == "Closed").sum()) if "Job Status" in df.columns else 0
    latest_posted = df["Date Posted"].max() if "Date Posted" in df.columns and not df.empty else pd.NaT

    st.markdown(
        """
        <div class="hero-card">
            <h1>NZ Analyst Jobs Explorer</h1>
            <p>A simple analytics app for browsing analyst, analytics, BI, reporting, and data-related jobs in New Zealand.</p>
            <p>Use the Data Explorer page to filter postings, review trends, and open application links.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total roles", total_jobs)
    c2.metric("Active roles", active_jobs)
    c3.metric("Closed roles", closed_jobs)
    c4.metric(
        "Last Data Pull Date",
        latest_posted.strftime("%Y-%m-%d") if pd.notna(latest_posted) else "N/A"
    )

    col1, col2 = st.columns([1.15, 1])

    with col1:
        st.markdown('<div class="section-title">About the app</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="section-card">
                <p>This app is built to make analyst-related job data easier to browse for non-technical users.</p>
                <p>It focuses on plain-English fields such as Job Group, Job Title, Job Type, Work Setup, Job Status, posting dates, and direct application links.</p>
                <p>Job Group is inferred from role titles, so it helps with quick browsing but should not be treated as a perfect classification.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown('<div class="section-title">How to use</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="section-card">
                <p>1. Go to <b>Data Explorer</b> from the sidebar.</p>
                <p>2. Filter by date posted, job group, job type, work setup, remote status, or job status.</p>
                <p>3. Review charts for quick patterns and use the job table to open role links.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="credit-box">
            <div class="section-title">Credits and source</div>
            <p class="small-note">
                Dataset source: <a href="{DATASET_URL}" target="_blank">OpenJobData</a><br>
                Documentation: <a href="{DOCS_URL}" target="_blank">OpenJobData Documentation</a>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_explorer(df: pd.DataFrame):
    st.markdown(
        """
        <div class="hero-card">
            <h1>Data Explorer</h1>
            <p>Filter the dataset, review quick job-market patterns, and inspect the cleaned analyst roles table.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    filtered = apply_filters(df)
    build_metrics(filtered)

    st.info(
        "Job Group is a broad label based on words found in the job title. "
        "Use it as a quick guide rather than a perfect classification."
    )

    tab1, tab2 = st.tabs(["Overview", "Job Table"])

    with tab1:
        left, right = st.columns(2)
        with left:
            st.subheader("Jobs by group")
            jobs_by_group_chart(filtered)

        with right:
            st.subheader("Jobs by status")
            status_chart(filtered)

        left2, right2 = st.columns(2)
        with left2:
            st.subheader("Postings over time")
            postings_over_time_chart(filtered)

        with right2:
            st.subheader("Jobs by work setup")
            work_setup_chart(filtered)

    with tab2:
        display_cols = [
            "Job Group",
            "Job Title",
            "Department",
            "Job Type",
            "Work Setup",
            "Remote",
            "Date Posted",
            "Date Closed",
            "Job Status",
            "Application Link",
        ]

        available_cols = [c for c in display_cols if c in filtered.columns]

        st.subheader("Job table")

        st.dataframe(
            filtered[available_cols],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Job Group": st.column_config.TextColumn("Job Group", width="medium"),
                "Job Title": st.column_config.TextColumn("Job Title", width="large"),
                "Department": st.column_config.TextColumn("Department", width="medium"),
                "Job Type": st.column_config.TextColumn("Job Type", width="small"),
                "Work Setup": st.column_config.TextColumn("Work Setup", width="small"),
                "Remote": st.column_config.TextColumn("Remote", width="small"),
                "Date Posted": st.column_config.DatetimeColumn(
                    "Date Posted",
                    format="YYYY-MM-DD HH:mm"
                ),
                "Date Closed": st.column_config.DatetimeColumn(
                    "Date Closed",
                    format="YYYY-MM-DD HH:mm"
                ),
                "Job Status": st.column_config.TextColumn("Job Status", width="small"),
                "Application Link": st.column_config.LinkColumn(
                    "Application Link",
                    display_text="Open job",
                    width="medium"
                ),
            },
        )

        csv_data = filtered[available_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download filtered jobs as CSV",
            data=csv_data,
            file_name="analyst_jobs_filtered.csv",
            mime="text/csv"
        )

    st.markdown(
        f"""
        <div class="credit-box">
            <div class="section-title">Dataset and credits</div>
            <p class="small-note">
                This app uses job-listing data from <a href="{DATASET_URL}" target="_blank">OpenJobData</a>.<br>
                For setup and schema details, see the <a href="{DOCS_URL}" target="_blank">official documentation</a>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    inject_custom_css()

    if not DATA_PATH.exists():
        st.error(f"Data file not found: {DATA_PATH}")
        st.stop()

    df = load_data(DATA_PATH)

    if df.empty:
        st.warning("No data available.")
        st.stop()

    page = sidebar_navigation()

    if page == "Home":
        render_home(df)
    else:
        render_explorer(df)


if __name__ == "__main__":
    main()