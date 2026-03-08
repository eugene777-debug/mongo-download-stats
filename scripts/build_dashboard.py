import pandas as pd
import plotly.graph_objects as go

def load_data():
    pymongo = pd.read_csv("data/pymongo.csv", parse_dates=["week_start", "week_end"])
    mongodb = pd.read_csv("data/mongodb.csv", parse_dates=["week_start", "week_end"])
    return pymongo, mongodb

def make_chart(df, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["week_start"],
        y=df["downloads"],
        mode="lines",
        name=title
    ))
    fig.update_layout(title=title, xaxis_title="Week", yaxis_title="Downloads")
    return fig.to_html(full_html=False)

def make_yoy_chart(df, title):
    df = df.copy()

    # Keep only the last 3 years of data
    if "week_start" in df.columns:
        cutoff = df["week_start"].max() - pd.DateOffset(years=3)
        df = df[df["week_start"] >= cutoff]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["week_start"],
        y=df["yoy"],
        mode="lines",
        name=title
    ))
    fig.update_layout(
        title=f"{title} YoY % Growth",
        xaxis_title="Week",
        yaxis_title="YoY %"
    )
    return fig.to_html(full_html=False)


def main():
    pymongo, mongodb = load_data()

    with open("index.html", "w") as f:
        f.write("<html><head><title>Mongo Download Stats</title></head><body>")
        f.write("<h1>MongoDB Ecosystem Download Trends</h1>")

        f.write("<h2>pymongo Weekly Downloads</h2>")
        f.write(make_chart(pymongo, "pymongo Weekly Downloads"))

        f.write("<h2>mongodb Weekly Downloads</h2>")
        f.write(make_chart(mongodb, "mongodb Weekly Downloads"))

        f.write("<h2>pymongo YoY Growth</h2>")
        f.write(make_yoy_chart(pymongo, "pymongo"))

        f.write("<h2>mongodb YoY Growth</h2>")
        f.write(make_yoy_chart(mongodb, "mongodb"))

        f.write("</body></html>")

if __name__ == "__main__":
    main()
