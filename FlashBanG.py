import discord
from discord.ext import commands
from discord import app_commands
import logging
from dotenv import load_dotenv
import os
from typing import Optional
from ro_py import Client
import gc
from userGet import *
from userStats import *

load_dotenv()

token = os.getenv('DISCORD_TOKEN')
guild = os.getenv('ID')
GUILD_ID = discord.Object(id=guild)
EPHEMERAL = False # Set this false if u wanna debug easier

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='*', intents=intents)

# --------------------------------- DOX A DUDE ---------------------------------

@bot.tree.command(name='getinfo', description='Get player info', guild=GUILD_ID)
@app_commands.describe(
    name='Name of player',
    id='ID of player'
)
async def getinfo(ctx: discord.Interaction, name: Optional[str] = None, id: Optional[int] = None):

    if name is None and id is None:
        await ctx.response.send_message('Provide a player name/id', ephemeral=EPHEMERAL)
        return

    if name is not None and id is not None:
        await ctx.response.send_message('Give one or the other im not making this thing 100 lines longer', ephemeral=EPHEMERAL)
        return
    
    client = Client()

    try:
        if name is not None:
            user = getUserByName(name)

        if id is not None:
            user = getUserByID(id)
        
        userName = user['name']
        userId = user['id']
        userDisplayName = user['displayName']

    
    except Exception as e:
        print(e)
        embed = discord.Embed(title=f'Could not find user',
                              color=0xff4444)
        await ctx.response.send_message(embed=embed, ephemeral=EPHEMERAL)
        return

    # gonna be a lot of get requests here
    userLevel = 0
    userKD = 0
    userKills = 0
    userDeaths = 0
    userPlaytime = 0
    userElo = 0

    embed = discord.Embed(title=f'📊 User Info: {userName} ({userDisplayName})',
                          description=f'User ID: `{userId}`',
                          color=0x44ff44)
    embed.add_field(name='📈 Game Stats',
                    value=f'**Level:** {userLevel}\n**KD:** {userKD}\n**Kills:** {userKills}\n**Deaths:** {userDeaths}\n**Playtime:** {userPlaytime}h\n**Elo:** {userElo}',
                    inline=False)

    await ctx.response.send_message(embed=embed)



    del user, client, ctx
    gc.collect()
    return

# --------------------------------- COMMANDS ---------------------------------

@bot.tree.command(name='ping', description='check if bot is running', guild=GUILD_ID)
async def ping(ctx: discord.Interaction):
    embed = discord.Embed(title='Bot is running',
                          color=0x44ff44)

    await ctx.response.send_message(embed=embed, ephemeral=EPHEMERAL)
    return

# --------------------------------- BOT SETUP ---------------------------------

@bot.event
async def on_ready():
    print('FlashBanG running')

    try:
        guild = GUILD_ID
        synced = await bot.tree.sync(guild=guild)
        print(f'synced {len(synced)} commands to {guild.id}')
        await bot.change_presence(activity=discord.Game(name='SIX SEVENNNN'))

    except Exception as e:
        print(f'Shit broke: {e}')

bot.run(token, log_handler=handler, log_level=logging.DEBUG)