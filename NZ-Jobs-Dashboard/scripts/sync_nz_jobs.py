from huggingface_hub import HfFileSystem
import pandas as pd
from pathlib import Path
import re
from datetime import datetime

BUCKET_PREFIX = "buckets/Invicto69/Jobs-Dataset-bucket"
CHANGES_DIR = f"{BUCKET_PREFIX}/data/minimal/changes"

PROJECT_DIR = Path("NZ-Jobs-Dashboard")
BASE_DIR = PROJECT_DIR / "data"

LOCAL_CHANGE_CACHE = BASE_DIR / "raw" / "changes"
RAW_NZ_DIR = BASE_DIR / "raw" / "nz_jobs"
SILVER_DIR = BASE_DIR / "silver"
GOLD_DIR = BASE_DIR / "gold"

MASTER_PATH = SILVER_DIR / "nz_master.parquet"
ANALYST_PATH = GOLD_DIR / "analyst_roles.parquet"

MASTER_XLSX_PATH = BASE_DIR / "nz_master.xlsx"
ANALYST_XLSX_PATH = BASE_DIR / "analyst_roles.xlsx"

START_FROM = pd.Timestamp("2026-05-28").date()

KEEP_COLS = [
    "id",
    "job_id",
    "company_id",
    "title",
    "department",
    "employment_type",
    "workplace_type",
    "country",
    "is_remote",
    "posted_at",
    "apply_url",
    "fetched_time",
    "status",
    "close_time",
]

JOB_GROUP_PATTERNS = [
    ("Business Intelligence", r"\bbusiness intelligence\b|\bbi\b"),
    ("Data", r"\bdata\b"),
    ("Analytics", r"\banalytics?\b"),
    ("Reporting", r"\breporting\b"),
    ("Insights", r"\binsights?\b"),
    ("Pricing", r"\bpricing\b"),
    ("Forecasting", r"\bforecast(ing)?\b"),
    ("Analyst", r"\banalyst\b"),
]

for folder in [LOCAL_CHANGE_CACHE, RAW_NZ_DIR, SILVER_DIR, GOLD_DIR]:
    folder.mkdir(parents=True, exist_ok=True)


def col_or_default(df: pd.DataFrame, col_name: str, default="") -> pd.Series:
    if col_name in df.columns:
        return df[col_name]
    return pd.Series([default] * len(df), index=df.index)


def normalize_text(value) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def extract_date_from_filename(name: str):
    stem = Path(name).stem

    patterns = [
        (r"(\d{4}-\d{2}-\d{2})", "%Y-%m-%d"),
        (r"(\d{2}-\d{2}-\d{4})", "%d-%m-%Y"),
        (r"(\d{4}_\d{2}_\d{2})", "%Y_%m_%d"),
        (r"(\d{2}_\d{2}_\d{4})", "%d_%m_%Y"),
    ]

    for pattern, fmt in patterns:
        match = re.search(pattern, stem)
        if match:
            try:
                return datetime.strptime(match.group(1), fmt).date()
            except ValueError:
                pass

    return None


def list_remote_change_files(fs: HfFileSystem):
    files = sorted(fs.glob(f"{CHANGES_DIR}/*.parquet"))

    filtered = []
    for file_path in files:
        file_date = extract_date_from_filename(Path(file_path).name)
        if file_date is not None and file_date >= START_FROM:
            filtered.append(file_path)

    return filtered


def download_remote_files(fs: HfFileSystem, remote_files):
    local_files = []

    for remote_file in remote_files:
        local_path = LOCAL_CHANGE_CACHE / Path(remote_file).name

        if not local_path.exists():
            with fs.open(remote_file, "rb") as src, open(local_path, "wb") as dst:
                dst.write(src.read())

        local_files.append(local_path)

    return local_files


def local_files_from_start():
    files = list(LOCAL_CHANGE_CACHE.glob("*.parquet"))

    filtered = []
    for file_path in files:
        file_date = extract_date_from_filename(file_path.name)
        if file_date is not None and file_date >= START_FROM:
            filtered.append((file_date, file_path))

    filtered.sort(key=lambda x: x[0])
    return [path for _, path in filtered]


def read_nz_subset(file_path: Path) -> pd.DataFrame:
    df = pd.read_parquet(file_path)
    existing_cols = [c for c in KEEP_COLS if c in df.columns]
    if not existing_cols:
        return pd.DataFrame(columns=KEEP_COLS)

    out = df[existing_cols].copy()

    if "country" in out.columns:
        country_mask = (
            out["country"]
            .fillna("")
            .astype(str)
            .str.contains(r"New Zealand|^NZ$", case=False, regex=True)
        )
        out = out[country_mask].copy()

    return out


