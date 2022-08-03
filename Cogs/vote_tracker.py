import discord
from discord.ext import commands
import requests
import os
import time

class VoteTracker(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("📡 Vote Tracker loaded!")
    topgg_token = os.environ["topgg_token"]
    while True:
      data = requests.get(url="https://top.gg/api/bots/963457369310916678/votes", headers={"Authorization":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijk2MzQ1NzM2OTMxMDkxNjY3OCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjU4NTU5MzQ2fQ.vYowXBFpRZ28cgppzbF1PkYstQHJz_Z7LJ8fKy3yyio"})
      time.sleep(1)
      data2 = requests.get(url="https://top.gg/api/bots/963457369310916678/votes", headers= {"Authorization":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijk2MzQ1NzM2OTMxMDkxNjY3OCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjU4NTU5MzQ2fQ.vYowXBFpRZ28cgppzbF1PkYstQHJz_Z7LJ8fKy3yyio"})
      print(data) 
      if data != data2:
        voter = data2[-1]
        voter_id = voter["id"]
        for guild in self.client.guilds:
          for member in guild.members:
            if member.id == voter_id:
              voter_obj = await guild.fetch_member(member.id)
              
        await voter_obj.send("😊 **Thank you for voting!** If you like our bot, you will like our bot's server! We constantly post development updates and sneak peeks to new features.")
        guild = 963460256627851294
        channel = await guild.fetch_channel(1000089804064706561)
        await channel.send(f"🔺 **{voter['username']}** just upvoted the bot on https://top.gg!")
        await channel.send
