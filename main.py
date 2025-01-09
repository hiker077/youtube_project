import json
from pathlib import Path
from dotenv import dotenv_values
from dash import Dash
import dash_bootstrap_components as dbc

from src.api.main import get_video_list, get_video_statistics, get_video_categories
from src.data_processing.utilities import prepare_and_save_data
from src.dashboard.layout import create_layout
from src.dashboard.callbacks import register_callbacks
from src.dashboard.utilities import load_data

EXTERNAL_STYLESHEETS = [
    dbc.themes.BOOTSTRAP,
    "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.7.2/font/bootstrap-icons.min.css",
]

config = dotenv_values(".env")
config_share = dotenv_values(".env.share")

dashboard_data_path = Path(config_share["DASHBOARD_DATA_FILE"])


# Download of raw data
print("1. Dowload of video IDs started.")
video_list_long = get_video_list(
    url=config_share["URL_SEARCH"],
    api_key=config["API_KEY"],
    channel_id=config["CHANNEL_ID"],
    published_after=config_share["PUBLISHED_AFTER"],
    published_before=config_share["PUBLISHED_BEFORE"],
    video_duration=config_share["VIDEO_DURATION_LONG"],
)
video_list_medium = get_video_list(
    url=config_share["URL_SEARCH"],
    api_key=config["API_KEY"],
    channel_id=config["CHANNEL_ID"],
    published_after=config_share["PUBLISHED_AFTER"],
    published_before=config_share["PUBLISHED_BEFORE"],
    video_duration=config_share["VIDEO_DURATION_MEDIUM"],
)
video_list = video_list_long + video_list_medium
with open(config_share["FILE_VIDEO_LIST"], "w") as file:
    json.dump(video_list, file)

print("3. Saving of videos statistics list has been started.")
video_statistics, category_list = get_video_statistics(
    url=config_share["URL_VIDEOS"],
    channelId=config["CHANNEL_ID"],
    videoList=video_list,
    api_key=config["API_KEY"],
)
with open(config_share["PATH_VIDEO_STATISTICS_LIST"], "w") as file:
    json.dump(video_statistics, file)

print("4. Saving of videos categories list has been started.")
video_categories = get_video_categories(
    url=config_share["URL_VIDEO_CATEGORIES"],
    api_key=config["API_KEY"],
    category_ids=category_list,
)
with open(config_share["PATH_VIDEOS_CATEGORIES"], "w") as file:
    json.dump(video_categories, file)

# Data preparation
data = prepare_and_save_data(
    config_share["PATH_VIDEO_STATISTICS_LIST"], config_share["PATH_VIDEOS_CATEGORIES"]
)
data.to_csv(config_share["DASHBOARD_DATA_FILE"])

# Run of dashboard
if dashboard_data_path.exists():
    data = load_data(dashboard_data_path)
else:
    raise ValueError(
        f"File with necessary data does not exist: {dashboard_data_path.name}"
    )


# app = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
# app.title = "YouTube Dashboard"
# app.layout = create_layout(data, config["YOUTUBE_LOGO"])

# register_callbacks(app)
# if __name__ == "__main__":
#     app.run_server(debug=True)
