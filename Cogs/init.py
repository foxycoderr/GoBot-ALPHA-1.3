import discord
from discord.ext import commands
import asyncio
from datetime import datetime
import json

class Init(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_message(self, message):
    client = self.client
    i = 0
    def get_value(file:str, value:str):
      with open(f'{file}.json', 'r') as f:
          values = json.load(f)
      return values[str(f"{value}")]


    file = "commands"
    value1 = "commands"
    value2 = "users"

    users = 975682231098032188
    servers = 975682756220698624
    commands = 975689021038678056
    while True:
      usersch = await self.client.fetch_channel(users)
      serversch = await self.client.fetch_channel(servers)
      commandsch = await self.client.fetch_channel(commands)
      usersdata = get_value(file, value2)
      commandsdata = get_value(file, value1)

      await self.client.change_presence(activity=discord.Game(name="?help"))
      await asyncio.sleep(5)
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f" {str(len(client.guilds))} servers | {sum([guild.member_count for guild in client.guilds])//1000}k users")) 
      await asyncio.sleep(5)
      i = i + 1
      if i == 90:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        channel = await self.client.fetch_channel(974573495667273748)
        await channel.send(f"**BETA UP** at {current_time}")
        i = 0
      
      #total in init.py: 0