import aiohttp
import asyncio
import requests
from dotenv import load_dotenv
import os

load_dotenv()


class InstagramAPI:
    BASE_URL = 'https://www.instagram.com/'
    STORIES_UA = 'Instagram 123.0.0.21.114 (iPhone; CPU iPhone OS 11_4 like Mac OS X; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/605.1.15'
    LOGIN_URL = BASE_URL + 'accounts/login/ajax/'
    USERNAME = os.getenv('INSTAGRAM_USERNAME')
    PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

    def __init__(self):
        cur_session = requests.Session()
        cur_session.headers.update(
            {'Referer': self.BASE_URL, 'user-agent': self.STORIES_UA})
        req = cur_session.get(self.BASE_URL)
        cur_session.headers.update(
            {'X-CSRFToken': req.cookies["csrftoken"]})

        login_data = {'username': self.USERNAME, 'password': self.PASSWORD}
        login = cur_session.post(
            self.LOGIN_URL, data=login_data, allow_redirects=True)
        self.cookies = login.cookies

    async def get_latest_instagram_post(self, username: str, prev_fetch_time: int) -> dict:
        profile_data = dict()
        all_data = []
        try:
            # await asyncio.sleep(1)
            response = await self.request_api(username)
            user_data = response["graphql"]["user"]

            image_posts_data = user_data["edge_owner_to_timeline_media"]["edges"]
            # video_posts_data = user_data["edge_felix_video_timeline"]["edges"]

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

    async def check_instagram_user(self, username: str) -> dict:
        await asyncio.sleep(1)
        try:
            if not (await self.request_api(username)):
                return {"data": False, "success": True, "API": "Instagram", "username": username}
            return {"data": True, "success": True, "API": "Instagram", "username": username}
        except Exception as e:
            print(repr(e))
            return {"data": False, "success": False, "API": "Instagram", "username": username}

    async def request_api(self, username):
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.get(os.getenv("INSTAGRAM_LINK").format(username=username)) as r:
                response = await r.json()
        return response


async def main():
    instagram_api = InstagramAPI()
    print(await instagram_api.get_latest_instagram_post('adele', 1))
    # print(await check_instagram_user('adele'))
if __name__ == "__main__":
    for _ in range(10):
        asyncio.run(main())
