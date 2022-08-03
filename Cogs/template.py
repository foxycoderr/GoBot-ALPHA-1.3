import discord
from discord.ext import commands

class Name(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Name Cog loaded!")

  #@commands.command()
  #async def command(self, ctx):
    #None