def prepare_datetime_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in ["posted_at", "fetched_time", "close_time"]:
        if col in out.columns:
            dt = pd.to_datetime(out[col], utc=True, errors="coerce")
            out[col] = dt.dt.tz_convert("Pacific/Auckland").dt.tz_localize(None)
    return out


def standardize_job_group(title: str) -> str:
    title_lower = normalize_text(title).lower()
    for label, pattern in JOB_GROUP_PATTERNS:
        if re.search(pattern, title_lower):
            return label
    return ""


def standardize_job_type(value: str) -> str:
    v = normalize_text(value).lower()
    if not v:
        return "Not specified"
    if "fixed" in v:
        return "Fixed-term"
    if "contract" in v:
        return "Contract"
    if "casual" in v:
        return "Casual"
    if "part" in v:
        return "Part-time"
    if "full" in v or "permanent" in v:
        return "Full-time"
    return normalize_text(value).title()


def standardize_work_setup(value: str) -> str:
    v = normalize_text(value).lower()
    if v in {"onsite", "on-site", "on site"}:
        return "On-site"
    if v == "hybrid":
        return "Hybrid"
    if v == "remote":
        return "Remote"
    if v in {"tbc", "", "na", "n/a", "unknown"}:
        return "Unknown"
    return normalize_text(value).title()


def standardize_remote(remote_value, work_setup: str) -> str:
    setup = normalize_text(work_setup)
    v = normalize_text(remote_value).lower()

    if setup == "Remote":
        return "Yes"
    if v in {"true", "1", "yes"}:
        return "Yes"
    if v in {"false", "0", "no"}:
        return "No"
    if setup in {"On-site", "Hybrid"}:
        return "No"
    return "Unknown"


def standardize_status(value: str) -> str:
    v = normalize_text(value).lower()
    if v == "active":
        return "Active"
    if v == "closed":
        return "Closed"
    return "Unknown"


def build_analyst_roles(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    out["Job Group"] = col_or_default(out, "title").fillna("").astype(str).apply(standardize_job_group)
    out = out[out["Job Group"] != ""].copy()

    out["Job Title"] = col_or_default(out, "title").fillna("").astype(str).str.strip()
    out["Department"] = col_or_default(out, "department").fillna("").astype(str).str.strip()
    out["Department"] = out["Department"].replace("", "Not specified")

    out["Job Type"] = col_or_default(out, "employment_type").apply(standardize_job_type)
    out["Work Setup"] = col_or_default(out, "workplace_type").apply(standardize_work_setup)
    out["Remote"] = [
        standardize_remote(remote_value, work_setup)
        for remote_value, work_setup in zip(col_or_default(out, "is_remote"), out["Work Setup"])
    ]
    out["Date Posted"] = pd.to_datetime(col_or_default(out, "posted_at"), errors="coerce")
    out["Date Closed"] = pd.to_datetime(col_or_default(out, "close_time"), errors="coerce")
    out["Job Status"] = col_or_default(out, "status").apply(standardize_status)
    out["Application Link"] = col_or_default(out, "apply_url").fillna("").astype(str).str.strip()

    final_cols = [
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
    out = out[final_cols].copy()
    out = out.sort_values(["Date Posted", "Job Title"], ascending=[False, True], na_position="last")
    out = out.drop_duplicates(subset=["Job Title", "Application Link"], keep="first").reset_index(drop=True)
    return out


def build_summary(raw_df: pd.DataFrame, analyst_df: pd.DataFrame) -> pd.DataFrame:
    raw_status = col_or_default(raw_df, "status").fillna("").astype(str).str.lower()
    analyst_status = col_or_default(analyst_df, "Job Status").fillna("").astype(str)

    summary_rows = [
        {"Metric": "Total NZ jobs", "Value": len(raw_df)},
        {"Metric": "Open NZ jobs", "Value": int((raw_status == "active").sum())},
        {"Metric": "Closed NZ jobs", "Value": int((raw_status == "closed").sum())},
        {"Metric": "Analyst sheet rows", "Value": len(analyst_df)},
        {"Metric": "Open analyst jobs", "Value": int((analyst_status == "Active").sum())},
        {"Metric": "Closed analyst jobs", "Value": int((analyst_status == "Closed").sum())},
        {"Metric": "Latest analyst post date", "Value": analyst_df["Date Posted"].max() if not analyst_df.empty else pd.NaT},
        {"Metric": "Latest analyst close date", "Value": analyst_df["Date Closed"].max() if not analyst_df.empty else pd.NaT},
    ]
    return pd.DataFrame(summary_rows)


def build_readme() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Field": [
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
            ],
            "Meaning": [
                "Broad group based on words found in the job title.",
                "The advertised role title.",
                "Business area or team, if provided by the source.",
                "Simple job type such as Full-time, Part-time, Contract, Casual, or Fixed-term.",
                "How the job is expected to be worked: On-site, Hybrid, Remote, or Unknown.",
                "Simple Yes / No / Unknown field for remote work.",
                "When the job was posted.",
                "When the job was marked closed, if available.",
                "Whether the job is currently Active or Closed.",
                "Direct link to the job listing.",
            ],
        }
    )


