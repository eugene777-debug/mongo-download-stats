import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_pypi_history():
    url = "https://pypistats.org/api/packages/pymongo/overall?mirrors=false"
    data = requests.get(url).json()["data"]

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # Convert daily → weekly
    df = df.set_index("date").resample("W-SUN")["downloads"].sum().reset_index()
    df["week_start"] = df["date"] - pd.to_timedelta(6, unit="d")
    df["week_end"] = df["date"]

    return df[["week_start", "week_end", "downloads"]]

def compute_yoy(df):
    df = df.copy()
    df["yoy"] = None

    for i in range(len(df)):
        this_week = df.loc[i, "downloads"]
        this_start = df.loc[i, "week_start"]

        last_year_start = this_start - timedelta(days=365)
        match = df[df["week_start"] == last_year_start]

        if len(match) == 1:
            last_year = match["downloads"].values[0]
            if last_year > 0:
                df.loc[i, "yoy"] = (this_week - last_year) / last_year * 100

    return df

def main():
    df = fetch_pypi_history()
    df = compute_yoy(df)
    df.to_csv("data/pymongo.csv", index=False)

if __name__ == "__main__":
    main()
