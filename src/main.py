from dotenv import dotenv_values
from pathlib import Path
import dash_bootstrap_components as dbc
from dash import Dash
import yaml
import logging
import logging.config

from api.main import (
    get_video_list,
    save_to_file,
    get_video_statistics,
    get_video_categories,
)
from data_processing.utilities import transform_datas

from dashboard.utilities import load_data
from dashboard.layout import create_layout
from dashboard.callbacks import register_callbacks

config = dotenv_values(".env")
config_share = dotenv_values(".env.share")

EXTERNAL_STYLESHEETS = [
    dbc.themes.BOOTSTRAP,
    "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.7.2/font/bootstrap-icons.min.css",
]

# Set up logging
with open(config_share["LOGGING_CONFIG"], "r") as file:
    config_logging = yaml.safe_load(file)
    logging.config.dictConfig(config_logging)

logger = logging.getLogger(__name__)


# def data_initialization():
#     video_list = get_video_list(
#         url=config_share["URL_SEARCH"],
#         channel_id=config["CHANNEL_ID"],
#         api_key=config["API_KEY"],
#         video_duration=[
#             config_share["VIDEO_DURATION_MEDIUM"],
#             config_share["VIDEO_DURATION_LONG"],
#         ],
#         published_after=config_share["PUBLISHED_AFTER"],
#         published_before=config_share["PUBLISHED_BEFORE"],
#         page_token=None,
#         download_limit=1,
#     )

#     output_file = Path(config_share["FILE_VIDEO_LIST"])
#     save_to_file(video_list, output_file)

#     video_statistics, category_list = get_video_statistics(
#         url=config_share["URL_VIDEOS"],
#         channelId=config["CHANNEL_ID"],
#         videoList=video_list,
#         api_key=config["API_KEY"],
#     )

#     output_file = Path(config_share["PATH_VIDEO_STATISTICS_LIST"])
#     save_to_file(video_statistics, output_file)

#     category_list = get_video_categories(
#         url=config_share["URL_VIDEO_CATEGORIES"],
#         category_ids=category_list,
#         api_key=config["API_KEY"],
#     )

#     save_to_file(category_list, Path(config_share["PATH_VIDEOS_CATEGORIES"]))

#     # Data preparation
#     data = transform_datas(
#         config_share["PATH_VIDEO_STATISTICS_LIST"],
#         config_share["PATH_VIDEOS_CATEGORIES"],
#     )
#     data.to_csv(config_share["DASHBOARD_DATA_FILE"])


# if config_share["DATA_DOWNLOAD"] == "True":
#     data_initialization()

# Run of dashboard
dashboard_data_path = Path(config_share["DASHBOARD_DATA_FILE"])
if dashboard_data_path.exists():
    data = load_data(dashboard_data_path)
else:
    raise ValueError(
        logging.error(
            f"File with necessary data does not exist: {dashboard_data_path.name}"
        )
    )


app = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
app.title = "YouTube Dashboard"
app.layout = create_layout(data, config_share["YOUTUBE_LOGO"])

register_callbacks(app)
if __name__ == "__main__":
    app.run_server(debug=True)
