import aiohttp
import time
import asyncio


async def request_api(url):
    headers = {'user-agent': 'ftw-bot'}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as r:
            response = await r.json()
    return response


async def get_latest_subreddit_posts(subreddit: str, prev_fetch_time: int) -> dict:
    profile_data = dict()
    all_data = []
    try:
        api_url = f"https://www.reddit.com/r/{subreddit}.json"
        about_url = f"https://www.reddit.com/r/{subreddit}/about.json"
        posts_data = (await request_api(api_url))["data"]["children"]
        subreddit_data = (await request_api(about_url))["data"]

        profile_data["profile_URL"] = f"https://www.reddit.com/r/{subreddit}"
        profile_data["profile_pic_URL"] = subreddit_data['icon_img']
        for post_data in posts_data:
            post_data = post_data['data']
            if post_data['created'] > prev_fetch_time:
                data = dict()
                data["post_id"] = post_data["id"]
                data["post_URL"] = f"https://reddit.com/r/{subreddit}/comments/{data['post_id']}"
                data["post_timestamp"] = post_data["created"]
                if post_data.get("url_overriden_by_dest") is not None:
                    data["post_media_URL"] = post_data["url_overridden_by_dest"]
                else:
                    data["post_media_URL"] = None
                if post_data.get("selftext") is not None:
                    data["post_text"] = post_data["selftext"]
                # 0 because there might be multiple images
                # if no image, there is no ["preview"]
                if post_data.get("preview") is not None:
                    data["post_media_URL"] = f'https://i.redd.it/{post_data["preview"]["images"][0]["source"]["url"][24:37]}.jpg'
                all_data.append({**profile_data, **data})
    except Exception as e:
        return {"data": repr(e), "success": False, "API": "Reddit", "username": subreddit, "prev_time": prev_fetch_time}
    return {"data": all_data, "success": True, "API": "Reddit", "username": subreddit, "prev_time": prev_fetch_time}


async def check_subreddit(subreddit: str) -> dict:
    try:
        about_url = f"https://www.reddit.com/r/{subreddit}/about.json"
        if (await request_api(about_url)).get("data"):
            return {"data": True, "success": True, "API": "Reddit", "username": subreddit}
        return {"data": False, "success": True, "API": "Reddit", "username": subreddit}
    except Exception as e:
        return {"data": False, "success": False, "API": "Reddit", "username": subreddit}


async def main():
    start = time.perf_counter()
    # print(await get_latest_subreddit_posts("earthporn", 1))
    print(await check_subreddit("earthporn"))
    finish = time.perf_counter()
    print(f'finished in {round(finish-start, 2)} seconds(s)')

if __name__ == '__main__':
    asyncio.run(main())
