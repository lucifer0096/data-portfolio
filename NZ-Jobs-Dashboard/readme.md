# NZ Jobs Dashboard

A Streamlit dashboard for exploring analyst, analytics, BI, reporting, and related job postings in New Zealand.

## Live app

[Open the dashboard](https://lucifer0096-nz-jobs-dashboard-app.streamlit.app/)

## Overview

This project filters and presents analyst-related roles from a broader jobs dataset. It includes:
- an interactive Streamlit dashboard,
- cleaned parquet outputs for app use,
- and a GitHub Actions workflow that refreshes the dataset automatically.

## Project structure

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

The app is deployed on Streamlit Community Cloud using:
- Repository: `lucifer0096/data-portfolio`
- Branch: `main`
- App file: `NZ-Jobs-Dashboard/app/app.py`

## Data refresh

The GitHub Actions workflow:
1. runs the sync script,
2. refreshes the parquet outputs,
3. updates the app build marker,
4. verifies that the app can still start correctly.

Workflow file:

```text
.github/workflows/sync-nz-jobs.yml
```

You can also run it manually from the **Actions** tab because the workflow uses `workflow_dispatch`.

## Timestamps in the app

The app shows:
- **Data file updated** = the modified time of the deployed parquet file.
- **Workflow sync marker** = the timestamp written by GitHub Actions after a successful sync.
- **Latest Job Posted** = the newest posting date in the dataset, not the workflow runtime.

## Local run

```bash
pip install -r NZ-Jobs-Dashboard/requirements.txt
streamlit run NZ-Jobs-Dashboard/app/app.py
```

## Source credit

This dashboard uses job-listing data from [OpenJobData](https://openjobdata.com).
For dataset setup and documentation, see the [OpenJobData documentation](https://openjobdata.com/documentation).
