# Sample Project — Sales EDA

Short description
- Title: Sample Sales EDA
- Author: Rahul Bhaskaran
- Purpose: A tiny example project to demonstrate repository structure and reproducible notebook/script workflow.

Contents
- notebooks/sample_analysis.ipynb — Jupyter notebook with exploratory steps
- scripts/analysis.py — small script to load sample data and print summaries
- sql/query.sql — example SQL to calculate monthly sales totals
- data/sample_sales.csv — small sample dataset (CSV)
- powerbi/ — place Power BI files here (use Git LFS for large .pbix)

How to run (Python)
1. Create & activate virtual environment:
   - python -m venv .venv
   - source .venv/bin/activate  (macOS/Linux) or .venv\Scripts\activate (Windows)
2. Install pandas if not installed:
   - pip install pandas
3. Run the script:
   - python scripts/analysis.py

Notebook
- Open notebooks/sample_analysis.ipynb in Jupyter Lab to see the exploratory steps.

Notes
- This is a small demo. Replace files with your real project files, keep sample data small, and track large binaries with Git LFS.
