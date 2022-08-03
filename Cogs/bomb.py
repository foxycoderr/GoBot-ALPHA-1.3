import discord
from discord.ext import commands
import random
import os
from requests import get
import json
import asyncio

class Bomb(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Bomb Cog loaded!")

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def bomb(self, ctx):
    for i in range (300):
      await ctx.send("https://media1.tenor.com/images/85e85abb417f11f83a093733a679fbc5/tenor.gif")
      await asyncio.sleep(0.3)

    #total in bomb.py: 1