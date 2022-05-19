import requests
import aiohttp
import asyncio


async def getLatestInstagramPosts(username, prevFetchTime):
    await asyncio.sleep(3)
    profileData = dict()
    allData = []
    try:
        async with aiohttp.ClientSession() as session:
            api_url = f"https://www.instagram.com/{username}/feed/?__a=1"
            async with session.get(api_url) as resp:
                response = await resp.json()
                userData = response["graphql"]["user"]
        imagePostsData = userData["edge_owner_to_timeline_media"]["edges"]
        videoPostsData = userData["edge_felix_video_timeline"]["edges"]

        profileData["profile_URL"] = f"https://www.instagram.com/{username}"
        profileData["profile_pic_URL"] = userData.get("profile_pic_url")

        def getPostData(postsData):
            i = 0
            while i < len(postsData) and postsData[i]["node"]["taken_at_timestamp"] > prevFetchTime:
                try:
                    data = dict()

                    data["post_id"] = postsData[i]["node"]["shortcode"]
                    data["post_URL"] = f"https://www.instagram.com/p/{data['post_id']}/"
                    data["post_timestamp"] = postsData[i]["node"]["taken_at_timestamp"]

                    data["post_isVideo"] = postsData[i]["node"]["is_video"]
                    data["post_media_URL"] = postsData[i]["node"]["display_url"]

                    if postsData[i]["node"]["edge_media_to_caption"]["edges"]:
                        data["post_text"] = postsData[i]["node"]["edge_media_to_caption"]["edges"][0]["node"].get(
                            "text")

                    allData.append({**profileData, **data})
                    i += 1
                except Exception as e:
                    print(repr(e), i, len(postsData))

        getPostData(imagePostsData)
        getPostData(videoPostsData)

    except Exception as e:
        print(repr(e))
        allData = None
    finally:
        await asyncio.sleep(3)
    return allData


def checkInstagramUser(username):
    if(requests.get(f"https://www.instagram.com/{username}/feed/?__a=1")):
        return True
    return False


async def main():
    print(await getLatestInstagramPosts('adele', 1))
if __name__ == "__main__":
    asyncio.run(main())
