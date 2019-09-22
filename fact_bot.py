import os, random, sys, praw, discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
redditSecret = os.getenv('REDDIT_CLIENT_SECRET')
redditID = os.getenv('REDDIT_CLIENT_ID')
redditAgent = os.getenv('REDDIT_USER_AGENT')
redditPW = os.getenv('REDDIT_PW')
redditUName = os.getenv('REDDIT_USERNAME')
reddit = praw.Reddit(client_id=redditID,
                     client_secret=redditSecret,
                     user_agent=redditAgent,
                     username=redditUName,
                     password=redditPW)

# Discord client
client = commands.Bot(command_prefix='!') # !COMMAND_NAME args

# Bot events
# Function name must equal a valid event name
@client.event
async def on_ready():
    # client is the bot
    # client.user is the bot in the user object
    # Docs here for client https://discordpy.readthedocs.io/en/async/api.html#client
    print('Logged on as {0}!'.format(client.user.name))

# Bot commands
# Function name is the command name
@client.command(pass_context=True)
# c = context.*
async def ping(c):
    await c.channel.send('Wadup') 

@client.command(pass_context=True)
async def fact(c):
    # c.message = message YOU sent (!fact)
    # c.channel = the channel the message was sent in
    facts = open("parsedfacts.txt", "r")
    facts_list = [line.split() for line in facts]
    fact_arr = random.choice(facts_list)
    fact = ' '.join(fact_arr)
    await c.channel.send(fact)

@client.command(pass_context=True)
async def heart(c):
    await c.channel.send("i :heart: u {0}! :D".format(c.message.author.name))

@client.command(pass_context=True)
async def moarfacts(c, times):
    """Repeats a message multiple times, then combines it into one message"""
    msg = ""
    facts = open("parsedfacts.txt", "r")
    fact_list = []
    for line in facts:
        fact_list.append(line)
    for i in range(int(times)):
        msg += random.choice(fact_list) + '\n'
    await c.channel.send(msg)

@client.command(pass_context=True)
async def fetchposts(sub, sort, post_count):
    msg = ""
    posts = reddit.subreddit(sub).new(limit=int(post_count))
    for p in posts:
        msg += "Title: " + p.title + '\n' "Body: " + p.selftext + '\n'
    # if 'hot' in sort  :
    # if 'top' in sort:
    # if 'controversial in sort':
    # if 'gilded' in sort:
    print(msg)
client.run(token)