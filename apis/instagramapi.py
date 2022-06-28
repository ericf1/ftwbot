import aiohttp
import asyncio
import binascii
import random


async def get_latest_instagram_post(username: str, prev_fetch_time: int) -> dict:
    profile_data = dict()
    all_data = []
    try:
        # await asyncio.sleep(1)
        response = await request_api(username)
        user_data = response["graphql"]["user"]

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

                        data["post_is_video"] = post_data["node"]["is_video"]
                        data["post_media_URL"] = post_data["node"]["display_url"]

                        if post_data["node"]["edge_media_to_caption"]["edges"]:
                            data["post_text"] = post_data["node"]["edge_media_to_caption"]["edges"][0]["node"].get(
                                "text")

                        all_data.append({**profile_data, **data})
                    except Exception as e:
                        print(repr(e), post_data)

        get_post_data(image_posts_data)
        # get_post_data(video_posts_data)

    except Exception as e:
        print(repr(e))
        return {"data": repr(e), "success": False, "API": "Instagram", "username": username, "prev_time": prev_fetch_time}
    return {"data": all_data, "success": True, "API": "Instagram", "username": username, "prev_time": prev_fetch_time}


async def check_instagram_user(username: str) -> dict:
    await asyncio.sleep(1)
    try:
        if not (await request_api(username)):
            return {"data": False, "success": True, "API": "Instagram", "username": username}
        return {"data": True, "success": True, "API": "Instagram", "username": username}
    except Exception as e:
        print(repr(e))
        return {"data": False, "success": True, "API": "Instagram", "username": username}

# generate_token and request_api are largely inspired by gallery_dl/extractor/instagram.py


def generate_token(size=16):
    """Generate a random token with hexadecimal digits"""
    data = random.getrandbits(size * 8).to_bytes(size, "big")
    return binascii.hexlify(data).decode()


async def request_api(username):
    csrf_token = generate_token()
    headers = {
        "Referer": "https://www.instagram.com/{}/".format(username),
        "X-CSRFToken": csrf_token,
        "X-IG-App-ID": "936619743392459",
        "X-IG-WWW-Claim": "0",
        "X-Requested-With": "XMLHttpRequest",
    }
    cookies = {
        "csrftoken": csrf_token,
    }

    async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
        async with session.get(f"https://www.instagram.com/{username}/feed/?__a=1") as r:
            response = await r.json()
    return response


async def main():
    # print(await get_latest_instagram_post('adele', 1))
    print(await check_instagram_user('adele'))
if __name__ == "__main__":
    for _ in range(10):
        asyncio.run(main())
