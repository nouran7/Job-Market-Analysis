

import requests
import pandas as pd
import os
from datetime import datetime, timezone

URL = "https://remoteok.com/api"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; JobMarketAnalysis/1.0)"
}

response = requests.get(URL, headers=HEADERS, timeout=30)
response.raise_for_status()

jobs_data = response.json()[1:]

new_jobs = []

scraped_at = datetime.now(timezone.utc).isoformat()

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

new_df = pd.DataFrame(new_jobs)

file_path = "remoteok_jobs.csv"

if os.path.exists(file_path):

    old_df = pd.read_csv(file_path, dtype={"job_id": str})

    old_ids = set(old_df["job_id"].dropna())

    new_df = new_df[
        ~new_df["job_id"].isin(old_ids)
    ]

    combined_df = pd.concat(
        [old_df, new_df],
        ignore_index=True
    )

else:
    combined_df = new_df

combined_df.to_csv(
    file_path,
    index=False,
    encoding="utf-8-sig"
)
print("Jobs fetched:", len(new_jobs))
print("Truly new jobs:", truly_new_jobs)
print("Total unique jobs:", combined_df["job_id"].nunique())
print("Data saved successfully!")
