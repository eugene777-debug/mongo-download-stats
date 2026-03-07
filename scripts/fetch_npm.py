import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_npm_history():
    start = "2015-01-01"
    end = datetime.today().strftime("%Y-%m-%d")

    url = f"https://api.npmjs.org/downloads/range/{start}:{end}/mongodb"
    data = requests.get(url).json()["downloads"]

    df = pd.DataFrame(data)
    df["day"] = pd.to_datetime(df["day"])
    df = df.sort_values("day")

    # Convert daily → weekly
    df = df.set_index("day").resample("W-SUN")["downloads"].sum().reset_index()
    df["week_start"] = df["day"] - pd.to_timedelta(6, unit="d")
    df["week_end"] = df["day"]

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
    df = fetch_npm_history()
    df = compute_yoy(df)
    df.to_csv("data/mongodb.csv", index=False)

if __name__ == "__main__":
    main()
