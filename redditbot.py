import discord
import asyncpraw
import asyncio
import config

intents = discord.Intents.default()
intents.messages = True

bot = discord.Client(intents=intents)

reddit = asyncpraw.Reddit(client_id=config.settings["CLIENT_ID"],
                          client_secret=config.settings["SECRET_CODE"],
                          user_agent="Random_meme_bot/0.1.0")

memes = []
Timeout = 5
Id_channel = 1256627395226767363
Subreddit_name = "memes"
post_limit = 1

@bot.event
async def on_ready():
    global memes  # Добавлено объявление глобальной переменной
    channel = bot.get_channel(Id_channel)
    
    if channel is None:
        print(f"Не удалось найти канал с ID: {Id_channel}")
        return
    
    while True:
        await asyncio.sleep(Timeout)
        memes_submissions = await reddit.subreddit(Subreddit_name)
        memes_submissions = memes_submissions.new(limit=post_limit)
        async for item in memes_submissions:
            if item.title not in memes:
                memes.append(item.title)
                await channel.send(item.url)
                break

bot.run(config.settings["DISCORD_TOKEN"])