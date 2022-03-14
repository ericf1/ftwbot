from instagramAPI import latestIGPost
from twitterAPI import latestTweet
previousPosts = open("posts.txt", "r+")
allPosts = previousPosts.readlines()

latestTweetData = latestTweet("elonmusk")
latestTweetDataLink = latestTweetData["link"]

if(allPosts[1] != latestTweetDataLink):
    print(latestTweetDataLink)
    allPosts[1] = latestTweetDataLink
    previousPosts.seek(0)
    previousPosts.writelines(allPosts)
    previousPosts.truncate()
