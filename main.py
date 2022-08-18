"""

Welcome 👋🏼!

This repl contains all of source code of the GoBot Discord bot. 

Please consider adding our bot to your discord server to support our work.
Invite link: https://discord.com/api/oauth2/authorize?client_id=963786329831911464&permissions=8&scope=bot (copy and paste into browser)

😊 Happy coding!

  — Sincerely, FoxyCoder (co-owner of the bot)

"""

#[----------IMPORTS----------]
import discord
from termcolor import colored
from discord.ext import commands
import os
import json
from Cogs.init import Init
from Cogs.info import Info
from Cogs.moderation import Moderation
from Cogs.errors import Errors
from Cogs.fun import Fun
from Cogs.math import Math
from Cogs.giveaways import Giveaways
from Cogs.polls import Polls
from Cogs.bomb import Bomb
from Cogs.gleveling import Leveling
from Cogs.localleveling import LocalLeveling
from Cogs.gleaderboard import Leaderboard
from Cogs.localleaderboard import LLeaderboard
from Cogs.reactions import Reactions
from Cogs.welcome import Welcome
from Cogs.blackjack import Blackjack
from Cogs.embeds import Embeds
from datetime import datetime
from Cogs.afk import AFK
from Cogs.tictactoe import Tic
from Cogs.leaver import Leaver
from Cogs.vote_tracker import VoteTracker
from Cogs.counting import Counting
import asyncio
from Cogs.util import Util
from Other.hosting import keep_alive
from Cogs.button_template import Buttons
import time
import threading
# from datetime import datetime
# from datetime import date
# import time
# from discord_ui import Components, Button, UI


#[----------PREFIXES----------]
def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]


#[----------BOT----------]
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=get_prefix,
                      help_command=None,
                      intents=intents)

# im explaning code to evo

#[----------EVENTS----------]
@client.event
async def on_ready():
  os.system("clear")
  with open('servers.json', 'r') as f:
    data = json.load(f)
  data = {}
  for guild in client.guilds:
    guild_obj = await client.fetch_guild(guild.id)
    #guild = await client.fetch_guild()

    def remove_unicode(text):
      new_text = text
      for letter in text:  
        if ord(letter) < 20 or ord(letter) > 126:
          new_text = new_text.replace(letter, '*')
      return str(new_text)
      
    name = remove_unicode(guild_obj.name)

    if name == "" or name == None:
      name = "*only unicode symbols*"
    data[name] = [guild.member_count, remove_unicode(str(guild.owner.name))]
  
  with open('servers.json', 'w') as f:
    json.dump(data, f, indent=2)
    
  os.system("clear")
  print(colored("Welcome to the GoBot Startup Menu", attrs=["bold"]))
  print("Loading bot...")
  time.sleep(0.3)
  print("")
  print(f"Discord.py version: {discord.__version__}")
  time.sleep(0.3)
  print("")
  print("Fetching guilds...")
  print("")
  for guild in client.guilds:
    print(colored(guild.name, attrs=["bold"]), "-", guild.member_count, "members")
    time.sleep(0.1)
  time.sleep(1)
  print("")
  print("Ready to start...")
  time.sleep(3)
  os.system('clear')

  client.add_cog(Init(client))
  client.add_cog(Info(client))
  client.add_cog(Moderation(client))
  client.add_cog(Errors(client))
  #client.add_cog(Buttons(client))
  client.add_cog(Fun(client))
  client.add_cog(Math(client))
  client.add_cog(Bomb(client))
  client.add_cog(Giveaways(client))
  client.add_cog(Polls(client))
  client.add_cog(Leveling(client))
  client.add_cog(LocalLeveling(client))
  client.add_cog(Leaderboard(client))
  client.add_cog(LLeaderboard(client))
  client.add_cog(VoteTracker(client))
  client.add_cog(Reactions(client))
  client.add_cog(Embeds(client))
  #client.add_cog(Blackjack(client))
  client.add_cog(AFK(client))
  client.add_cog(Welcome(client))
  client.add_cog(Leaver(client))
  client.add_cog(Tic(client))
  client.add_cog(Util(client))
  client.add_cog(Counting(client))

  time.sleep(3)
  os.system("clear")
  start_time = datetime.utcnow()

  def thread_function():
    start_time = datetime.utcnow()
    import asyncio
    import os
    import time
    while True:
      print(colored("Status:", attrs=["bold"]), colored("online", "green"))
      print(colored("Online since:", attrs = ['bold']), colored(datetime.utcnow(), attrs=["dark"]))
      print(colored("Time online:", attrs = ['bold']), colored(datetime.utcnow()-start_time, attrs=["dark"]))
      
      time.sleep(1)
      os.system("clear")

  x = threading.Thread(target=thread_function, args=())
  x.start()

      
  

#[----------COMMANDS----------]
@client.command()
@commands.has_permissions(administrator=True) 
async def stop(ctx):
  await ctx.send("`Stopping system...`")
  os.system("kill 1")

@client.event
async def on_guild_join(guild):
    if len(guild.members) < 501:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
            prefixes[str(guild.id)] = '?'
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        await guild.text_channels[0].send(
            ">>> **\ Hello! I am GoBot, your server's new guardian.** Run `?help` to get started."
        )  # good
    else:
        await guild.text_channels[0].send(
            ">>> ❌ **It seems like your server has more than 500 members.** GoBot's free version does not support servers with over 500 members. Premium will be available soon!"
        )


@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        prefixes.pop(str(guild.id))
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.command(aliases=["sp", "setprefix", "prefix"])  # command 1
@commands.has_permissions(administrator=True)
async def set_prefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        await ctx.send(f"> ✅ **Prefix has been updated to `{prefix}`.**")
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.command()
async def test(ctx):
    await ctx.send("> ✅ **Bot is operational, running all cogs.**"
                   )  # command 2

@client.command()
async def ping(ctx):
    message = await ctx.send(
        f">>> ⌛ Bot's current latency is **{round(client.latency * 1000, 2)}** ms."
    )  # command 3

      

    


#[--------COGS-------]
# removed for now
  
#[----------LOGGING IN----------]
keep_alive()
tokenvar = os.environ['token']
client.run(tokenvar)
#total in Main.py: 1 + 1
