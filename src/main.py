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
from data_processing.utilities import transform_data

from dashboard.utilities import load_data
from dashboard.layout import create_layout
from dashboard.callbacks import register_callbacks

# Load configuration
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


def data_initialization():
    """
    Download and process data for the dashboard. This function checks whether
    the necessary data files already exist before running the download process.
    """
    processed_data_path = Path(config_share["DASHBOARD_DATA_FILE"])

    # Skip initialization if data already exists
    if processed_data_path.exists():
        logger.info("Processed data file already exists. Skipping data initialization.")
        return

    logger.info("Starting data initialization...")

    # Download video list
    video_list = get_video_list(
        url=config_share["URL_SEARCH"],
        channel_id=config["CHANNEL_ID"],
        api_key=config["API_KEY"],
        video_duration=[
            config_share["VIDEO_DURATION_MEDIUM"],
            config_share["VIDEO_DURATION_LONG"],
        ],
        published_after=config_share["PUBLISHED_AFTER"],
        published_before=config_share["PUBLISHED_BEFORE"],
        page_token=None,
        download_limit=1,
    )
    save_to_file(video_list, Path(config_share["FILE_VIDEO_LIST"]))

    # Download video statistics
    video_statistics, category_list = get_video_statistics(
        url=config_share["URL_VIDEOS"],
        channelId=config["CHANNEL_ID"],
        videoList=video_list,
        api_key=config["API_KEY"],
    )
    save_to_file(video_statistics, Path(config_share["PATH_VIDEO_STATISTICS_LIST"]))

    # Download category list
    categories = get_video_categories(
        url=config_share["URL_VIDEO_CATEGORIES"],
        category_ids=category_list,
        api_key=config["API_KEY"],
    )
    save_to_file(categories, Path(config_share["PATH_VIDEOS_CATEGORIES"]))

    # Data transformation and saving
    transformed_data = transform_data(
        config_share["PATH_VIDEO_STATISTICS_LIST"],
        config_share["PATH_VIDEOS_CATEGORIES"],
    )
    transformed_data.to_csv(processed_data_path, index=False)

    logger.info(
        "Data initialization complete. Processed data saved to %s", processed_data_path
    )


def run_dashboard():
    """
    Main function to set up and run the dashboard.
    """
    # Check if the processed data file exists
    processed_data_path = Path(config_share["DASHBOARD_DATA_FILE"])
    if not processed_data_path.exists():
        logger.error(
            "Processed data file not found: %s. Please run the data initialization first.",
            processed_data_path,
        )
        raise FileNotFoundError(
            f"Processed data file not found: {processed_data_path.name}"
        )

    # Load data for the dashboard
    data = load_data(processed_data_path)

    # Set up the Dash app
    app = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
    app.title = "YouTube Dashboard"
    app.layout = create_layout(data, config_share["YOUTUBE_LOGO"])
    register_callbacks(app)

    # Run the server
    app.run_server(debug=True)


if __name__ == "__main__":
    # Run the data initialization only if explicitly required
    if config_share.get("DATA_DOWNLOAD") == "True":
        data_initialization()

    # Start the dashboard
    run_dashboard()
