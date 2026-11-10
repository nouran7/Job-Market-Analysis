
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

for job in jobs_data:
    new_jobs.append({
        "job_id": str(job.get("id")),
        "job_title": job.get("position"),
        "company": job.get("company"),
        "location": job.get("location"),
        "tags": ", ".join(job.get("tags", [])),
        "description": job.get("description"),
        "posted_date": job.get("date"),
        "salary_min": job.get("salary_min"),
        "salary_max": job.get("salary_max"),
        "job_url": job.get("url"),
        "apply_url": job.get("apply_url"),
        "scraped_at": datetime.now(timezone.utc).isoformat()
    })

new_df = pd.DataFrame(new_jobs)

file_path = "remoteok_jobs.csv"

if os.path.exists(file_path):
    old_df = pd.read_csv(file_path, dtype={"job_id": str})
    combined_df = pd.concat([old_df, new_df], ignore_index=True)
else:
    combined_df = new_df

combined_df.drop_duplicates(subset=["job_id"], keep="first", inplace=True)

combined_df.to_csv(file_path, index=False, encoding="utf-8-sig")

print("New jobs collected:", len(new_df))
print("Total unique jobs:", len(combined_df))
print("Data saved successfully!")
