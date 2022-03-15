import requests


def latestIGPost(username):
    latestIGPostData = dict()
    try:
        api_url = f"https://www.instagram.com/{username}/feed/?__a=1"
        userData = requests.get(api_url).json()["graphql"]["user"]
        eRiC = userData["edge_owner_to_timeline_media"]["edges"][0]["node"]

        post_id = eRiC["shortcode"]
        latestIGPostData["link"] = f"https://www.instagram.com/p/{post_id}/"
        latestIGPostData["photo"] = eRiC["display_url"]
        # latestIGPostData["likes"] =
        print(eRiC)
        try:
            latestIGPostData["description"] = userData["edge_owner_to_timeline_media"][
                "edges"][0]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
        except:
            latestIGPostData["description"] = None
        latestIGPostData["timestamp"] = eRiC["taken_at_timestamp"]
        latestIGPostData["fullname"] = userData["full_name"]
    except:
        latestIGPostData["link"] = ""
        latestIGPostData["photo"] = None
        latestIGPostData["description"] = None
        latestIGPostData["timestamp"] = None
        latestIGPostData["fullname"] = None
    return latestIGPostData


"""
Profile Picture
Username
Post Description
Likes
First Image
Timestamp

"""


# testing method
# print(latestIGPost("edisonfang123")["link"])
# print(latestIGPost("edisonfang123")["photo"])
# print(latestIGPost("edisonfang123")["description"])
# print(latestIGPost("edisonfang123")["timestamp"])
# print(latestIGPost("edisonfang123")["fullname"])
latestIGPost("edisonfang123")
