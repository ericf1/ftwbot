import aiohttp
import asyncio
from instagrapi import Client
from dotenv import load_dotenv
import os

load_dotenv()


class InstagramAPI:
    USERNAME = os.getenv("INSTAGRAM_USERNAME")
    PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

    def __init__(self):
        self.cl = Client()
        self.cl.load_settings("settings.json")
        self.cl.login(self.USERNAME, self.PASSWORD)
        self.cl.dump_settings("settings.json")

    async def get_latest_instagram_post(
        self, username: str, prev_fetch_time: int
    ) -> dict:
        profile_data = dict()
        all_data = []
        try:
            # await asyncio.sleep(1)
            userID = self.cl.user_id_from_username(username)
            info = self.cl.user_info(userID)

            # instagram can have up to 3 pinned posts
            image_posts_data = self.cl.user_medias(userID, 4)
            # video_posts_data = user_data["edge_felix_video_timeline"]["edges"]

            profile_data["profile_URL"] = f"https://www.instagram.com/{username}"
            profile_data["profile_pic_URL"] = info.profile_pic_url

            def get_post_data(posts_data):
                compared_time = prev_fetch_time

                for post_data in posts_data:
                    if int(post_data.taken_at.timestamp()) > compared_time:
                        try:
                            all_data.clear()
                            data = dict()

                            data["post_id"] = post_data.id
                            data[
                                "post_URL"
                            ] = f"https://www.instagram.com/p/{post_data.code}/"

                            compared_time = data[
                                "post_timestamp"
                            ] = post_data.taken_at.timestamp()

                            data["post_is_video"] = (
                                # media_type = 2 refers to any video, IGTV, or reel
                                True
                                if post_data.media_type == 2
                                else False
                            )
                            data["post_media_URL"] = post_data.thumbnail_url

                            if post_data.caption_text:
                                data["post_text"] = post_data.caption_text

                            all_data.append({**profile_data, **data})
                        except Exception as e:
                            print(repr(e), post_data)

            get_post_data(image_posts_data)
            # get_post_data(video_posts_data)

        except Exception as e:
            print(repr(e))
            return {
                "data": repr(e),
                "success": False,
                "API": "Instagram",
                "username": username,
                "prev_time": prev_fetch_time,
            }
        return {
            "data": all_data,
            "success": True,
            "API": "Instagram",
            "username": username,
            "prev_time": prev_fetch_time,
        }

    async def get_latest_instagram_story(
        self, username: str, prev_fetch_time: int
    ) -> dict():
        profile_data = dict()
        all_data = []

        try:
            # await asyncio.sleep(1)
            userID = self.cl.user_id_from_username(username)
            info = self.cl.user_info(userID)

            stories_data = self.cl.user_stories(userID)

            profile_data["profile_URL"] = f"https://www.instagram.com/{username}"
            profile_data["profile_pic_URL"] = info.profile_pic_url

            def get_stories_data(stories_data):
                for story_data in stories_data:
                    if int(story_data.taken_at.timestamp()) > prev_fetch_time:
                        try:
                            all_data.clear()
                            data = dict()

                            data["story_id"] = story_data.id
                            data[
                                "story_URL"
                            ] = f"https://www.instagram.com/stories/{username}/{story_data.pk}/"
                            data["post_timestamp"] = story_data.taken_at.timestamp()

                            data["post_is_video"] = (
                                # media_type = 2 refers to any video, IGTV, or reel
                                True
                                if story_data.media_type == 2
                                else False
                            )
                            data["post_media_URL"] = story_data.thumbnail_url

                            all_data.append({**profile_data, **data})
                        except Exception as e:
                            print(repr(e), story_data)

            get_stories_data(stories_data)

        except Exception as e:
            print(repr(e))
            return {
                "data": repr(e),
                "success": False,
                "API": "Instagram",
                "username": username,
                "prev_time": prev_fetch_time,
            }
        return {
            "data": all_data,
            "success": True,
            "API": "Instagram",
            "username": username,
            "prev_time": prev_fetch_time,
        }

    async def check_instagram_user(self, username: str) -> dict:
        await asyncio.sleep(1)
        try:
            if self.cl.user_id_from_username(username):
                # if username is invalid, it will throw an exception
                return {
                    "data": True,
                    "success": True,
                    "API": "Instagram",
                    "username": username,
                }
        except Exception as e:
            print(repr(e))
            return {
                "data": False,
                "success": False,
                "API": "Instagram",
                "username": username,
            }

    # async def request_api(self, username):
    #     async with aiohttp.ClientSession(cookies=self.cookies) as session:
    #         async with session.get(
    #             os.getenv("INSTAGRAM_LINK").format(username=username)
    #         ) as r:
    #             response = await r.json()
    #     return response


async def main():
    instagram_api = InstagramAPI()
    print(await instagram_api.get_latest_instagram_post("adele", 1))
    # print(await check_instagram_user('adele'))


if __name__ == "__main__":
    asyncio.run(main())
