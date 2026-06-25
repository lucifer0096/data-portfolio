# NZ Analyst Jobs Explorer

A Streamlit dashboard for exploring analyst-related job postings in New Zealand.

This project turns raw job listing snapshots into a cleaned analyst-focused dataset and an interactive dashboard for browsing trends, filtering roles, and opening application links. The dashboard is built on top of OpenJobData job listing data and documentation. [OpenJobData](https://openjobdata.com) [OpenJobData Documentation](https://openjobdata.com/documentation)

## Project overview

The project has two main parts:

- **Data pipeline**: downloads and merges raw job-change parquet files, filters New Zealand jobs, standardizes important fields, and creates cleaned outputs.
- **Streamlit app**: loads the cleaned analyst roles dataset and provides a simple interface for filtering, charting, and browsing jobs.

The pipeline currently:
- downloads remote parquet change files from a Hugging Face-backed source
- filters rows where the country is New Zealand or NZ
- keeps a selected set of fields such as title, department, job type, work setup, status, dates, and application link
- standardizes job type, work setup, remote flag, and status
- creates an analyst-focused gold dataset based on job-title keyword grouping
- exports parquet and Excel outputs

## Features

The Streamlit dashboard includes:

- Search by job title
- Filter by date posted
- Filter by job group
- Filter by job type
- Filter by work setup
- Filter by remote status
- Filter by job status
- Sort by newest posted, oldest posted, recently closed, or job title A-Z
- KPI cards for jobs shown, active jobs, closed jobs, and latest visible posting date
- Charts for job group, job status, postings over time, and work setup
- A browsable cleaned analyst roles table with application links

## Folder structure

```text
nz-jobs-dashboard/
├── app/
│   └── app.py
├── scripts/
│   └── sync_nz_jobs.py
├── data/
│   ├── gold/
│   │   └── analyst_roles.parquet
│   └── silver/
│       └── nz_master.parquet
├── requirements.txt
├── .gitignore
└── README.md
```

## Data outputs

The pipeline generates these main outputs:

- `data/silver/nz_master.parquet`  
  Cleaned New Zealand jobs dataset.

- `data/gold/analyst_roles.parquet`  
  Analyst-focused dataset used by the Streamlit dashboard.

It also creates Excel outputs in the local project workflow:

- `data/nz_master.xlsx`
- `data/analyst_roles.xlsx`

## Key fields in the app

The dashboard uses these cleaned fields:

- **Job Group**: broad category inferred from words in the job title
- **Job Title**: advertised title of the role
- **Department**: business area or team when available
- **Job Type**: full-time, part-time, contract, casual, fixed-term, or not specified
- **Work Setup**: on-site, hybrid, remote, or unknown
- **Remote**: yes, no, or unknown
- **Date Posted**: posting date
- **Date Closed**: close date when available
- **Job Status**: active, closed, or unknown
- **Application Link**: direct job listing URL

## Analyst role grouping

Analyst-related rows are identified from job titles using keyword-based group patterns. Current groups include:

- Business Intelligence
- Data
- Analytics
- Reporting
- Insights
- Pricing
- Forecasting
- Analyst

This grouping is designed for simple browsing rather than perfect occupational classification.

## How to run locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the app

From the repository root, run:

```bash
streamlit run app/app.py
```

### 3. Run the sync script

```bash
python scripts/sync_nz_jobs.py
```

## Deployment notes

This app is intended for deployment with Streamlit Community Cloud.

If this project sits inside a larger portfolio repository, make sure file paths in the app are relative to the **repository root**, because Community Cloud runs from the root of the GitHub repository rather than the app subfolder.

Example deployment entrypoint:

```text
nz-jobs-dashboard/app/app.py
```

## Data source

This project uses job-listing data from OpenJobData:

- [OpenJobData Homepage](https://openjobdata.com)
- [OpenJobData Documentation](https://openjobdata.com/documentation)

## Tech stack

- Python
- Pandas
- Streamlit
- PyArrow
- Hugging Face Hub
- XlsxWriter

## Notes

- The current dashboard is focused on analyst-related roles in New Zealand.
- Job groups are inferred from titles, so they should be treated as a practical browsing aid rather than a formal taxonomy.
- The app uses the cleaned gold parquet dataset for fast loading and filtering.

## Author

Created by Lucifer0096 as part of a broader data portfolio project.
