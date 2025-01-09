from dotenv import dotenv_values
from pathlib import Path
import json

from api.main import get_video_list, get_video_statistics
from api.config import (
    URL_SEARCH,
    URL_VIDEOS,
    PUBLISHED_AFTER,
    PUBLISHED_BEFORE,
)


config = dotenv_values(".env")
config_share = dotenv_values(".env.share")

dashboard_data_path = Path(config_share["DASHBOARD_DATA_FILE"])


def save_to_file(data, file_path):
    """
    Zapis danych do pliku JSON.
    """
    try:
        with open(file_path, "w") as file:
            json.dump(data, file)
        # logger.info(f"Dane zapisane do pliku: {file_path}")
    except Exception as e:
        print(e)
        # logger.error(f"Nie udało się zapisać danych do pliku {file_path}: {e}")
        raise


def download_video_list(config, config_share, video_duration):
    """
    Pobieranie listy wideo na podstawie konfiguracji.
    """
    # logger.info("Pobieranie listy wideo.")
    print("Start downloading video list")
    video_list = []
    for duration_value in video_duration:
        # logger.info(f"Pobieranie wideo o długości: {duration}.")
        video_list.extend(
            get_video_list(
                url=URL_SEARCH,
                api_key=config["API_KEY"],
                channel_id=config["CHANNEL_ID"],
                published_after=PUBLISHED_AFTER,
                published_before=PUBLISHED_BEFORE,
                video_duration=duration_value,
            )
        )
    video_list = list(set(video_list))
    output_file = Path(config_share["FILE_VIDEO_LIST"])
    # logger.info(f"Zapis listy wideo do pliku: {output_file}.")
    save_to_file(video_list, output_file)
    # logger.info("Pobieranie listy wideo zakończone.")
    return video_list


# download_video_list(config, config_share, video_duration=VIDEO_DURATION)


def download_video_statistics(video_list, config_share, config):
    """
    Pobieranie statystyk wideo.
    """
    # logger.info("Pobieranie statystyk wideo.")
    video_statistics, category_list = get_video_statistics(
        url=URL_VIDEOS,
        channelId=config["CHANNEL_ID"],
        videoList=video_list,
        api_key=config["API_KEY"],
    )
    output_file_video_statistics = Path(config_share["PATH_VIDEO_STATISTICS_LIST"])
    save_to_file(video_statistics, output_file_video_statistics)
    output_file_category_list = Path(config_share["PATH_VIDEOS_CATEGORIES"])
    save_to_file(category_list, output_file_category_list)
    return video_statistics, category_list


# test
with open(config_share["FILE_VIDEO_LIST"], "r") as file:
    video_list = json.load(file)


video_statistics, category_list = download_video_statistics(
    video_list, config_share, config
)


# Działa pobierania listy wideo i statystyk wideo.
# To do:
# w api.main dodać save_to_file
# dodać zapisywanie i config w api.main zamist w głownym pliku
# save param yes/no
# refactoring pozostałych mainów
