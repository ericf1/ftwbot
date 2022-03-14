import requests


def latestIGPost(username):
    latestIGPostData = dict()
    try:
        api_url = f"https://www.instagram.com/{username}/feed/?__a=1"
        data = requests.get(api_url).json()["graphql"]["user"]

        post_id = data["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"]
        latestIGPostData["link"] = f"https://www.instagram.com/p/{post_id}/"
        latestIGPostData["photo"] = data["edge_owner_to_timeline_media"]["edges"][0]["node"]["display_url"]
        try:
            latestIGPostData["description"] = data["edge_owner_to_timeline_media"][
                "edges"][0]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
        except:
            latestIGPostData["description"] = None
        latestIGPostData["timestamp"] = data["edge_owner_to_timeline_media"]["edges"][0]["node"]["taken_at_timestamp"]
        latestIGPostData["fullname"] = data["full_name"]
    except:
        latestIGPostData["link"] = ""
        latestIGPostData["photo"] = None
        latestIGPostData["description"] = None
        latestIGPostData["timestamp"] = None
        latestIGPostData["fullname"] = None
    return latestIGPostData


# testing method
# print(latestIGPost("edisonfang123")["link"])
# print(latestIGPost("edisonfang123")["photo"])
# print(latestIGPost("edisonfang123")["description"])
# print(latestIGPost("edisonfang123")["timestamp"])
# print(latestIGPost("edisonfang123")["fullname"])
