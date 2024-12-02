# youtube_utils/api.py
import requests
import json


# def fetch_videos(url, channel_id, api_key, video_duration, published_after, published_before, page_token= None):
#     """
#     Funtion fetchs videos IDs for singl request.
#     """
#     params = {'part': 'snippet','type':'video','videoDuration': video_duration, 'channelId': channel_id, 'key': api_key, 'pageToken': page_token, 'publishedAfter': published_after, 'publishedBefore': published_before}
#     response = requests.get(url, params=params)
#     response_json = response.json()
#     video_ids = [item['id'].get('videoId') for item in response_json.get('items', []) if item['id'].get('videoId')]
#     page_token = response_json.get('nextPageToken')
#     return video_ids, page_token


def get_video_list(url, channel_id, api_key, video_duration, published_after, published_before, page_token= None, download_iteration=None):
    """"
    This function upload entire list of videoID's for defined channel_id. 
    Return the list. 
    """
    videos_list = []
    page_token = None
    count = 0

    try:
        while True:
            # Check if the download limit is reached or no more pages are available
            if download_iteration is not None and (count >= download_iteration or (count>0 and page_token is None)):
                    print('Task fisnished. Dowload limit was reached or there is no page_token.')
                    break
            
            # Fetch videos and update the list
            params = {'part': 'snippet','type':'video','videoDuration': video_duration, 'channelId': channel_id, 'key': api_key, 'pageToken': page_token, 'publishedAfter': published_after, 'publishedBefore': published_before}
            response = requests.get(url, params=params)
            response_json = response.json()
            video_ids = [item['id'].get('videoId') for item in response_json.get('items', []) if item['id'].get('videoId')]
            page_token = response_json.get('nextPageToken')
            videos_list.extend(video_ids)
            video_count = len(videos_list)          
            count +=1

            #Log progress
            print(f'Number of IDs in list {video_count} and page_token {page_token}')

            #Break if no more pages
            if page_token is None:
                    print('Task fisnished. Page token doesnt exist.')
                    break

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

    return videos_list




def get_video_statistics(url, channelId, videoList, api_key , part=('snippet', 'contentDetails', 'statistics')):
    """
    Download of single video statistics.
    Function returns list of statistics and category set.
    """
    results = []
    category_list = set()
 
    try:
        for index, video_id in enumerate(videoList):
            params = {'part': part, 'id': video_id, 'key': api_key}
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                response_json = response.json()
                error_message = response_json.get('error', {}).get('message', 'Unknown error')
                raise Exception(f"Error fetching videos {video_id} :{response.status_code} - {error_message}")
            
            response_json = response.json()
            if 'items' not in response_json:
                print(f"No statistics available for video {video_id}. Skipping.")
                continue
            
            item = response_json['items'][0]
            snippet = item.get('snippet', {})
            statistic = item.get('statistics', {})
            content_details = item.get('contentDetails')
    
            results.append({
                'videoID': item.get('id', ''),
                'publishedAt': snippet.get('publishedAt'),
                'title': snippet.get('title'),
                'tags': snippet.get('tags', []),
                'viewCount': statistic.get('viewCount'),
                'likeCount': statistic.get('likeCount'),
                'commentCount': statistic.get('commentCount'),
                'contentDetails': content_details.get('duration'),
                'categoryId': snippet.get('categoryId')
            })
            
            if category_id := snippet.get('categoryId'):
                category_list.add(category_id)

            print(f'VideoId: {video_id}. Iteration number: {index}')
       

    except Exception as e:
        print("Something went wrong:", e)
        return None

    return results, category_list


def get_video_categories(url, category_ids, api_key):
    """
    Fetching the names of Youtube categories based on IDs. 
    """

    category_list = []

    try:
        params = {'part': 'snippet', 'id': category_ids, 'key': api_key}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            response_json = response.json()
            error_message = response_json.get('error', {}).get('message', 'Unknown error')
            raise Exception(f"Error:{response.status_code} - {error_message}")

        response_json = response.json()
        
        items = response_json.get('items', [])
        if not items:
            print("No categories found in the response.")
            return []

        for item in items:
            category_id = item.get('id','')
            category_title = item.get('snippet', {}).get('title', 'Unknown Title')
            if category_id and category_title:
                category_list.append({'id': category_id, 'title': category_title})
        else:
            print("Error fetching video categories.")

    except Exception as e:
        print("Something went wrong:", e)
        return None

    return category_list