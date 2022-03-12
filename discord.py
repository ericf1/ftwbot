from twitterAPI import latestTweet
from instagramAPI import latestIGPost

import time

#input instagram username and twitter username
usernameIG = "thedivestudios"
usernameTwitter = "thedivestudios"

oldTweetLink = ""
oldIGLink = ""

def embeddedLink(link):
    print(link)

#Loop to run continously check
while(True):
    time.sleep(60)
    if(oldTweetLink):
        latestTweetLink = latestTweet(usernameTwitter)
        if(oldTweetLink != latestTweetLink):
            embeddedLink(latestTweetLink)
            oldTweetLink = latestTweetLink

    if(oldIGLink):
        latestIGLink = latestIGPost(usernameIG)
        if(oldIGLink != latestIGLink):
            embeddedLink(latestIGLink)
            oldIGLink = latestIGLink
        