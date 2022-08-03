import discord
from discord.ext import commands
import datetime
import asyncio
import random

class Giveaways(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Giveaway Cog loaded!")
    
  @commands.command(aliases=["giveaway"])
  @commands.has_permissions(manage_roles=True)
  async def gstart(self, ctx, channel : discord.TextChannel, winners : int, days=0, hours=0, minutes=0, sec=0, *, prize : str):
    days = int(days)
    hours = int(hours)
    minutes = int(minutes)
    sec = int(sec)
    embed = discord.Embed(title=":tada: **GIVEAWAY!** :tada:", description = f"**{prize}**", color=0x00d1c6, timestamp = ctx.message.created_at)
  
    end = datetime.datetime.now() + datetime.timedelta(seconds = sec + minutes*60 + hours *3600 + days*86400)
  
    embed.add_field(name = "Ends At:", value = f"{end} UTC", inline=False)
    embed.add_field(name = "Hosted by:", value = f"{ctx.message.author}", inline=False)
    embed.add_field(name = "Time period:", value = f"{days}d, {hours}h, {minutes}m, {sec}s", inline=False)
  
    my_msg = await channel.send(embed = embed)
  
    await my_msg.add_reaction("🎉")
  
    await asyncio.sleep(sec + minutes*60 + hours*3600 + days*86400)
  
    new_msg = await channel.fetch_message(my_msg.id)
  
    users = await new_msg.reactions[0].users().flatten()
    client = self.client
    users.pop(users.index(client.user))
    if ctx.message.author in users:
      print("bobbbthebuilder")
      users.pop(users.index(ctx.message.author))
    print(len(users))
  
    
    if len(users) != 0:
      winner = random.choice(users)
      embe = discord.Embed(title=":tada: **GIVEAWAY ENDED!** :tada:", description = f"The giveaway for **{prize}** hosted by **{ctx.message.author}** was won by** {winner.mention}**!", color=0x00d1c6, timestamp = ctx.message.created_at) # I have an idea
      embe.set_footer(text=f"{len(users)} users participated") 
      await ctx.send(embed=embe, content=ctx.author.mention+" "+winner.mention)
    else: 
      embe = discord.Embed(title=":x: **GIVEAWAY ERROR!** :x:", description = f"The giveaway for **{prize}** hosted by **{ctx.message.author}** was not won by **anyone** since nobody participated in the giveaway.", color=0x00d1c6, timestamp = ctx.message.created_at)
      embe.set_footer(text=f"{len(users)} users participated")
      await ctx.send(embed=embe)
    #total in giveaways.py: 1 