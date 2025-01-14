import plotly.express as px
import pandas as pd
from datetime import datetime


def load_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df["TITLE"] = [
        f"[{title}]({link})"
        for title, link in zip(
            df["TITLE"], ("https://www.youtube.com/watch?v=" + df["VIDEOID"])
        )
    ]
    return df


def data_filter(
    dff,
    chart1_state,
    chart3_state,
    chart4_state,
    trigger_id,
    slider_filter_state,
    dropdown_filter_state,
    state_data,
    date_picker_start,
    date_picker_end,
    is_month=False,
):
    """Filter our all neceserry data base on callback Input and State conditions."""

    dff["PUBLISHEDAT"] = pd.to_datetime(dff["PUBLISHEDAT"])
    date_picker_start = datetime.strptime(date_picker_start, "%Y-%m-%d").date()
    date_picker_end = datetime.strptime(date_picker_end, "%Y-%m-%d").date()
    dff = dff.loc[
        (dff["PUBLISHEDAT"].dt.date >= date_picker_start)
        & (dff["PUBLISHEDAT"].dt.date <= date_picker_end)
    ]
    dff = dff[
        (dff["VIDEO_TIME"] >= slider_filter_state[0])
        & (dff["VIDEO_TIME"] <= slider_filter_state[1])
    ]
    dff = dff[dff["CATEGORY_TITLE"].isin(dropdown_filter_state)]

    state_data = state_data if state_data is not None else {}

    if trigger_id is not None:
        if trigger_id in state_data:
            state_data.pop(trigger_id)
        else:
            state_data[trigger_id] = 0

        if chart1_state is not None and "chart-1" in state_data:
            chart1_state = chart1_state["points"][0]["x"]
            month = pd.to_datetime(chart1_state).strftime("%Y-%m")
            dff = dff[dff["YEAR_MONTH"] == month]

        if chart3_state is not None and "chart-3" in state_data:
            chart3_state = chart3_state["points"][0]["x"]
            dff = dff[dff["DAY_OF_WEEK_NAME"] == chart3_state]

        if chart4_state is not None and "chart-4" in state_data:
            chart4_state = chart4_state["points"][0]["x"]
            dff = dff[dff["CATEGORY_TITLE"] == chart4_state]
    else:
        state_data = {}

    return dff, state_data


def kpis(df):
    """Count KPI's results which are displayed on main dashboard page."""

    count = len(df)
    views_mean = round(df["VIEWCOUNT"].mean(), 0)
    comment_mean = round(df["COMMENTCOUNT"].mean(), 0)
    like_mean = round(df["LIKECOUNT"].mean(), 0)

    return count, views_mean, comment_mean, like_mean


def build_charts(data: pd.DataFrame):
    """Generate 4 charts dispaly in dashboard."""

    ## Chart 1
    df1 = (
        data.groupby("YEAR_MONTH")["YEAR_MONTH"]
        .count()
        .reset_index(name="count")
        .sort_values(by="YEAR_MONTH", ascending=True)
    )
    fig1 = px.line(
        df1,
        x="YEAR_MONTH",
        y="count",
        markers=True,
        text="count",
        template="plotly_white",
    )
    fig1.update_traces(
        textposition="top right",
        line=dict(color="firebrick", width=3),
        line_shape="spline",
    )
    fig1.update_layout(
        title="Number of published videos",
        xaxis_title="Month",
        yaxis_title="Number of movies",
        barmode="group",
        xaxis_tickangle=-45,
    )
    # Chart 2
    df2 = (
        data.groupby(["CATEGORY_TITLE"])
        .aggregate({"VIEWCOUNT": "mean", "LIKECOUNT": ["mean", "count"]})
        .reset_index()
    )
    df2.columns = ["_".join(col).strip("_") for col in df2.columns]
    df2.columns = [
        "Category",
        "Average of views",
        "Average of likes",
        "Number of movies",
    ]
    sizeref = 2.0 * (df2["Number of movies"].max()) / (100**2)
    fig2 = px.scatter(
        df2,
        x="Average of views",
        y="Average of likes",
        size="Number of movies",
        color="Category",
        template="plotly_white",
    )
    fig2.update_traces(marker=dict(sizemode="area", sizeref=sizeref, line_width=2))
    fig2.update_layout(
        title="Category statistics",
        xaxis_title="Avg. number of views",
        yaxis_title="Avg. number of likes",
    )
    # Chart 3
    df3 = (
        data.groupby(["DAY_OF_WEEK_NAME", "PUBLISHED_PERIOD", "DAY_OF_WEEK_NUMBER"])
        .size()
        .reset_index(name="COUNT")
        .sort_values(by="DAY_OF_WEEK_NUMBER")
    )
    fig3 = px.bar(
        df3,
        x="DAY_OF_WEEK_NAME",
        y="COUNT",
        color="PUBLISHED_PERIOD",
        template="plotly_white",
    )
    fig3.update_layout(
        title="Day of video publication",
        xaxis_title="Day of week",
        yaxis_title="Number of movies",
    )
    # Chart 4
    fig4 = px.box(
        data,
        x="CATEGORY_TITLE",
        y="VIDEO_TIME",
        template="plotly_white",
        color="CATEGORY_TITLE",
    )
    # fig4.update_traces( boxpoints='all', jitter=0.5,)
    fig4.update_layout(
        title="Statistics of video time",
        xaxis_title="Category",
        yaxis_title="Video time",
        showlegend=False,
    )

    return fig1, fig2, fig3, fig4


def get_filters_parameters(data: pd.DataFrame):
    """Prepare default values from page filters"""

    raw_data = data.to_dict("records")
    picker_range_start_date = pd.to_datetime(data["PUBLISHEDAT"]).dt.date.min()
    picker_range_end_date = pd.to_datetime(data["PUBLISHEDAT"]).dt.date.max()
    range_sider_video_time_min = data["VIDEO_TIME"].min()
    range_sider_video_time_max = data["VIDEO_TIME"].max()
    drop_down_category = data["CATEGORY_TITLE"].unique()

    return (
        raw_data,
        picker_range_start_date,
        picker_range_end_date,
        range_sider_video_time_min,
        range_sider_video_time_max,
        drop_down_category,
    )
