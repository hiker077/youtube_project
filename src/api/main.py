import requests
import json
import logging
from typing import List, Dict, Tuple, Union, Optional

logger = logging.getLogger(__name__)


def fetch_response(url: str, params: Dict) -> Optional[Dict]:
    """
    Helper function to handle API requests and parse JSON responses.
    """
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during API request: {e}", exc_info=True)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response: {e}", exc_info=True)
    return None


def get_video_list(
    url: str,
    channel_id: str,
    api_key: str,
    video_duration: List[str],
    published_after: str,
    published_before: str,
    page_token: Optional[str] = None,
    download_limit: Optional[int] = None,
) -> List[str]:
    """ "
    Fetches a list of video IDs for a given channel.
    """
    videos_list = []
    count = 0

    logging.info("Download of video list has been started.")
    # try:
    for video_duration_type in video_duration:
        logger.info(f"Processing video type: {video_duration_type}.")
        while True:
            # if download_limit is not None and (
            #     count >= download_limit or (count > 0 and page_token is None)
            # ):
            if download_limit and count >= download_limit:
                logger.info("Dowload limit reach.")
                return videos_list

            params = {
                "part": "snippet",
                "type": "video",
                "videoDuration": video_duration_type,
                "channelId": channel_id,
                "key": api_key,
                "pageToken": page_token,
                "publishedAfter": published_after,
                "publishedBefore": published_before,
            }

            response_json = fetch_response(url, params)
            if response_json is None:
                break

            video_ids = [
                item["id"].get("videoId")
                for item in response_json.get("items", [])
                if item["id"].get("videoId")
            ]
            videos_list.extend(video_ids)
            page_token = response_json.get("nextPageToken")
            count += 1

            logger.info(
                f"Downloaded {len(videos_list)} videos. Page_token {page_token}"
            )

            if not page_token:
                break

    logger.info("Completed download of video list.")
    return videos_list


def get_video_statistics(
    url, channelId, videoList, api_key, part=("snippet", "contentDetails", "statistics")
):
    """
    Fetch video statistics for a list of video IDs.
    """
    results = []
    category_list = set()

    logging.info("Dowload of video statistics has been started.")
    try:
        for index, video_id in enumerate(videoList):
            params = {"part": part, "id": video_id, "key": api_key}
            response = requests.get(url, params=params)

            if response.status_code != 200:
                response_json = response.json()
                error_message = response_json.get("error", {}).get(
                    "message", "Unknown error"
                )
                raise Exception(
                    logger.error(
                        f"Error fetching videos {video_id} :{response.status_code} - {error_message}",
                        exc_info=True,
                    )
                )

            response_json = response.json()
            if "items" not in response_json:
                logger.info(f"No statistics available for video {video_id}. Skipping.")
                continue

            item = response_json["items"][0]
            snippet = item.get("snippet", {})
            statistic = item.get("statistics", {})
            content_details = item.get("contentDetails")

            results.append(
                {
                    "videoID": item.get("id", ""),
                    "publishedAt": snippet.get("publishedAt"),
                    "title": snippet.get("title"),
                    "tags": snippet.get("tags", []),
                    "viewCount": statistic.get("viewCount"),
                    "likeCount": statistic.get("likeCount"),
                    "commentCount": statistic.get("commentCount"),
                    "contentDetails": content_details.get("duration"),
                    "categoryId": snippet.get("categoryId"),
                }
            )

            if category_id := snippet.get("categoryId"):
                category_list.add(category_id)

            logger.info(f"VideoId: {video_id}. Iteration number: {index}")
        category_list = list(category_list)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return None

    logging.info("Dowload of video statisticts has been finished.")

    return results, category_list


def get_video_categories(url, category_ids, api_key):
    """
    Fetching the names of Youtube categories based on IDs.
    """

    category_list = []

    logging.info("Dowload of video categories has been started.")
    try:
        params = {"part": "snippet", "id": category_ids, "key": api_key}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            response_json = response.json()
            error_message = response_json.get("error", {}).get(
                "message", "Unknown error"
            )
            raise Exception(
                logging.error(
                    f"Error fetching categories: {response.status_code} - {error_message}"
                )
            )

        response_json = response.json()

        items = response_json.get("items", [])
        if not items:
            logging.info("No categories found in the response.")
            return []

        for item in items:
            category_id = item.get("id", "")
            category_title = item.get("snippet", {}).get("title", "Unknown Title")
            if category_id and category_title:
                category_list.append({"id": category_id, "title": category_title})

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return None

    logging.info("Dowload of video categories has been finished.")

    return category_list


def save_to_file(data, file_path):
    """
    Save data to file in JSON format.
    """
    try:
        logging.info(f"Saving data to file: {file_path}")
        with open(file_path, "w") as file:
            json.dump(data, file)
        logging.info("Data saved correctly.")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise
