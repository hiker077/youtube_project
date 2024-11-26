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


def get_video_list(url, channel_id, api_key, video_duration, published_after, published_before, page_token= None, dowload_iteration=None):
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
            if dowload_iteration is not None and (count > dowload_iteration or (count>0 and page_token is None)):
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
    results = []
    category_list = set()
    """
    This function dowload video statistic for each videoID defined on the input list. 
    """
    try:
        for index, video_id in enumerate(videoList):
            params = {'part': part, 'id': video_id, 'key': api_key}
            response = requests.get(url, params=params)
            response_json = response.json()
            
            
            if response.status_code != 200:
                raise Exception(f"Error fetching videos: {response.status_code} - {response_json.get('error', {}).get('message')}")
            
            if 'items' in response_json:
                
                item_snippet = response_json['items'][0]['snippet']
                item_statistic = response_json['items'][0]['statistics']
                item_content_etails = response_json['items'][0]['contentDetails']
                item_id = response_json['items'][0]['id']
                
                publishedAt = item_snippet.get('publishedAt')
                title = item_snippet.get('title')
                tags = item_snippet.get('tags', [])
                viewCount = item_statistic.get('viewCount')
                likeCount = item_statistic.get('likeCount')
                commentCount = item_statistic.get('commentCount')
                contentDetails = item_content_etails.get('duration')
                categoryId = item_snippet.get('categoryId')

                results.append({
                    'videoID': item_id,
                    'publishedAt': publishedAt,
                    'title': title,
                    'tags': tags,
                    'viewCount': viewCount,
                    'likeCount': likeCount,
                    'commentCount': commentCount,
                    'contentDetails': contentDetails,
                    'categoryId': categoryId
                })

                category_list.add(item_snippet['categoryId'])
                print(f'VideoId: {video_id}. Iteration number: {index}')
            else:
                print(f"Error fetching statistics for video {video_id}")

    except Exception as e:
        print("Something went wrong:", e)
        return None

    return results, category_list

#no needed 
def get_video_categories(url, list_of_id, api_key):
    """
    Dowload the dictiorany of YouTube videos's categories. 
    Return list of dict's. 
    """
    
    category_list = []

    try:
        params = {'part': 'snippet', 'id': list_of_id, 'key': api_key}
        response = requests.get(url, params=params)
        response_json = response.json()

        if response.status_code != 200:
                raise Exception(f"Error fetching videos: {response.status_code} - {response_json.get('error', {}).get('message')}")

        if 'items' in response_json:
            for item in response_json['items']:
                category_id = item['id']
                category_title = item['snippet']['title']
                category_list.append({'id': category_id, 'title': category_title})
        else:
            print("Error fetching video categories.")

    except Exception as e:
        print("Something went wrong:", e)
        return None

    return category_list