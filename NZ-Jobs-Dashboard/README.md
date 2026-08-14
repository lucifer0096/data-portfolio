# NZ Jobs Dashboard

A live Streamlit dashboard for exploring analyst, analytics, BI, reporting, and related job postings in New Zealand, backed by an automated data-refresh pipeline.

**[Open the live dashboard](https://lucifer0096-nz-jobs-dashboard-app.streamlit.app/)**

## Overview

This project filters and presents analyst-related roles from a broader jobs dataset. It includes:
- an interactive Streamlit dashboard,
- cleaned parquet outputs for app use, and
- a GitHub Actions workflow that refreshes the dataset automatically.

## Dataset

- **Source:** [OpenJobData](https://openjobdata.com) ([documentation](https://openjobdata.com/documentation))
- **Scope:** New Zealand job postings, filtered to analyst/BI/reporting/data roles

## Tools & Skills

- Python, Pandas for data cleaning and pipeline logic
- Streamlit for the interactive dashboard
- Parquet for efficient columnar storage between pipeline stages
- GitHub Actions for scheduled/triggered data refresh and verification

## Project Structure

```text
NZ-Jobs-Dashboard/
├── app/
│   ├── app.py
│   └── build_info.py
├── data/
│   ├── gold/
│   │   └── analyst_roles.parquet
│   └── silver/
│       └── nz_master.parquet
├── scripts/
│   └── sync_nz_jobs.py
└── requirements.txt
```

## Deployment

Deployed on Streamlit Community Cloud:
- Repository: `lucifer0096/data-portfolio`
- Branch: `main`
- App file: `NZ-Jobs-Dashboard/app/app.py`

## Data Refresh

The GitHub Actions workflow (`.github/workflows/sync-nz-jobs.yml`):
1. Runs the sync script.
2. Refreshes the parquet outputs.
3. Updates the app build marker.
4. Verifies that the app can still start correctly.

It can also be triggered manually from the **Actions** tab (`workflow_dispatch`).

## Timestamps in the App

- **Data file updated** — modified time of the deployed parquet file.
- **Workflow sync marker** — timestamp written by GitHub Actions after a successful sync.
- **Latest Job Posted** — newest posting date in the dataset (not the workflow runtime).

## How to Run Locally

```bash
pip install -r NZ-Jobs-Dashboard/requirements.txt
streamlit run NZ-Jobs-Dashboard/app/app.py
```

## Future Improvements

- Add role-level trend charts (postings over time by role category).
- Surface salary-band filtering if the source data supports it.

## Source Credit

Job-listing data from [OpenJobData](https://openjobdata.com). See the [documentation](https://openjobdata.com/documentation) for dataset setup details.
