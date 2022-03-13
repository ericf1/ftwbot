import requests


def latestIGPost(username):
    latestIGPostData = dict()
    api_url = f"https://www.instagram.com/{username}/feed/?__a=1"
    data = requests.get(api_url).json()["graphql"]["user"]

    post_id = data["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"]
    latestIGPostData["link"] = f"https://www.instagram.com/p/{post_id}/"
    latestIGPostData["photo"] = data["edge_owner_to_timeline_media"]["edges"][0]["node"]["display_url"]
    latestIGPostData["description"] = data["edge_owner_to_timeline_media"][
        "edges"][0]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
    latestIGPostData["timestamp"] = data["edge_owner_to_timeline_media"]["edges"][0]["node"]["taken_at_timestamp"]
    latestIGPostData["fullname"] = data["full_name"]
    return latestIGPostData


# testing method
print(latestIGPost("adele")["link"])
print(latestIGPost("adele")["photo"])
print(latestIGPost("adele")["description"])
print(latestIGPost("adele")["timestamp"])
print(latestIGPost("adele")["fullname"])
