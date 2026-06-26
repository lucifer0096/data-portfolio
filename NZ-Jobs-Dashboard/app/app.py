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
                padding-top: 1rem;
                padding-bottom: 1.5rem;
                max-width: 1280px;
            }

            .stApp [data-testid="stHeader"] {
                background: transparent;
            }

            div[data-testid="stMetric"] {
                border: 1px solid rgba(120, 120, 120, 0.18);
                border-radius: 14px;
                padding: 0.7rem 0.8rem;
                background: rgba(255, 255, 255, 0.02);
            }

            .meta-strip {
                border: 1px solid rgba(120, 120, 120, 0.18);
                border-radius: 14px;
                padding: 0.85rem 1rem;
                margin-top: 0.2rem;
                margin-bottom: 1rem;
                background: rgba(255, 255, 255, 0.02);
                font-size: 0.95rem;
            }

            .section-note {
                color: #94a3b8;
                font-size: 0.94rem;
                line-height: 1.5;
            }

            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
            }

            .stTabs [data-baseweb="tab"] {
                border-radius: 10px;
                padding: 10px 14px;
            }

            .stDownloadButton button,
            .stButton button,
            .stForm button {
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


def format_date(value) -> str:
    if pd.isna(value):
        return "N/A"
    return pd.to_datetime(value).strftime("%Y-%m-%d")


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


def render_sidebar_filters(df: pd.DataFrame) -> dict:
    st.sidebar.title("Filters")
    st.sidebar.caption("Default view shows active roles only.")

    with st.sidebar.form("filters_form"):
        search_text = st.text_input("Search job title")

        posted_dates = (
            df["Date Posted"].dropna()
            if "Date Posted" in df.columns
            else pd.Series(dtype="datetime64[ns]")
        )

        selected_range = None
        if not posted_dates.empty:
            min_posted = posted_dates.min().date()
            max_posted = posted_dates.max().date()
            selected_range = st.date_input(
                "Date posted range",
                value=(min_posted, max_posted),
                min_value=min_posted,
                max_value=max_posted,
                format="YYYY-MM-DD",
            )

        job_groups = st.multiselect(
            "Job Group",
            sorted([x for x in df["Job Group"].unique() if x]) if "Job Group" in df.columns else []
        )
        job_types = st.multiselect(
            "Job Type",
            sorted([x for x in df["Job Type"].unique() if x]) if "Job Type" in df.columns else []
        )
        work_setups = st.multiselect(
            "Work Setup",
            sorted([x for x in df["Work Setup"].unique() if x]) if "Work Setup" in df.columns else []
        )
        remote_values = st.multiselect(
            "Remote",
            sorted([x for x in df["Remote"].unique() if x]) if "Remote" in df.columns else []
        )

        statuses_available = (
            sorted([x for x in df["Job Status"].unique() if x]) if "Job Status" in df.columns else []
        )
        statuses = st.multiselect(
            "Job Status",
            statuses_available,
            default=["Active"] if "Active" in statuses_available else [],
        )

        sort_option = st.selectbox(
            "Sort by",
            ["Newest posted", "Oldest posted", "Recently closed", "Job title A-Z"],
        )

        submitted = st.form_submit_button("Apply filters", use_container_width=True)

    st.sidebar.markdown("---")
    st.sidebar.subheader("Source")
    st.sidebar.markdown(f"[OpenJobData]({DATASET_URL})")
    st.sidebar.markdown(f"[Documentation]({DOCS_URL})")

    return {
        "search_text": search_text,
        "selected_range": selected_range,
        "job_groups": job_groups,
        "job_types": job_types,
        "work_setups": work_setups,
        "remote_values": remote_values,
        "statuses": statuses,
        "sort_option": sort_option,
        "submitted": submitted,
    }


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    filtered = df.copy()

    selected_range = filters.get("selected_range")
    if isinstance(selected_range, tuple) and len(selected_range) == 2 and "Date Posted" in filtered.columns:
        start_date, end_date = selected_range
        filtered = filtered[
            filtered["Date Posted"].dt.date.between(start_date, end_date)
        ]

    search_text = filters.get("search_text")
    if search_text and "Job Title" in filtered.columns:
        filtered = filtered[
            filtered["Job Title"].str.contains(search_text, case=False, na=False)
        ]

    for col_name, selected_values in [
        ("Job Group", filters.get("job_groups")),
        ("Job Type", filters.get("job_types")),
        ("Work Setup", filters.get("work_setups")),
        ("Remote", filters.get("remote_values")),
        ("Job Status", filters.get("statuses")),
    ]:
        if selected_values and col_name in filtered.columns:
            filtered = filtered[filtered[col_name].isin(selected_values)]

    sort_option = filters.get("sort_option", "Newest posted")
    if sort_option == "Newest posted" and "Date Posted" in filtered.columns:
        filtered = filtered.sort_values("Date Posted", ascending=False, na_position="last")
    elif sort_option == "Oldest posted" and "Date Posted" in filtered.columns:
        filtered = filtered.sort_values("Date Posted", ascending=True, na_position="last")
    elif sort_option == "Recently closed" and "Date Closed" in filtered.columns:
        filtered = filtered.sort_values("Date Closed", ascending=False, na_position="last")
    elif sort_option == "Job title A-Z" and "Job Title" in filtered.columns:
        filtered = filtered.sort_values("Job Title", ascending=True, na_position="last")

    return filtered.reset_index(drop=True)


def metric_row(df: pd.DataFrame):
    total_jobs = len(df)
    active_jobs = int((df["Job Status"] == "Active").sum()) if "Job Status" in df.columns else 0
    closed_jobs = int((df["Job Status"] == "Closed").sum()) if "Job Status" in df.columns else 0
    latest_posted = df["Date Posted"].max() if "Date Posted" in df.columns and not df.empty else pd.NaT

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Filtered jobs", total_jobs)
    c2.metric("Active jobs", active_jobs)
    c3.metric("Closed jobs", closed_jobs)
    c4.metric("Latest job posted", format_date(latest_posted))


def freshness_strip(df: pd.DataFrame, file_updated_text: str):
    latest_posted = df["Date Posted"].max() if "Date Posted" in df.columns and not df.empty else pd.NaT
    st.markdown(
        f"""
        <div class="meta-strip">
            <strong>Data file updated:</strong> {file_updated_text}
            &nbsp;&nbsp;|&nbsp;&nbsp;
            <strong>Workflow sync marker:</strong> {LAST_SYNC}
            &nbsp;&nbsp;|&nbsp;&nbsp;
            <strong>Latest job posted:</strong> {format_date(latest_posted)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def top_n_with_other(df: pd.DataFrame, column: str, top_n: int = 10) -> pd.DataFrame:
    if column not in df.columns or df.empty:
        return pd.DataFrame(columns=[column, "Jobs"])

    chart_df = (
        df[df[column].astype(str).str.strip() != ""]
        .groupby(column, dropna=False)
        .size()
        .reset_index(name="Jobs")
        .sort_values("Jobs", ascending=False)
    )

    if len(chart_df) <= top_n:
        return chart_df

    top = chart_df.head(top_n).copy()
    other_sum = chart_df.iloc[top_n:]["Jobs"].sum()
    other_row = pd.DataFrame({column: ["Other"], "Jobs": [other_sum]})
    return pd.concat([top, other_row], ignore_index=True)


def jobs_by_group_chart(df: pd.DataFrame):
    chart_df = top_n_with_other(df, "Job Group", top_n=10)
    if chart_df.empty:
        st.warning("No Job Group values available.")
        return
    st.bar_chart(chart_df, x="Job Group", y="Jobs", use_container_width=True)


def work_setup_chart(df: pd.DataFrame):
    chart_df = top_n_with_other(df, "Work Setup", top_n=10)
    if chart_df.empty:
        st.warning("No Work Setup values available.")
        return
    st.bar_chart(chart_df, x="Work Setup", y="Jobs", use_container_width=True)


def status_chart(df: pd.DataFrame):
    chart_df = top_n_with_other(df, "Job Status", top_n=10)
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


def render_header():
    st.title("NZ Analyst Jobs Explorer")
    st.caption(
        "Browse analyst, analytics, BI, reporting, and data-related roles in New Zealand."
    )


def render_overview(df: pd.DataFrame, file_updated_text: str):
    render_header()
    metric_row(df)
    freshness_strip(df, file_updated_text)

    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.subheader("Jobs by group")
            jobs_by_group_chart(df)

    with right:
        with st.container(border=True):
            st.subheader("Work setup")
            work_setup_chart(df)

    left2, right2 = st.columns(2)
    with left2:
        with st.container(border=True):
            st.subheader("Status mix")
            status_chart(df)

    with right2:
        with st.container(border=True):
            st.subheader("Postings over time")
            postings_over_time_chart(df)

    with st.expander("About this dataset"):
        st.markdown(
            """
            - This app focuses on analyst, analytics, BI, reporting, and related data roles in New Zealand.
            - Job Group is inferred from role titles and should be treated as a browsing aid rather than a perfect classification.
            - The app includes both a file update time and a workflow sync marker to make freshness easier to verify.
            """
        )


def render_explorer(df: pd.DataFrame, file_updated_text: str):
    render_header()
    metric_row(df)
    freshness_strip(df, file_updated_text)

    st.markdown(
        '<div class="section-note">Use the sidebar filters to refine roles, then browse the full job table below.</div>',
        unsafe_allow_html=True,
    )

    if df.empty:
        st.warning("No jobs match the selected filters.")
        return

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
    available_cols = [c for c in display_cols if c in df.columns]

    st.dataframe(
        df[available_cols],
        use_container_width=True,
        hide_index=True,
        height=620,
        column_config={
            "Application Link": st.column_config.LinkColumn(
                "Open role",
                display_text="Apply",
            ),
            "Date Posted": st.column_config.DatetimeColumn(
                "Date Posted",
                format="YYYY-MM-DD",
            ),
            "Date Closed": st.column_config.DatetimeColumn(
                "Date Closed",
                format="YYYY-MM-DD",
            ),
        },
    )

    csv_data = df[available_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered data as CSV",
        data=csv_data,
        file_name="nz_analyst_jobs_filtered.csv",
        mime="text/csv",
    )


def render_footer():
    st.markdown("---")
    st.caption(f"Source: OpenJobData • {DATASET_URL}")
    st.caption(f"Documentation: {DOCS_URL}")


def main():
    inject_custom_css()

    if not DATA_PATH.exists():
        st.error(f"Data file not found: {DATA_PATH}")
        st.stop()

    data_mtime = DATA_PATH.stat().st_mtime
    file_updated_text = format_file_timestamp(data_mtime)

    df = load_data(str(DATA_PATH), data_mtime)
    if df.empty:
        st.warning("No data available.")
        st.stop()

    filters = render_sidebar_filters(df)
    filtered_df = apply_filters(df, filters)

    tab1, tab2 = st.tabs(["Overview", "Job Explorer"])

    with tab1:
        render_overview(filtered_df, file_updated_text)

    with tab2:
        render_explorer(filtered_df, file_updated_text)

    render_footer()


if __name__ == "__main__":
    main()
