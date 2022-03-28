_R='twitter'
_Q='instagram'
_P='post_text'
_O='post_isVideo'
_N='post_timestamp'
_M='post_URL'
_L='profile_pic_URL'
_K='profile_URL'
_J='user'
_I='channelID'
_H=False
_G=None
_F='post_media_URL'
_E='post_id'
_D='color'
_C='icon'
_B=True
_A='socials'
import tweepy,requests
from webbrowser import get
from dotenv import load_dotenv
import os
from turtle import update
from tinydb import TinyDB
from discord.ext import commands,tasks
import discord,logging,time
from datetime import datetime,timezone
load_dotenv()
socialsData={_Q:{_C:'https://www.instagram.com/static/images/ico/favicon-192.png/68d99ba29cc8.png',_D:13453419},_R:{_C:'https://cdn.cms-twdigitalassets.com/content/dam/developer-twitter/images/Twitter_logo_blue_`48.png',_D:44270}}
def getLatestInstagramPosts(username,prevFetchTime):
	B='edges';profileData=dict();allData=[]
	try:
		api_url=f"https://www.instagram.com/{username}/feed/?__a=1";userData=requests.get(api_url).json()['graphql'][_J];imagePostsData=userData['edge_owner_to_timeline_media'][B];videoPostsData=userData['edge_felix_video_timeline'][B];profileData[_K]=f"https://www.instagram.com/{username}";profileData[_L]=userData.get('profile_pic_url')
		def getPostData(postsData):
			D='edge_media_to_caption';C='taken_at_timestamp';A='node';i=0
			while i<len(postsData)and postsData[i][A][C]>prevFetchTime:
				try:
					data=dict();data[_E]=postsData[i][A]['shortcode'];data[_M]=f"https://www.instagram.com/p/{data[_E]}/";data[_N]=postsData[i][A][C];data[_O]=postsData[i][A]['is_video'];data[_F]=postsData[i][A]['display_url']
					if postsData[i][A][D][B]:data[_P]=postsData[i][A][D][B][0][A].get('text')
					allData.append({**profileData,**data});i+=1
				except Exception as e:print(repr(e),i,len(postsData))
		getPostData(imagePostsData);getPostData(videoPostsData)
	except Exception as e:print(repr(e));allData=_G
	return allData
def checkInstagramUser(username):
	if requests.get(f"https://www.instagram.com/{username}/feed/?__a=1"):return _B
	return _H
load_dotenv()
auth=tweepy.OAuthHandler(os.getenv('TWITTER_API_KEY'),os.getenv('TWITTER_API_SECRET_KEY'),os.getenv('TWITTER_ACCESS_TOKEN'),os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))
api=tweepy.API(auth,wait_on_rate_limit=_B)
def getLatestTwitterPosts(username,prevFetchTime):
	B='media';A='extended_entities';profileData=dict();allData=[]
	try:
		tweetsData=api.user_timeline(screen_name=f"{username}",count=20,tweet_mode='extended',exclude_replies=_B,include_rts=_H)
		if tweetsData[0]._json[_J]:
			userData=tweetsData[0]._json[_J];profileData['profile_name']=userData['name'];profileData[_K]=f"https://twitter.com/{username}";profileData[_L]=userData['profile_image_url_https'];i=0
			while i<len(tweetsData)and tweetsData[i].created_at.timestamp()>prevFetchTime:
				tweetData=tweetsData[i]._json;data=dict();data[_E]=tweetData['id'];data[_M]=f"https://twitter.com/{username}/status/{data[_E]}";data[_N]=tweetsData[i].created_at.timestamp()
				if tweetData.get(A)and tweetData[A].get(B)[0]:mediaData=tweetData[A][B][0];data[_O]=_B if mediaData['type']=='video'else _H;data[_F]=mediaData['media_url']
				data[_P]=tweetData['full_text'];allData.append({**profileData,**data});i+=1
	except Exception as e:print(repr(e));allData=_G
	return allData
def checkTwitterUser(username):
	try:api.get_user(screen_name=username);return _B
	except:return _H
db=TinyDB('database.json')
def doc(server_id):
	table=db.table(str(server_id))
	if not table.get(doc_id=1):table.insert({_A:{}},doc_ids=[1])
	for socialMedia in socialsData.keys():
		if socialMedia not in table.get(doc_id=1)[_A].keys():socialMediaObject=table.get(doc_id=1)[_A];socialMediaObject[socialMedia]=[];table.update({_A:socialMediaObject})
	return table.get(doc_id=1)
def updateDoc(server_id,obj):
	table=db.table(str(server_id))
	if not table.get(doc_id=1):table.insert({_A:{}},doc_ids=[1])
	for socialMedia in socialsData.keys():
		if socialMedia not in table.get(doc_id=1)[_A].keys():socialMediaObject=table.get(doc_id=1)[_A];socialMediaObject[socialMedia]=[];table.update({_A:socialMediaObject})
	table.update(obj,doc_ids=[1])