def autofit_worksheet(writer, sheet_name: str, df: pd.DataFrame):
    worksheet = writer.sheets[sheet_name]
    worksheet.freeze_panes(1, 0)

    if len(df.columns) > 0:
        worksheet.autofilter(0, 0, max(len(df), 1), len(df.columns) - 1)

    for i, col in enumerate(df.columns):
        values = df[col].fillna("").astype(str)
        longest_value = values.str.len().max() if not values.empty else 0
        header_len = len(str(col))
        width = min(max(longest_value, header_len) + 2, 40)
        worksheet.set_column(i, i, width)


def write_excel_outputs(raw_df: pd.DataFrame, analyst_df: pd.DataFrame, summary_df: pd.DataFrame, readme_df: pd.DataFrame):
    raw_for_excel = raw_df.sort_values(["posted_at", "title"], ascending=[False, True], na_position="last").copy()

    with pd.ExcelWriter(
        MASTER_XLSX_PATH,
        engine="xlsxwriter",
        datetime_format="yyyy-mm-dd hh:mm:ss",
        date_format="yyyy-mm-dd",
    ) as writer:
        raw_for_excel.to_excel(writer, sheet_name="Raw Data", index=False)
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        analyst_df.to_excel(writer, sheet_name="Analyst Roles", index=False)
        readme_df.to_excel(writer, sheet_name="Read Me", index=False)

        autofit_worksheet(writer, "Raw Data", raw_for_excel)
        autofit_worksheet(writer, "Summary", summary_df)
        autofit_worksheet(writer, "Analyst Roles", analyst_df)
        autofit_worksheet(writer, "Read Me", readme_df)

    with pd.ExcelWriter(
        ANALYST_XLSX_PATH,
        engine="xlsxwriter",
        datetime_format="yyyy-mm-dd hh:mm:ss",
        date_format="yyyy-mm-dd",
    ) as writer:
        analyst_df.to_excel(writer, sheet_name="Analyst Roles", index=False)
        readme_df.to_excel(writer, sheet_name="Read Me", index=False)

        autofit_worksheet(writer, "Analyst Roles", analyst_df)
        autofit_worksheet(writer, "Read Me", readme_df)


def main():
    fs = HfFileSystem()

    remote_files = list_remote_change_files(fs)
    if not remote_files:
        raise FileNotFoundError(f"No remote parquet files found from {START_FROM} onward.")

    download_remote_files(fs, remote_files)

    local_files = local_files_from_start()
    if not local_files:
        raise FileNotFoundError(f"No local parquet files found from {START_FROM} onward.")

    frames = []
    for file_path in local_files:
        try:
            subset = read_nz_subset(file_path)
            if not subset.empty:
                frames.append(subset)
        except Exception as e:
            print(f"Skipping {file_path.name}: {e}")

    if not frames:
        raise ValueError("No New Zealand rows found in the selected parquet files.")

    raw_df = pd.concat(frames, ignore_index=True)
    raw_df = prepare_datetime_columns(raw_df)

    if "fetched_time" in raw_df.columns:
        raw_df = raw_df.sort_values("fetched_time", ascending=False, na_position="last")

    if "id" in raw_df.columns:
        raw_df = raw_df.drop_duplicates(subset=["id"], keep="first")
    else:
        raw_df = raw_df.drop_duplicates()

    raw_df = raw_df.reset_index(drop=True)

    analyst_df = build_analyst_roles(raw_df)
    summary_df = build_summary(raw_df, analyst_df)
    readme_df = build_readme()

    raw_df.to_parquet(MASTER_PATH, index=False)
    analyst_df.to_parquet(ANALYST_PATH, index=False)

    write_excel_outputs(raw_df, analyst_df, summary_df, readme_df)

    print(f"Pulled {len(remote_files)} remote files from {START_FROM} onward")
    print(f"Merged {len(local_files)} local files from {START_FROM} onward")
    print(f"Saved master parquet: {MASTER_PATH}")
    print(f"Saved analyst parquet: {ANALYST_PATH}")
    print(f"Saved master workbook: {MASTER_XLSX_PATH}")
    print(f"Saved analyst workbook: {ANALYST_XLSX_PATH}")


if __name__ == "__main__":
    main()
