import discord
from discord.ext import commands
import asyncio
import json

class AFK(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ AFK Cog loaded!")

    #shut
  #[MESSAGE HANDLER] (not command)
  @commands.Cog.listener()
  async def on_message(self, message):         
    with open("afk.json", "r") as f: 
      data = json.loads(f.read())
    user = str(message.author.id)
    if (message.mentions and not message.author.bot):
      for mention in message.mentions:
        if str(mention.id) in data:
          if data[str(mention.id)]['status'] == 'True':
            await message.channel.send(f">>> **{mention} is now AFK.**")
    if (user in data):
      if (data[user]['status'] == 'True' and not "afk" in message.content.lower()):
        data[user]['status'] = 'False'
        with open("afk.json", "w") as f:
          json.dump(data,f)
        await message.channel.send(">>> <:yes:984360144047571014> **You are no longer AFK.**", delete_after=10)
  @commands.command()
  async def afk(self, ctx, setting="toggle"): 
    with open("afk.json", "r") as f: 
      data = json.loads(f.read())
    wrong = False
    user = str(ctx.author.id) 
    if (user not in data):
      data[user] = {}
      data[user]['status'] = "False"
      if (setting == "toggle"):
        if (data[user]['status'] == "True"):
          data[user]['status'] = "False" 
        else:
          data[user]['status'] = "True"
          
      elif (setting == 'on'):
        data[user]['status'] = "True"
      elif (setting == 'off'):
        data[user]['status'] = "False" 
      else:
        wrong = True
      
    else: 
      if (setting == "toggle"):
        if (data[user]['status'] == "True"):
          data[user]['status'] = "False"
        else:
          data[user]['status'] = "True"
      elif (setting == 'on'):
        data[user]['status'] = "True"
      elif (setting == 'off'):
        data[user]['status'] = "False"
      else:
        wrong = True
    
    with open("afk.json", "w") as f:
      json.dump(data,f)
      
    if (wrong == False):
      await ctx.send(f">>> <:yes:984360144047571014> **Set your AFK status to `{data[user]['status']}`.**",delete_after=10)
    elif (wrong == True):
      await ctx.send( "**<:no:984361059420880896> Wrong argument passed.** This only works with **on, off, or no argument**, which toggles the statement.",delete_after=30)
  
      #total in afk.py: 1