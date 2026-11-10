
import requests
import pandas as pd
import os
from datetime import datetime, timezone

# API Configuration
URL = "https://remoteok.com/api"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; JobMarketAnalysis/1.0)"
}

# Fetch jobs from Remote OK
response = requests.get(
    URL,
    headers=HEADERS,
    timeout=30
)

response.raise_for_status()

jobs_data = response.json()[1:]

new_jobs = []

scraped_at = datetime.now(timezone.utc).isoformat()

# Extract job information
for job in jobs_data:

    job_id = job.get("id")

    # Skip jobs without a valid ID
    if job_id is None or str(job_id).strip() == "":
        continue

    tags = job.get("tags") or []

    new_jobs.append({
        "job_id": str(job_id),
        "job_title": job.get("position"),
        "company": job.get("company"),
        "location": job.get("location"),
        "tags": ", ".join(tags),
        "description": job.get("description"),
        "posted_date": job.get("date"),
        "salary_min": job.get("salary_min"),
        "salary_max": job.get("salary_max"),
        "job_url": job.get("url"),
        "apply_url": job.get("apply_url"),
        "scraped_at": scraped_at
    })

# Convert extracted jobs to DataFrame
new_df = pd.DataFrame(new_jobs)

# Remove duplicates within the current scraping run
new_df.drop_duplicates(
    subset=["job_id"],
    keep="last",
    inplace=True
)

# CSV file path
file_path = "remoteok_jobs.csv"

# Load existing data and append only new jobs
if os.path.exists(file_path):

    old_df = pd.read_csv(
        file_path,
        dtype={"job_id": str}
    )

    old_ids = set(old_df["job_id"].dropna())

    # Identify jobs that do not exist in the old CSV
    truly_new_jobs = new_df[
        ~new_df["job_id"].isin(old_ids)
    ]

    # Append only new jobs
    combined_df = pd.concat(
        [old_df, truly_new_jobs],
        ignore_index=True
    )

else:

    truly_new_jobs = new_df.copy()
    combined_df = new_df.copy()

# Save updated data
combined_df.to_csv(
    file_path,
    index=False,
    encoding="utf-8-sig"
)

# Display execution summary
print("Jobs fetched:", len(jobs_data))
print("Valid unique jobs fetched:", len(new_df))
print("Truly new jobs:", len(truly_new_jobs))
print("Total unique jobs:", combined_df["job_id"].nunique())
print("Data saved successfully!")
