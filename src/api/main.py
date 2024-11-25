from youtube_utils.youtube_api import get_video_list, get_video_statistics, get_video_categories
from youtube_utils.config import *
from youtube_utils.data_processing import prepare_and_save_data
import pandas as pd 
import json

def main():
    #Download list of videoID's
    # set up long or medium

    print('1. Dowload of video IDs started.')
    video_list_long = get_video_list(url =  URL_SEARCH, api_key = API_KEY, channel_id= CHANNEL_ID,published_after= PUBLISHED_AFTER, published_before = PUBLISHED_BEFORE,  video_duration= VIDEO_DURATION_LONG)
    video_list_medium = get_video_list(url =  URL_SEARCH, api_key = API_KEY, channel_id= CHANNEL_ID, published_after= PUBLISHED_AFTER, published_before=PUBLISHED_BEFORE, video_duration= VIDEO_DURATION_MEDIUM)
    video_list = video_list_long + video_list_medium

    print('2. Saving of video IDs list to started.')
    with open('data/raw_data/video_list.json', 'w') as file:
        json.dump(video_list, file)

    #Dowload video statistics
    # Adding less URL_VIDEOS, parallel
       #dodaj ścieżki do CONFIG 
    print('3. Saving of videos statistics list has been started.')
    video_statistics, category_list = get_video_statistics(url = URL_VIDEOS, channelId = CHANNEL_ID, videoList = video_list, api_key=API_KEY)
    with open('data/raw_data/video_statistics_list.json', 'w') as file:
        json.dump(video_statistics, file)
    

    # #Dowload video categories
    print('4. Saving of videos categories list has been started.')
    video_categories = get_video_categories(url=URL_VIDEO_CATEGORIES, api_key= API_KEY, list_of_id= category_list)
    with open('data/raw_data/video_categories.json', 'w') as file:
        json.dump(video_categories, file)

    print('5. Saving of dashboard data has been started.')
    youtube_data_dashboard = prepare_and_save_data(path_video_statistics_list =PATH_VIDEO_STATISTICS_LIST, path_videos_categories= PATH_VIDEOS_CATEGORIES)
    youtube_data_dashboard.to_csv(PATH_DASHBOARD_DATA + 'youtube_data_dashboard.csv')
    

    
if __name__ == "__main__":
    main()