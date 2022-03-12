import requests


def latestIGPost(username):
    api_url = f"https://www.instagram.com/{username}/feed/?__a=1"
    data = requests.get(api_url).json()[
        "graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]
    latestIGPostData = dict()
    post_id = data["shortcode"]
    latestIGPostData["link"] = f'https://www.instagram.com/p/{post_id}/'
    latestIGPostData["photo"] = data["display_url"]
    latestIGPostData["description"] = data["edge_media_to_caption"]["edges"][0]["node"]["text"]
    latestIGPostData["timestamp"] = data["taken_at_timestamp"]
    return latestIGPostData


# testing method
print(latestIGPost('adele')["photo"])
