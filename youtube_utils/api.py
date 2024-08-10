# youtube_utils/api.py
import requests
import json


def fetch_videos(url, channel_id, api_key, max_results, video_duration, page_token= None):
    """Can be long or medium
    Test2  asdasd
    TEst 3
    """
    params = {'part': 'snippet', 'type':'video','videoDuration': video_duration, 'channelId': channel_id, 'key': api_key, 'maxResults': max_results, 'pageToken': page_token}
    response = requests.get(url, params=params)
    response_json = response.json()
    video_ids = [item['id'].get('videoId') for item in response_json.get('items', []) if item['id'].get('videoId')]
    page_token = response_json.get('nextPageToken')


    return video_ids, page_token


def get_video_list(url, api_key, maxResults, channel_id, video_duration, dowload_iteration=None):
    """"
    This function upload entire list of videoID's for defined channel_id. 
    Return the list. 
    """
    
    videos_list = []
    page_token = None

    try:
        ##temp litmit of dowloads
        count = 1
        while True:
            # if response.status_code != 200:
            #     raise Exception(f"Error fetching videos: {response.status_code} - {response_json.get('error', {}).get('message')}")
            ##change to logg later 
            if dowload_iteration is not None:
                if count > dowload_iteration or (count>1 and page_token is None):
                    print('Task fisnished. Dowload limit was reached or there is no page_token.')
                    break
                    
                else:
                    video_ids, page_token = fetch_videos(url, channel_id, api_key, maxResults, video_duration, page_token)
                    # video_ids = [item['id'].get('videoId') for item in response_json.get('items', []) if item['id'].get('videoId')]
                    videos_list.extend(video_ids)
                    video_count = len(videos_list)
                    count +=1
                    print(f'Number of IDs in list {video_count} and page_token {page_token}')
            else:
                if count>1 and page_token is None:
                    print('Task fisnished. Page token doesnt exist.')
                    break
                else: 
                    video_ids, page_token = fetch_videos(url, channel_id, api_key, maxResults, video_duration, page_token)
                    # video_ids = [item['id'].get('videoId') for item in response_json.get('items', []) if item['id'].get('videoId')]
                    videos_list.extend(video_ids)
                    video_count = len(videos_list)
                    count +=1
                    print(f'Number of IDs in list {video_count} and page_token {page_token}')

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

    return videos_list



def get_video_statistics(url, channelId, videoList, api_key, part=('snippet', 'contentDetails', 'statistics')):
    results = []
    category_list = set()
    """
    This function dowload video statistic for each videoID defined on the input list. 
    """

    try:
        for video_id in videoList:
            params = {'part': part, 'id': video_id, 'key': api_key}
            response = requests.get(url, params=params)
            response_json = response.json()
            
            if response.status_code != 200:
                raise Exception(f"Error fetching videos: {response.status_code} - {response_json.get('error', {}).get('message')}")
            
            if 'items' in response_json:
                item = response_json['items'][0]['snippet']
                publishedAt = item['publishedAt']
                title = item['title']
                tags = item.get('tags', [])
                viewCount = response_json['items'][0]['statistics']['viewCount']
                likeCount = response_json['items'][0]['statistics']['likeCount']
                commentCount = response_json['items'][0]['statistics']['commentCount']
                contentDetails = response_json['items'][0]['contentDetails']['duration']
                categoryId = item['categoryId']
                results.append({
                    'publishedAt': publishedAt,
                    'title': title,
                    'tags': tags,
                    'viewCount': viewCount,
                    'likeCount': likeCount,
                    'commentCount': commentCount,
                    'contentDetails': contentDetails,
                    'categoryId': categoryId
                })
                category_list.add(item['categoryId'])
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