import discord
from discord.ext import tasks
import asyncio
import humanize
from solana.rpc.async_api import AsyncClient
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
token = ""
client = discord.Client(activity=discord.Activity(type=discord.ActivityType.watching, name="?"), intents=intents)
mainnet = "https://api.mainnet-beta.solana.com"
devnet = "https://api.devnet.solana.com"
testnet = "https://api.testnet.solana.com/"

@client.event
async def on_ready():
    print("TPS BOT ON")

@client.event
async def on_guild_join(guild):
    channel = client.get_channel(980667426951819314)
    embed = discord.Embed(title="Joined a new guild!", description=f"**{guild.name}**\n\n{guild.description}", color=discord.Color.dark_purple())
    embed.add_field(name="Members", value=f"{guild.member_count}")
    embed.add_field(name="Date created", value=f"{guild.created_at}")
    try:
        embed.add_field(name="Owner", value=f"{guild.owner}\n{guild.owner.id}")
    except:
        embed.add_field(name="Owner", value="None")
    embed.set_footer(text=f"{guild.id}")
    try:
        embed.set_thumbnail(url=guild.icon.url)
    except:
        pass
    try:
        embed.set_image(url=guild.banner_url)
    except:
        pass
    await channel.send(embed=embed)

@client.event
async def on_guild_remove(guild):
    channel = client.get_channel(980667426951819314)
    embed = discord.Embed(title="Left a guild!", description=f"**{guild.name}**\n\n{guild.description}", color=discord.Color.dark_purple())
    embed.add_field(name="Members", value=f"{guild.member_count}")
    embed.add_field(name="Date created", value=f"{guild.created_at}")
    try:
        embed.add_field(name="Owner", value=f"{guild.owner}\n{guild.owner.id}")
    except:
        embed.add_field(name="Owner", value="None")
    embed.set_footer(text=f"{guild.id}")
    try:
        embed.set_thumbnail(url=guild.icon.url)
    except:
        pass
    try:
        embed.set_image(url=guild.banner_url)
    except:
        pass
    await channel.send(embed=embed)

@tasks.loop(minutes=1)
async def update():
    async with AsyncClient(mainnet) as tclient:
        change = []
        TPS = 0
        for i in range(60):
            try:
                block1 = await tclient.get_transaction_count(commitment="finalized")
                await asyncio.sleep(1)
                block2 = await tclient.get_transaction_count(commitment="finalized")
                change.append(block2["result"] - block1["result"])
            except Exception as e:
                print(e)
        try:
            TPS = round(sum(change)/len(change))
            strTPS = humanize.intcomma(TPS)    
        except Exception as e:
            print(e)
            return
        if TPS >= 1500:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{strTPS} ✅"))
        if TPS < 1500 and TPS >= 1000:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{strTPS} ⚠️"))
        if TPS < 1000 and TPS > 150:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{strTPS} ❌"))
        if TPS <= 150:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{strTPS} 💀"))

update.start()
client.run(token)
