import re
##pobierz pobrane dane 
import json
import pandas as pd
from datetime import datetime


def get_publishing_period(x):
    ##define date period in which channel published movie
    x = int(x.strftime("%H"))
    if 5 <= x < 12:
        return "Morning"
    elif 12 <= x < 18:
        return "Afternoon"
    else:
        return "Evening"


def get_minutes(x):
    ##function to extact time (in minutes)

    hour = re.search(r'(\d{1,2})H', x)
    minute = re.search(r'(\d{1,2})M', x)
    second = re.search(r'(\d{1,2})S', x)

    hour = 0 if hour is None else int(hour.group(1))
    minute = 0 if minute is None else int(minute.group(1))
    second = 0 if second is None else int(second.group(1))
    minutes = round(hour * 60 + minute + second / 60, 2)

    return minutes


def prepare_and_save_data(path_video_statistics_list, path_videos_categories):
    """
    Funciton return csv file with youtube data which will be used to dashboard prepataion. 
    """

    videos_df = pd.read_json(path_video_statistics_list)
    videos_categories = pd.read_json(path_videos_categories)
    videos_categories.rename(columns={'id': 'categoryId', 'title': 'category_title'}, inplace=True)

    # change type of objects
    videos_df[['viewCount', 'likeCount', 'commentCount', 'categoryId']] = videos_df[
        ['viewCount', 'likeCount', 'commentCount', 'categoryId']].fillna(0).astype('int64')

    ##define new column with minutes of video
    videos_df['video_time'] = videos_df['contentDetails'].apply(lambda x: get_minutes(x))
    videos_df['publishedAt'] = videos_df['publishedAt'].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ"))
    videos_df['published_period'] = videos_df['publishedAt'].apply(lambda x: get_publishing_period(x))
    videos_df['YEAR_MONTH'] = videos_df['publishedAt'].dt.to_period('M')
    videos_df['DAY_OF_WEEK_NAME'] = videos_df['publishedAt'].dt.day_name()
    videos_df['DAY_OF_WEEK_NUMBER'] = videos_df['publishedAt'].dt.day_of_week
    videos_df = videos_df.merge(videos_categories, on='categoryId')
    videos_df.columns = videos_df.columns.str.upper()

    return videos_df
