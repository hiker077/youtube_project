from pathlib import Path

BASE_DIR = Path.cwd() 
RAW_DATA_DIR = BASE_DIR / 'data' / 'raw_data'
FILE_VIDEO_LIST = RAW_DATA_DIR / 'video_list.json'
FILE_VIDEO_STAT_LIST = RAW_DATA_DIR / 'video_statistics_list.json'
FILE_VIDEO_CATEGORIES = RAW_DATA_DIR / 'video_categories.json'

#API_KEY = 'AIzaSyDBk-6UYCERAyG3v6KCu_QFomytZvt6kyo' ##ProjectYoutube2
API_KEY ='AIzaSyANkwKbzmirDS6ffLFi-BxCmBLiLqqG0TY'
CHANNEL_ID = 'UClhEl4bMD8_escGCCTmRAYg'
URL_SEARCH = 'https://www.googleapis.com/youtube/v3/search'
URL_VIDEOS = 'https://www.googleapis.com/youtube/v3/videos'
URL_VIDEO_CATEGORIES = 'https://www.googleapis.com/youtube/v3/videoCategories'
# MAX_RESULTS = 5  # MAX results per request 
PUBLISHED_AFTER = '2024-11-11T00:00:00Z'
PUBLISHED_BEFORE = '2024-11-25T00:00:00Z'
DOWNLOAD_ITERATION=1
VIDEO_DURATION_MEDIUM = 'medium'
VIDEO_DURATION_LONG = 'long'
PATH_VIDEO_STATISTICS_LIST = 'data/raw_data/video_statistics_list.json'
PATH_VIDEOS_CATEGORIES = 'data/raw_data/video_categories.json'
PATH_DASHBOARD_DATA = 'data/dashboard_data/'