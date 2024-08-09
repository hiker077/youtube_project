##pobierz pobrane dane 
import json
import pandas as pd
from datetime import datetime
from youtube_utils.utils import *


def prepare_and_save_data(path, file_name):
    """
    Funciton return csv file with youtube data which will be use to dashboard prepataion. 
    """

    videos_df = pd.read_json('data/raw_data/video_statistics_list.json')
    videos_categories = pd.read_json('data/raw_data/video_categories.json')
    videos_categories.rename(columns={'id': 'categoryId', 'title': 'category_title'}, inplace=True)


    #change type of objects
    videos_df[['viewCount','likeCount', 'commentCount','categoryId']] = videos_df[['viewCount','likeCount', 'commentCount','categoryId']].astype('int64')

    ##define new column with minutes of video 
    videos_df['video_time'] = videos_df['contentDetails'].apply(lambda x: get_minutes(x))
    videos_df['publishedAt']= videos_df['publishedAt'].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ"))
    videos_df['published_period'] = videos_df['publishedAt'].apply(lambda x: get_publishing_period(x))
    videos_df['YEAR_MONTH'] = videos_df['publishedAt'].dt.to_period('M')
    videos_df['DAY_OF_WEEK_NAME'] = videos_df['publishedAt'].dt.day_name()
    videos_df['DAY_OF_WEEK_NUMBER'] = videos_df['publishedAt'].dt.day_of_week

    videos_df = videos_df.merge(videos_categories, on='categoryId')
    videos_df.columns = videos_df.columns.str.upper()

    videos_df.to_csv(path+ file_name+ '.csv')