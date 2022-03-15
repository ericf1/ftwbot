import requests


def latestIGPost(username, prevFetchTime):
    data = dict()
    allData = []
    try:
        api_url = f"https://www.instagram.com/{username}/feed/?__a=1"
        userData = requests.get(api_url).json()["graphql"]["user"]
        postsData = userData["edge_owner_to_timeline_media"]["edges"]

        data["profile_URL"] = f"https://www.instagram.com/{username}"
        data["profile_pic_URL"] = userData.get("profile_pic_url")

        i = 0
        while True:
            try:
                data["post_timestamp"] = postsData[i]["node"].get(
                    "taken_at_timestamp")
                if data["post_timestamp"] < prevFetchTime:
                    break

                data["post_id"] = postsData[i]["node"].get("shortcode")
                data["post_URL"] = f"https://www.instagram.com/p/{data['post_id']}/"
                data["post_isVideo"] = postsData[i]["node"].get("is_video")

                if not data["post_isVideo"]:
                    data["post_picture"] = postsData[i]["node"].get(
                        "display_url")

                data["post_likes"] = postsData[i]["node"]["edge_liked_by"].get(
                    "count")
                data["post_description"] = postsData[i]["node"]["edge_media_to_caption"]["edges"][0]["node"].get(
                    "text")

                allData += data
                loopIndex += 1
            except:
                data = None
    except:
        allData = None
    return allData


# testing method
# print(latestIGPost("edisonfang123")["link"])
# print(latestIGPost("edisonfang123")["photo"])
# print(latestIGPost("edisonfang123")["description"])
# print(latestIGPost("edisonfang123")["timestamp"])
# print(latestIGPost("edisonfang123")["fullname"])
print(latestIGPost("adele"))
