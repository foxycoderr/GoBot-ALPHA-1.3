import discord
from discord.ext import commands

class Embeds(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Embeds Cog loaded!")

  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def embed(self, ctx, title, image_url, timestamp : bool, color, channel : discord.TextChannel, *, description):
    if timestamp==True:
      embed = discord.Embed(title=title, description=description, color = 0x00d1c6, timestamp=ctx.message.created_at)
    else:
      embed = discord.Embed(title=title, description=description)
    if image_url != "None":
      embed.set_image(url=image_url)
    await channel.send(embed=embed)
    #total in embeds.py: 1 