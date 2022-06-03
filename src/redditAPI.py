import requests

headers = {'user-agent':'ftw-bot'}
# response = requests.get('https://www.reddit.com/r/funny.json', headers=headers)
# json_response = response.json()
# for item in json_response['data']['children']:
#     print(item['data'])
def getLatestSubredditPosts(subreddit, prevFetchTime):
    profileData = dict()
    allData = []
    try:
        api_url = f"https://www.reddit.com/r/{subreddit}.json"
        print(api_url)
        about_url = f"https://www.reddit.com/r/{subreddit}/about.json"
        # subredditData = requests.get(about_url,headers=headers).json()['data']
        postsData = requests.get(api_url,headers=headers).json()['data']['children']
        # profileData["profile_URL"] = f"https://www.reddit.com/r/{subreddit}"
        # profileData["profile_pic_URL"] = subredditData['icon_img']
        print("here!")
        i = 0
        print(postsData[i]['data']['created'] > prevFetchTime)
        print(len(postsData) > i)
        while i < len(postsData) and postsData[i]['data']['created'] > prevFetchTime:
            postData = postsData[i]['data']
            print("im in !")
            data = dict()
            data["post_id"] = postData["id"]
            data["post_URL"] = f"https://reddit.com/r/{subreddit}/comments/{data['post_id']}"
            data["post_timestamp"] = postData['created']
            
            data["post_isVideo"] = postData["is_video"]
            try:
                if postData["url_overridden_by_dest"]:
                    data["post_media_URL"] = postData["url_overridden_by_dest"]
            except:
                data["post_media_URL"] = None
            if postData["selftext"]:
                data["post_text"] = postData["selftext"]
            
            allData.append({**profileData, **data})
            i += 1

            

    except Exception as e:
        print(repr(e))
        allData = None
    return allData   


