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
                    data["post_timestamp"] = postsData[i]["node"].get(
                        "taken_at_timestamp")

                    data["post_id"] = postsData[i]["node"].get(
                        "shortcode")
                    data["post_URL"] = f"https://www.instagram.com/p/{data['post_id']}/"

                    data["post_isVideo"] = postsData[i]["node"].get(
                        "is_video")
                    if data["post_isVideo"]:
                        data["post_video_frame"] = postsData[i]["node"].get(
                            "display_url")
                        data["post_video_URL"] = postsData[i]["node"].get(
                            "video_url")
                    else:
                        data["post_picture_URL"] = postsData[i]["node"].get(
                            "display_url")
                        data["post_likes"] = postsData[i]["node"]["edge_liked_by"].get(
                            "count")
                    if postsData[i]["node"]["edge_media_to_caption"]["edges"]:
                        data["post_description"] = postsData[i]["node"]["edge_media_to_caption"]["edges"][0]["node"].get(
                            "text")

                    # print(i, data["post_timestamp"])

                    allData.append({**profileData, **data})
                    i += 1

                except Exception as e:
                    print(repr(e), i, len(postsData))

        getPostData(imagePostsData)
        getPostData(videoPostsData)

    except Exception as e:
        print(repr(e))
        allData = None
    return allData


# latestIGPosts("edisonfang123", 1647231250)
# latestIGPosts("edisonfang123", 0)
