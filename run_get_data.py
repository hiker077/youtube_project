import json

from src.config.settings import *
from src.api.main import get_video_list, get_video_statistics, get_video_categories
from src.dashboard.app import app

print(FILE_VIDEO_LIST)

print('1. Dowload of video IDs started.')
video_list_long = get_video_list(url =  URL_SEARCH, api_key = API_KEY, channel_id= CHANNEL_ID,published_after= PUBLISHED_AFTER, published_before = PUBLISHED_BEFORE,  video_duration= VIDEO_DURATION_LONG)
video_list_medium = get_video_list(url =  URL_SEARCH, api_key = API_KEY, channel_id= CHANNEL_ID, published_after= PUBLISHED_AFTER, published_before=PUBLISHED_BEFORE, video_duration= VIDEO_DURATION_MEDIUM)
video_list = video_list_long + video_list_medium

# print('2. Saving of video IDs list to started.')
# with open(FILE_VIDEO_LIST, 'w') as file:
#     json.dump(video_list, file)

#     #Dowload video statistics
#     # Adding less URL_VIDEOS, parallel
#        #dodaj ścieżki do CONFIG 
# print('3. Saving of videos statistics list has been started.')
# video_statistics, category_list = get_video_statistics(url = URL_VIDEOS, channelId = CHANNEL_ID, videoList = video_list, api_key=API_KEY)
# with open(FILE_VIDEO_STAT_LIST, 'w') as file:
#     json.dump(video_statistics, file)
    

#     # #Dowload video categories
# print('4. Saving of videos categories list has been started.')
# video_categories = get_video_categories(url=URL_VIDEO_CATEGORIES, api_key= API_KEY, category_ids= category_list)
# with open(FILE_VIDEO_CATEGORIES, 'w') as file:
#     json.dump(video_categories, file)


# Dodaj kod do uruchomienia aplikacji
# app.run_server(debug=True)
