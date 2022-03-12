import requests

def latestIGPost(username):
    api_url = f"https://www.instagram.com/{username}/feed/?__a=1"
    data = requests.get(api_url)
    post_id = data.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"]
    return f'https://www.instagram.com/p/{post_id}/'

#testing method
print(latestIGPost('adele'))