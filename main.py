from youtube_utils.api import get_video_list, get_video_statistics, get_video_categories
from youtube_utils.config import *
from youtube_utils.data_processing import prepare_and_save_data
import json

def main():
    ##Download list of videoID's
    ## set up long or medium

    # print('1. Dowload of video IDs started.')
    # video_list = get_video_list(url =  URL_SEARCH, api_key = API_KEY, maxResults= MAX_RESULTS, channel_id= CHANNEL_ID, video_duration= VIDEO_DURATION)
    
    # print('2. Saving od video IDs list to started.')
    # with open('data/raw_data/video_list.json', 'w') as file:
    #     json.dump(video_list, file)


    #test
    ##Dowload video statistics
    ## Adding less URL_VIDEOS, parallel
    video_statistics, category_list = get_video_statistics(url = URL_VIDEOS, channelId = CHANNEL_ID, videoList = video_list, api_key=API_KEY)
    #Dowload video categories
    video_categories = get_video_categories(url=URL_VIDEO_CATEGORIES, api_key= API_KEY, list_of_id= category_list)

    #Saving raw data t json. 
    ## !!!Sprawdz czy zadziała lokalizacja w nowym miejscu
    ##dodaj ścieżki do CONFIG 
    with open('data/raw_data/video_statistics_list.json', 'w') as file:
        json.dump(video_statistics, file)

    with open('data/raw_data/video_categories.json', 'w') as file:
        json.dump(video_categories, file)
    
    prepare_and_save_data('data/dashboard_data/', 'youtube_data_dashboard')
    

    
if __name__ == "__main__":
    main()