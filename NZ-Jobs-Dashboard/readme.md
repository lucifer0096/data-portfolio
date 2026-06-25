# NZ Jobs Dashboard

A Streamlit dashboard for exploring analyst, analytics, BI, reporting, and related job postings in New Zealand.

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

## Live app

Deployed on Streamlit Community Cloud from:

- Repository: `lucifer0096/data-portfolio`
- Branch: `main`
- App file: `NZ-Jobs-Dashboard/app/app.py`

## Data pipeline

The project uses a GitHub Actions workflow to:

1. run the sync script,
2. refresh the parquet outputs,
3. update a build marker file used by the app,
4. verify that the app can still start correctly.

The main workflow file is:

```text
.github/workflows/sync-nz-jobs.yml
```

## Manual refresh

You can trigger the workflow manually from GitHub:

1. Open the repository.
2. Go to **Actions**.
3. Select **Sync and Verify NZ Jobs App**.
4. Click **Run workflow**.
5. Run it on the `main` branch.

GitHub supports manual workflow runs through `workflow_dispatch`.

## What the timestamps mean

The app shows two useful refresh signals:

- **Data file updated** = the modified time of the deployed parquet file.
- **Workflow sync marker** = the timestamp written by GitHub Actions after a successful sync.

The **Latest Job Posted** metric is different: it shows the newest job posting date in the dataset, not the workflow run time.

## Local run

Install dependencies and start the app:

```bash
pip install -r NZ-Jobs-Dashboard/requirements.txt
streamlit run NZ-Jobs-Dashboard/app/app.py
```

## Notes

- The dashboard reads from `data/gold/analyst_roles.parquet`.
- The app uses relative paths so it works from the repository structure used in GitHub and Streamlit Community Cloud.
- The project is designed to reduce manual refresh steps by using GitHub Actions for scheduled and manual updates.
