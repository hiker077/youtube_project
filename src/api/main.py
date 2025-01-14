import requests
import json
import logging
from typing import List, Dict, Tuple, Optional, Any

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
    url: str,
    channelId: str,
    videoList: List[str],
    api_key: str,
    part: Tuple[str, ...] = ("snippet", "contentDetails", "statistics"),
) -> Tuple[List[Dict], List[str]]:
    """
    Fetch video statistics for a list of video IDs.

    Args:
        url (str): The API endpoint URL.
        channelId (str): Channel ID to fetch video statistics.
        videoList (List[str]): List of video IDs to fetch statistics.
        api_key (str): API key for authentication.
        part (Tuple[str, ...], optional): List of video parts to fetch. Defaults to ("snippet", "contentDetails", "statistics").

    Returns:
        Tuple[List[Dict], List[str]]: List of dictionaries with video statistics and list of category IDs.
    """
    results = []
    category_list = set()

    logging.info("Dowload of video statistics has been started.")
    for video_id in videoList:
        params = {"part": part, "id": video_id, "key": api_key}
        response_json = fetch_response(url, params)

        if not response_json or "items" not in response_json:
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

    logging.info("Completed download of video statisticts.")
    return results, list(category_list)


def get_video_categories(url: str, category_ids: List[str], api_key: str) -> List[Dict]:
    """
    Fetch names of Youtube categories based on IDs.

    Args:
        url (str): The API endpoint URL.
        category_ids (List[str]): List of category IDs to fetch.
        api_key (str): API key for authentication.

    Returns:
        List[Dict]: List of dictionaries with category ID and title.
    """
    if not category_ids:
        logging.info("No category IDs provided. Returning an empty list.")
        return []

    logging.info("Download of video categories started.")
    category_list = []
    params = {"part": "snippet", "id": ",".join(category_ids), "key": api_key}

    response_json = fetch_response(url, params)
    if not response_json:
        logging.info("No response received. Returning empty list.")
        return []

    items = response_json.get("items", [])
    if not items:
        logging.info("No categories found. Returning empty list.")
        return []

    for item in items:
        category_id = item.get("id", "")
        category_title = item.get("snippet", {}).get("title", "Unknown Title")
        if category_id and category_title:
            category_list.append({"id": category_id, "title": category_title})

    logging.info("Completed download of video categories.")
    return category_list


def save_to_file(data: Any, file_path: str) -> None:
    """
    Save data to file in JSON format.

    Args:
        data (Any): Data to be serialized and saved.
        file_path (str): Path to the file where data will be saved.
    """
    try:
        logging.info(f"Saving data to file: {file_path}")
        with open(file_path, "w") as file:
            json.dump(data, file)
        logging.info("Data saved correctly.")

    except ValueError as ve:
        logger.error(f"Data serialization error: {ve}", exc_info=True)
        raise

    except IOError as ioe:
        logger.error(f"File writing error: {ioe}", exc_info=True)
        raise

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise
