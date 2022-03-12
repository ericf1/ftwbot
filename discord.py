from twitterAPI import latestTweet
from instagramAPI import latestIGPost

import time

usernameIG = "thedivestudios"
usernameTwitter = "thedivestudios"

oldTweetLink = ""
oldIGLink = ""

onIG = True
onTwitter = False

def embeddedLink(link):
    print(link)

#Loop to run continously check
while(True):
    time.sleep(60)
    if(onIG):
        latestTweetLink = latestTweet(usernameTwitter)
        if(oldTweetLink != latestTweetLink):
            embeddedLink(latestTweetLink)
        oldTweetLink = latestTweetLink

    if(onTwitter):
        latestIGLink = latestIGPost(usernameIG)
        if(oldIGLink != latestIGLink):
            embeddedLink(latestIGLink)
        oldIGLink = latestIGLink