import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import dateutil.parser as dp
import time
import asyncio
load_dotenv()

youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))


async def get_latest_youtube_post(channel_id: str, prev_fetch_time: int) -> dict:
    try:
        profile_data = dict()
        all_data = []
        # it is a channelID if:
        if not (len(channel_id) == 24 and channel_id[0::1] == "UC"):
            request = youtube.search().list(
                part="id",
                type="channel",
                maxResults="1",
                q=channel_id
            )
            channel_id = request.execute().get(
                "items")[0].get('id').get('channelId')
        response = youtube.channels().list(part="contentDetails, snippet",
                                           maxResults="1", id=channel_id).execute()
        playlist_id = response.get('items')[0].get('contentDetails').get(
            'relatedPlaylists').get('uploads')
        profile_pic = response.get('items')[0].get('snippet').get(
            'thumbnails').get('default').get('url')
        title = response.get('items')[0].get('snippet').get('title')
        if(playlist_id is None):
            return []
        # formatting the data now
        profile_data["profile_name"] = title
        profile_data["profile_URL"] = f"https://www.youtube.com/channel/{channel_id}"
        profile_data["profile_pic_URL"] = profile_pic
        videosRequest = youtube.playlistItems().list(
            part="contentDetails, snippet",
            maxResults="8",
            playlistId=playlist_id
        ).execute()
        videos = videosRequest.get('items')

        for video in videos:
            # solution thanks to https://stackoverflow.com/questions/27245488/converting-iso-8601-date-time-to-seconds-in-python/27246418#27246418
            # ensures that the time is correct before we go through the details
            video_date_time = video.get(
                'contentDetails').get('videoPublishedAt')
            timestamp = dp.parse(video_date_time).timestamp()
            if timestamp > prev_fetch_time:
                data = dict()
                data["post_id"] = video.get('contentDetails').get('videoId')
                data["post_URL"] = f"https://www.youtube.com/watch?v={data['post_id']}/"
                data["post_timestamp"] = timestamp
                data["post_isVideo"] = True
                data["post_media_URL"] = f"https://i1.ytimg.com/vi/{data['post_id']}/sddefault.jpg"
                data["post_text"] = video.get('snippet').get('title')
                all_data.append({**profile_data, **data})
    except Exception as e:
        return {"data": repr(e), "success": False, "API": "YouTube", "username": channel_id, "prev_time": prev_fetch_time}
    return {"data": all_data, "success": True, "API": "YouTube", "username": channel_id, "prev_time": prev_fetch_time}


async def check_youtube_user(channel_id: str) -> dict:
    try:
        request = youtube.search().list(
            part="id",
            type="channel",
            maxResults="1",
            q=channel_id
        )
        response = request.execute().get("items")
        if response:
            return {"data": True, "success": True, "API": "YouTube", "username": channel_id}
        return {"data": False, "success": True, "API": "YouTube", "username": channel_id}
    except Exception as e:
        return {"data": False, "success": False, "API": "YouTube", "username": channel_id}


async def main():
    channel = 'ludwig'
    start = time.perf_counter()
    # print(await get_latest_youtube_post(channel, 1))
    print(await check_youtube_user(channel))
    finish = time.perf_counter()
    print(f'finished in {round(finish-start, 2)} seconds(s)')


# test the time of the fetch
if __name__ == '__main__':
    asyncio.run(main())
