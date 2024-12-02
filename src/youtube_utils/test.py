from youtube_api import get_video_list, get_video_statistics, get_video_categories
from config import *
from data_processing import prepare_and_save_data
import pandas as pd 
import json

video_list_long = get_video_list(url =  URL_SEARCH, api_key = API_KEY, channel_id= CHANNEL_ID,published_after= PUBLISHED_AFTER, published_before = PUBLISHED_BEFORE,  video_duration= VIDEO_DURATION_LONG, download_iteration=1)
print(video_list_long)