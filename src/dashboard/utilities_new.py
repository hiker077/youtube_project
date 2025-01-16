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
    df["PUBLISHEDAT"] = pd.to_datetime(df["PUBLISHEDAT"])
    return df


def filter_data(
    data,
    chart1_state,
    chart3_state,
    chart4_state,
    trigger_id,
    slider_filter_state,
    dropdown_filter_state,
    state_data,
    date_picker_start,
    date_picker_end,
):
    """Filter our all neceserry data base on callback Input and State conditions."""

    data["PUBLISHEDAT"] = pd.to_datetime(data["PUBLISHEDAT"])
    date_picker_start = datetime.strptime(date_picker_start, "%Y-%m-%d").date()
    date_picker_end = datetime.strptime(date_picker_end, "%Y-%m-%d").date()
    filtered_data = data[
        (data["PUBLISHEDAT"].dt.date.between(date_picker_start, date_picker_end))
        & (data["VIDEO_TIME"].between(slider_filter_state[0], slider_filter_state[1]))
        & (data["CATEGORY_TITLE"].isin(dropdown_filter_state))
    ]

    # Manage state data
    state_data = state_data or {}
    if trigger_id:
        state_data.pop(
            trigger_id, None
        ) if trigger_id in state_data else state_data.update({trigger_id: 0})

        if chart1_state and "chart-1" in state_data:
            selected_month = pd.to_datetime(chart1_state["points"][0]["x"]).strftime(
                "%Y-%m"
            )
            filtered_data = filtered_data[filtered_data["YEAR_MONTH"] == selected_month]

        if chart3_state and "chart-3" in state_data:
            selected_day = chart3_state["points"][0]["x"]
            filtered_data = filtered_data[
                filtered_data["DAY_OF_WEEK_NAME"] == selected_day
            ]

        if chart4_state and "chart-4" in state_data:
            selected_category = chart4_state["points"][0]["x"]
            filtered_data = filtered_data[
                filtered_data["CATEGORY_TITLE"] == selected_category
            ]

    return filtered_data, state_data


def calculate_kpis(data: pd.DataFrame) -> tuple[int, float, float, float]:
    """
    Calculate key performance indicators.
    """
    count = len(data)
    views_mean = round(data["VIEWCOUNT"].mean(), 0)
    comments_mean = round(data["COMMENTCOUNT"].mean(), 0)
    likes_mean = round(data["LIKECOUNT"].mean(), 0)

    return count, views_mean, comments_mean, likes_mean


def generate_charts(data: pd.DataFrame) -> tuple[px.line, px.scatter, px.bar, px.box]:
    """
    Generate charts for the dashboard.
    """
    # Chart 1: Number of published videos by month
    monthly_data = (
        data.groupby("YEAR_MONTH")
        .size()
        .reset_index(name="count")
        .sort_values("YEAR_MONTH")
    )
    fig1 = px.line(
        monthly_data,
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
        title="Number of Published Videos",
        xaxis_title="Month",
        yaxis_title="Number of Videos",
        xaxis_tickangle=-45,
    )

    # Chart 2: Category statistics
    category_stats = (
        data.groupby("CATEGORY_TITLE")
        .agg(
            Average_Views=("VIEWCOUNT", "mean"),
            Average_Likes=("LIKECOUNT", "mean"),
            Number_of_Movies=("CATEGORY_TITLE", "size"),
        )
        .reset_index()
    )
    sizeref = 2.0 * max(category_stats["Number_of_Movies"]) / (100**2)
    fig2 = px.scatter(
        category_stats,
        x="Average_Views",
        y="Average_Likes",
        size="Number_of_Movies",
        color="CATEGORY_TITLE",
        template="plotly_white",
    )
    fig2.update_traces(marker=dict(sizemode="area", sizeref=sizeref, line_width=2))
    fig2.update_layout(
        title="Category Statistics", xaxis_title="Avg. Views", yaxis_title="Avg. Likes"
    )

    # Chart 3: Day of publication statistics
    day_data = (
        data.groupby(["DAY_OF_WEEK_NAME", "PUBLISHED_PERIOD", "DAY_OF_WEEK_NUMBER"])
        .size()
        .reset_index(name="COUNT")
        .sort_values("DAY_OF_WEEK_NUMBER")
    )
    fig3 = px.bar(
        day_data,
        x="DAY_OF_WEEK_NAME",
        y="COUNT",
        color="PUBLISHED_PERIOD",
        template="plotly_white",
    )
    fig3.update_layout(
        title="Day of Video Publication",
        xaxis_title="Day of Week",
        yaxis_title="Number of Videos",
    )

    # Chart 4: Video duration by category
    fig4 = px.box(
        data,
        x="CATEGORY_TITLE",
        y="VIDEO_TIME",
        template="plotly_white",
        color="CATEGORY_TITLE",
    )
    fig4.update_layout(
        title="Video Duration by Category",
        xaxis_title="Category",
        yaxis_title="Duration (minutes)",
        showlegend=False,
    )

    return fig1, fig2, fig3, fig4


def extract_filter_parameters(data: pd.DataFrame) -> tuple:
    """
    Extract default filter parameters from the dataset.
    """
    raw_data = data.to_dict("records")
    picker_start = data["PUBLISHEDAT"].min().date()
    picker_end = data["PUBLISHEDAT"].max().date()
    min_duration = data["VIDEO_TIME"].min()
    max_duration = data["VIDEO_TIME"].max()
    categories = data["CATEGORY_TITLE"].unique().tolist()

    return raw_data, picker_start, picker_end, min_duration, max_duration, categories
