from platform import node
import requests


def getLatestIGPosts(username, prevFetchTime):
    profileData = dict()
    allData = []
    try:
        api_url = f"https://www.instagram.com/{username}/feed/?__a=1"
        userData = requests.get(api_url).json()["graphql"]["user"]
        imagePostsData = userData["edge_owner_to_timeline_media"]["edges"]
        videoPostsData = userData["edge_felix_video_timeline"]["edges"]

        profileData["profile_URL"] = f"https://www.instagram.com/{username}"
        profileData["profile_pic_URL"] = userData.get("profile_pic_url")

        def getPostData(postsData):
            i = 0
            while i < len(postsData) and postsData[i]["node"].get(
                    "taken_at_timestamp") > prevFetchTime:
                try:
                    data = dict()

                    data["post_id"] = postsData[i]["node"]["shortcode"]
                    data["post_URL"] = f"https://www.instagram.com/p/{data['post_id']}/"
                    data["post_timestamp"] = postsData[i]["node"]["taken_at_timestamp"]

                    data["post_isVideo"] = postsData[i]["node"]["is_video"]
                    if data["post_isVideo"]:
                        data["post_video_frame_URL"] = postsData[i]["node"]["display_url"]
                        data["post_video_URL"] = postsData[i]["node"]["video_url"]
                    else:
                        data["post_picture_URL"] = postsData[i]["node"]["display_url"]

                    if postsData[i]["node"]["edge_media_to_caption"]["edges"]:
                        data["post_text"] = postsData[i]["node"]["edge_media_to_caption"]["edges"][0]["node"].get(
                            "text")

                    data["post_likes"] = postsData[i]["node"]["edge_liked_by"].get(
                        "count")

                    print(i)
                    # print(data["post_URL"])
                    print({**profileData, **data})

                    allData.append(
                        {**profileData, **data})
                    i += 1
                except Exception as e:
                    print(repr(e), i, len(postsData))

        getPostData(imagePostsData)
        getPostData(videoPostsData)

    except Exception as e:
        print(repr(e))
        allData = None
    return allData


getLatestIGPosts("edisonfang123", 1647662400)
# getLatestIGPosts("edisonfang123", 0)
