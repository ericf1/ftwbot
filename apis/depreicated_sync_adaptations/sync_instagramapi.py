import requests


def get_latest_instagram_post(username, prev_fetch_time):
    profile_data = dict()
    all_data = []
    try:
        api_url = f"https://www.instagram.com/{username}/feed/?__a=1"
        user_data = requests.get(api_url).json()["graphql"]["user"]

        image_posts_data = user_data["edge_owner_to_timeline_media"]["edges"]
        video_posts_data = user_data["edge_felix_video_timeline"]["edges"]

        profile_data["profile_URL"] = f"https://www.instagram.com/{username}"
        profile_data["profile_pic_URL"] = user_data.get("profile_pic_url")

        def get_post_data(posts_data):
            for post_data in posts_data:
                if post_data["node"]["taken_at_timestamp"] > prev_fetch_time:
                    try:
                        data = dict()

                        data["post_id"] = post_data["node"]["shortcode"]
                        data["post_URL"] = f"https://www.instagram.com/p/{data['post_id']}/"
                        data["post_timestamp"] = post_data["node"]["taken_at_timestamp"]

                        data["post_isVideo"] = post_data["node"]["is_video"]
                        data["post_media_URL"] = post_data["node"]["display_url"]

                        if post_data["node"]["edge_media_to_caption"]["edges"]:
                            data["post_text"] = post_data["node"]["edge_media_to_caption"]["edges"][0]["node"].get(
                                "text")

                        all_data.append({**profile_data, **data})
                    except Exception as e:
                        print(repr(e), post_data)

        get_post_data(image_posts_data)
        get_post_data(video_posts_data)

    except Exception as e:
        print(repr(e))
        all_data = []
    return all_data


def check_instagram_user(username):
    if(requests.get(f"https://www.instagram.com/{username}/feed/?__a=1")):
        return True
    return False


def main():
    print(get_latest_instagram_post('adele', 1))


if __name__ == "__main__":
    main()