bot=commands.Bot(command_prefix='s!')
async def isAdmin(ctx):
	isAdmin=ctx.author.permissions_in(ctx.channel).administrator
	if not isAdmin:await ctx.send('You do not have permission to use this command.')
	return isAdmin
async def addReaction(ctx):await ctx.message.add_reaction('✅')
def to_lower(arg):return arg.lower()
@bot.event
async def on_ready():print(f"{bot.user.name} has connected to Discord!")
@tasks.loop(minutes=1.0)
async def myLoop():await bot.wait_until_ready();await update()
@bot.command()
async def ping(ctx):await ctx.send('Pong')
@bot.command()
async def setChannel(ctx,channel=_G):
	if not await isAdmin(ctx):return
	if channel:updateDoc(ctx.guild.id,{_I:channel.id})
	else:updateDoc(ctx.guild.id,{_I:ctx.channel.id})
	await addReaction(ctx)
@setChannel.error
async def setChannel_error(ctx,error):
	if isinstance(error,commands.ArgumentParsingError):await ctx.send('Incorrect usage of command: `s!setChannel #{text-channel}`')
@bot.command()
async def update(ctx=_G):
	A='prevTime'
	for serverID in db.tables():
		if not doc(serverID).get(_I):return
		channel=bot.get_channel(doc(serverID)[_I]);prevTime=doc(serverID).get(A)
		if prevTime:
			for socialMedia in socialsData.keys():
				platform=socialMedia.capitalize()
				for user in doc(serverID)[_A][socialMedia]:
					posts=globals()[f"getLatest{platform}Posts"](user,prevTime)
					if posts:
						for p in posts:
							embed=discord.Embed(description=p[_P],color=socialsData[socialMedia][_D],timestamp=datetime.utcfromtimestamp(p[_N]).replace(tzinfo=timezone.utc));embed.set_author(name=user,url=p[_K],icon_url=p[_L]);embed.set_footer(text=platform,icon_url=socialsData[socialMedia][_C])
							if p.get(_F):embed.set_image(url=p[_F])
							await channel.send(content=f"**New post from {user} on {platform}**\n{p[_M]}\n{'Click to view video'if p.get(_O)else''}",embed=embed)
		updateDoc(serverID,{A:int(time.time())})
	if ctx:await addReaction(ctx)
@bot.command()
async def add(ctx,socialMedia,user):
	if not await isAdmin(ctx):return
	if socialMedia not in socialsData.keys():await ctx.send(f"Invalid social media site entered. Available social media platforms are {', '.join(socialsData.keys())}.");return
	platform=socialMedia.capitalize()
	if not globals()[f"check{platform}User"](user):await ctx.send(f"`User {user}` does not exist on {platform}.");return
	if user in doc(ctx.guild.id)[_A][socialMedia]:await ctx.send(f"Updates from `{user}` already exist.");return
	socialsObj=doc(ctx.guild.id)[_A];socialsObj[socialMedia]=[*socialsObj[socialMedia],user];updateDoc(ctx.guild.id,{_A:socialsObj});await addReaction(ctx)
@add.error
async def add_error(ctx,error):
	if isinstance(error,commands.MissingRequiredArgument)or isinstance(error,commands.ArgumentParsingError):await ctx.send('Incorrect usage of command: `s!add {social-media-site} {username}`')
@bot.command()
async def remove(ctx,socialMedia,user):
	if not await isAdmin(ctx):return
	if socialMedia!=_R and socialMedia!=_Q:await ctx.send('Invalid social media site entered. Available social media platforms are `twitter` and `instagram`.');return
	if not user in doc(ctx.guild.id)[_A][socialMedia]:await ctx.send(f"Updates from `{user}` on {socialMedia} don't exist.");return
	users=doc(ctx.guild.id)[_A][socialMedia];users.pop(users.index(user));socialsObj=doc(ctx.guild.id)[_A];socialsObj[socialMedia]=users;updateDoc(ctx.guild.id,{_A:socialsObj});await addReaction(ctx)
@remove.error
async def remove_error(ctx,error):
	if isinstance(error,commands.MissingRequiredArgument)or isinstance(error,commands.ArgumentParsingError):await ctx.send('Incorrect usage of command: `s!remove {social-media-site} {username}`')
@bot.command()
async def list(ctx):
	if not await isAdmin(ctx):return
	for socialMedia in socialsData:embed=discord.Embed(title='Accounts',description='\n'.join(doc(ctx.guild.id)[_A][socialMedia]),color=socialsData[socialMedia][_D]);embed.set_footer(text=socialMedia.capitalize(),icon_url=socialsData[socialMedia][_C]);await ctx.send(embed=embed)
	await addReaction(ctx)
logger=logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler=logging.FileHandler(filename='discord.log',encoding='utf-8',mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
myLoop.start()
bot.run(os.getenv('DISCORD_TOKEN'))