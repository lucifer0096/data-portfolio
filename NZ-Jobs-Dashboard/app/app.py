import pandas as pd
import streamlit as st
from pathlib import Path
from build_info import LAST_SYNC

st.set_page_config(
    page_title="NZ Analyst Jobs Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
DATA_PATH = PROJECT_DIR / "data" / "gold" / "analyst_roles.parquet"
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

            .stAlert {
                border-radius: 14px;
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


def format_file_timestamp(file_mtime: float) -> str:
    return (
        pd.to_datetime(file_mtime, unit="s", utc=True)
        .tz_convert("Pacific/Auckland")
        .strftime("%Y-%m-%d %H:%M NZ")
    )


@st.cache_data
def load_data(path_str: str, file_mtime: float) -> pd.DataFrame:
    _ = file_mtime
    df = pd.read_parquet(path_str)

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
    page = st.sidebar.radio("Go to", ["Home", "Data Explorer"], index=0)

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
        if "Job Group" in filtered.columns
        else [],
    )

    job_types = st.sidebar.multiselect(
        "Job Type",
        sorted([x for x in filtered["Job Type"].dropna().unique() if x])
        if "Job Type" in filtered.columns
        else [],
    )

    work_setups = st.sidebar.multiselect(
        "Work Setup",
        sorted([x for x in filtered["Work Setup"].dropna().unique() if x])
        if "Work Setup" in filtered.columns
        else [],
    )

    remote_values = st.sidebar.multiselect(
        "Remote",
        sorted([x for x in filtered["Remote"].dropna().unique() if x])
        if "Remote" in filtered.columns
        else [],
    )

    statuses_available = (
        sorted([x for x in filtered["Job Status"].dropna().unique() if x])
        if "Job Status" in filtered.columns
        else []
    )
    default_status = ["Active"] if "Active" in statuses_available else []

    statuses = st.sidebar.multiselect(
        "Job Status",
        statuses_available,
        default=default_status,
    )

    if search_text and "Job Title" in filtered.columns:
        filtered = filtered[
            filtered["Job Title"].str.contains(search_text, case=False, na=False)
        ]

    if job_groups and "Job Group" in filtered.columns:
        filtered = filtered[filtered["Job Group"].isin(job_groups)]

    if job_types and "Job Type" in filtered.columns:
        filtered = filtered[filtered["Job Type"].isin(job_types)]

    if work_setups and "Work Setup" in filtered.columns:
        filtered = filtered[filtered["Work Setup"].isin(work_setups)]

    if remote_values and "Remote" in filtered.columns:
        filtered = filtered[filtered["Remote"].isin(remote_values)]

    if statuses and "Job Status" in filtered.columns:
        filtered = filtered[filtered["Job Status"].isin(statuses)]

    sort_option = st.sidebar.selectbox(
        "Sort by",
        ["Newest posted", "Oldest posted", "Recently closed", "Job title A-Z"],
    )

    if sort_option == "Newest posted" and "Date Posted" in filtered.columns:
        filtered = filtered.sort_values("Date Posted", ascending=False, na_position="last")
    elif sort_option == "Oldest posted" and "Date Posted" in filtered.columns:
        filtered = filtered.sort_values("Date Posted", ascending=True, na_position="last")
    elif sort_option == "Recently closed" and "Date Closed" in filtered.columns:
        filtered = filtered.sort_values("Date Closed", ascending=False, na_position="last")
    elif sort_option == "Job title A-Z" and "Job Title" in filtered.columns:
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
        "Latest Job Posted",
        latest_posted.strftime("%Y-%m-%d") if pd.notna(latest_posted) else "N/A",
    )


def jobs_by_group_chart(df: pd.DataFrame):
    if df.empty or "Job Group" not in df.columns:
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
    if df.empty or "Job Status" not in df.columns:
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
    if df.empty or "Work Setup" not in df.columns:
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


def render_sync_debug(file_updated_text: str):
    st.caption(f"Data file updated: {file_updated_text}")
    st.caption(f"Workflow sync marker: {LAST_SYNC}")


def render_home(df: pd.DataFrame, file_updated_text: str):
    st.markdown(
        """
        <div class="hero-card">
            <h1>NZ Analyst Jobs Explorer</h1>
            <p>Browse analyst, analytics, BI, reporting, and related roles in New Zealand.</p>
            <p class="small-note">The app now shows the real parquet file update time and the workflow sync marker so you can verify GitHub refreshes more easily.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    build_metrics(df)
    render_sync_debug(file_updated_text)

    left, right = st.columns(2)
    with left:
        st.subheader("Jobs by group")
        jobs_by_group_chart(df)

    with right:
        st.subheader("Status mix")
        status_chart(df)

    left, right = st.columns(2)
    with left:
        st.subheader("Postings over time")
        postings_over_time_chart(df)

    with right:
        st.subheader("Work setup")
        work_setup_chart(df)


def render_data_explorer(df: pd.DataFrame, file_updated_text: str):
    st.title("Data Explorer")
    build_metrics(df)
    render_sync_debug(file_updated_text)

    if df.empty:
        st.warning("No jobs match the selected filters.")
        return

    left, right = st.columns(2)
    with left:
        st.subheader("Jobs by group")
        jobs_by_group_chart(df)

    with right:
        st.subheader("Status mix")
        status_chart(df)

    display_df = df.copy()

    st.subheader("Job table")
    if "Application Link" in display_df.columns:
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Application Link": st.column_config.LinkColumn("Application Link")
            },
        )
    else:
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    csv_data = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered data as CSV",
        data=csv_data,
        file_name="nz_analyst_jobs_filtered.csv",
        mime="text/csv",
    )


def main():
    inject_custom_css()
    page = sidebar_navigation()

    if not DATA_PATH.exists():
        st.error(f"Data file not found: {DATA_PATH}")
        st.stop()

    data_mtime = DATA_PATH.stat().st_mtime
    file_updated_text = format_file_timestamp(data_mtime)

    df = load_data(str(DATA_PATH), data_mtime)
    filtered_df = apply_filters(df)

    if page == "Home":
        render_home(filtered_df, file_updated_text)
    else:
        render_data_explorer(filtered_df, file_updated_text)


if __name__ == "__main__":
    main()
