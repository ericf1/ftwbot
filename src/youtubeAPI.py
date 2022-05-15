import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import dateutil.parser as dp
import time
load_dotenv()

credentials = os.getenv('YOUTUBE_API_KEY')

youtube = build('youtube', 'v3', developerKey=credentials)


def getLatestYouTubePosts(channelID, prevFetchTime):
    profileData = dict()
    allData = []
    # it is a channelID if:
    if not (len(channelID) == 24 and channelID[0::1] == "UC"):
        request = youtube.search().list(
            part="id",
            type="channel",
            maxResults="1",
            q=channelID
        )
        channelID = request.execute().get(
            "items")[0].get('id').get('channelId')
    response = youtube.channels().list(part="contentDetails, snippet",
                                       maxResults="1", id=channelID).execute()
    playlistID = response.get('items')[0].get('contentDetails').get(
        'relatedPlaylists').get('uploads')
    profilePic = response.get('items')[0].get('snippet').get(
        'thumbnails').get('default').get('url')
    title = response.get('items')[0].get('snippet').get('title')
    if(playlistID is None):
        return []
    # formatting the data now
    profileData["profile_name"] = title
    profileData["profile_URL"] = f"https://www.youtube.com/channel/{channelID}"
    profileData["profile_pic_URL"] = profilePic
    videosRequest = youtube.playlistItems().list(
        part="contentDetails, snippet",
        maxResults="8",
        playlistId=playlistID
    ).execute()
    videos = videosRequest.get('items')

    for video in videos:
        # solution thanks to https://stackoverflow.com/questions/27245488/converting-iso-8601-date-time-to-seconds-in-python/27246418#27246418
        # ensures that the time is correct before we go through the details
        # print(video)
        videoDateTime = video.get('contentDetails').get('videoPublishedAt')
        timestamp = dp.parse(videoDateTime).timestamp()
        if timestamp > prevFetchTime:
            data = dict()
            data["post_id"] = video.get('contentDetails').get('videoId')
            data["post_URL"] = f"https://www.youtube.com/{data['post_id']}/"
            data["post_timestamp"] = timestamp
            data["post_isVideo"] = True
            data["post_media_URL"] = f"https://i1.ytimg.com/vi/{data['post_id']}/sddefault.jpg"
            data["post_text"] = video.get('snippet').get('title')
            allData.append({**profileData, **data})
    print(allData)


def checkYouTubeUser(channelID):
    response = youtube.channels().list(part="status", maxResults="1", id=channelID
                                       ).execute()
    if(response.get('pageInfo').get('totalResults') == 0):
        return False
    return True


# test the time of the fetch
if __name__ == '__main__':
    channel = ''

    start = time.perf_counter()
    getLatestYouTubePosts(channel, 1)
    finish = time.perf_counter()
    print(f'finished in {round(finish-start, 2)} seconds(s)')
