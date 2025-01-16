import re
import pandas as pd
import logging


logger = logging.getLogger(__name__)


def get_publishing_period(hour):
    """
    Determine the publishing period (Morning, Afternoon, Evening) based on the hour.
    """
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Afternoon"
    else:
        return "Evening"


def extract_duration_in_minutes(duration):
    """
    Extract the duration in minutes from an ISO 8601 duration string.
    """
    hour_match = re.search(r"(\d{1,2})H", duration)
    minute_match = re.search(r"(\d{1,2})M", duration)
    second_match = re.search(r"(\d{1,2})S", duration)

    hours = int(hour_match.group(1)) if hour_match else 0
    minutes = int(minute_match.group(1)) if minute_match else 0
    seconds = int(second_match.group(1)) if second_match else 0

    # Convert total duration to minutes (rounded to 2 decimal places)
    total_minutes = round(hours * 60 + minutes + seconds / 60, 2)

    return total_minutes


def transform_data(video_stats_path, categories_path):
    """
    Transform YouTube video and category data into a processed DataFrame.

    Args:
        video_stats_path (str): Path to the JSON file containing video statistics.
        categories_path (str): Path to the JSON file containing video categories.

    Returns:
        pd.DataFrame: Transformed DataFrame ready for dashboard preparation.
    """
    logger.info("Data transformation has started.")

    # Load video statistics and category data
    videos_df = pd.read_json(video_stats_path)
    categories_df = pd.read_json(categories_path)

    # Rename category columns for better clarity
    categories_df.rename(
        columns={"id": "categoryId", "title": "category_title"}, inplace=True
    )

    # Fill missing values and ensure numerical types for key metrics
    videos_df[["viewCount", "likeCount", "commentCount", "categoryId"]] = (
        videos_df[["viewCount", "likeCount", "commentCount", "categoryId"]]
        .fillna(0)
        .astype("int64")
    )

    # Add a new column for video duration in minutes
    videos_df["video_time"] = videos_df["contentDetails"].apply(
        extract_duration_in_minutes
    )

    # Convert publishedAt to datetime and derive related time columns
    videos_df["publishedAt"] = pd.to_datetime(
        videos_df["publishedAt"], format="%Y-%m-%dT%H:%M:%SZ"
    )
    videos_df["published_period"] = videos_df["publishedAt"].dt.hour.apply(
        get_publishing_period
    )
    videos_df["YEAR_MONTH"] = videos_df["publishedAt"].dt.to_period("M")
    videos_df["DAY_OF_WEEK_NAME"] = videos_df["publishedAt"].dt.day_name()
    videos_df["DAY_OF_WEEK_NUMBER"] = videos_df["publishedAt"].dt.day_of_week

    # Merge video data with category data
    videos_df = videos_df.merge(categories_df, on="categoryId", how="left")

    # Standardize column names to uppercase
    videos_df.columns = videos_df.columns.str.upper()

    logger.info("Data transformation has completed.")

    return videos_df
