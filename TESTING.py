from dotenv import dotenv_values
from pathlib import Path
import pandas as pd
import json
import pandas as pd

from src.data_processing.utilities import prepare_and_save_data
# config = dotenv_values(".env")
# # print( config['DATA_DIR'])
# # test = pd.read_json(config['DATA_DIR'])

# # test = pd.read_json(r'.data/raw_data/video_statistics_list.json')

# file_path = config['FILE_VIDEO_LIST']


# print(pd.read_json(file_path))
#    if download_iteration is not None and (count >= download_iteration or (count>0 and page_token is None)):
config = dotenv_values(".env")


dashboard_data_path = Path(config['DASHBOARD_DATA_FILE'])

if dashboard_data_path.exists():
    data = prepare_and_save_data(config['PATH_VIDEO_STATISTICS_LIST'], config['PATH_VIDEOS_CATEGORIES'])
    data.to_csv(config['DASHBOARD_DATA_FILE'])
else:
    raise ValueError(f'File with necessary data does not exist: {dashboard_data_path.name}')



