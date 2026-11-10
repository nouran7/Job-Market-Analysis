
file_path = "remoteok_jobs.csv"

if os.path.exists(file_path):

    old_df = pd.read_csv(file_path, dtype={"job_id": str})

    old_ids = set(old_df["job_id"].dropna())

    new_df = new_df.drop_duplicates(
        subset=["job_id"],
        keep="last"
    )

    truly_new_jobs = new_df[
        ~new_df["job_id"].isin(old_ids)
    ]

    combined_df = pd.concat(
        [old_df, truly_new_jobs],
        ignore_index=True
    )

else:
    new_df = new_df.drop_duplicates(
        subset=["job_id"],
        keep="last"
    )

    truly_new_jobs = new_df.copy()
    combined_df = new_df.copy()

combined_df.to_csv(
    file_path,
    index=False,
    encoding="utf-8-sig"
)

print("Jobs fetched:", len(jobs_data))
print("Truly new jobs:", len(truly_new_jobs))
print("Total unique jobs:", combined_df["job_id"].nunique())
print("Data saved successfully!")
