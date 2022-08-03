import discord
from discord.ext import commands
import json
import random

class Welcome(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Welcome Cog loaded!")
  @commands.has_permissions(manage_channels=True)
  @commands.command()
  async def welcome(self, ctx, toggler = "Toggle", channel : discord.TextChannel = None):
    with open('welcomes.json', 'r') as f:
      servers = json.load(f)

    final = True

    # start of all checks
    newServer = False
    if str(ctx.message.guild.id) in servers:
      if toggler == "Toggle": 
        if servers[str(ctx.message.guild.id)]["status"] == "on":
          final = False
        else:
          final = True
          
      elif toggler == "on":
        final = True
      elif toggler == "off":
        final = False
      else:
        toggler = True
    else:
      newServer = True

      if toggler == "Toggle": 
        if servers[str(ctx.message.guild.id)]["status"] == "on":
          final = False
        else:
          final = True
          
      elif toggler == "on":
        final = True
      elif toggler == "off":
        final = False
      else:
        toggler = True
    # end of all checks

    if (final == True and channel == None) or (final == False and not channel == None):
      await ctx.send("Wrong arguments passed!",delete_after=10)
    else:
      if not newServer:
        if final == True:
          servers[str(ctx.message.guild.id)]["status"] = "on"
          servers[str(ctx.message.guild.id)]["channel"] = str(channel.id)
          await ctx.send(f"Welcomer has been turned `on` in `{channel}`.",delete_after=10)
        else:
          servers[str(ctx.message.guild.id)]["status"] = "off"
          await ctx.send("Welcomer has been turned `off`.",delete_after=10)
      else:
        if final == True:
          servers[str(ctx.message.guild.id)] = {}
          servers[str(ctx.message.guild.id)]["status"] = "on"
          servers[str(ctx.message.guild.id)]["channel"] = str(channel.id)
          await ctx.send(f"Welcomer has been turned `on` in `{channel}`.",delete_after=10)
        else:
          await ctx.send("Welcomer is already `off`.",delete_after=10)

      
    with open('welcomes.json', 'w') as f:
      json.dump(servers, f)
        
  
  @commands.Cog.listener()
  async def on_member_join(self, member):
    with open('welcomes.json', 'r') as f:
      servers = json.load(f)
      
    if str(member.guild.id) in servers:
      if servers[str(member.guild.id)]["status"] == "on":
        channel = await self.client.fetch_channel(servers[str(member.guild.id)]["channel"])
        await channel.send(random.choice(f"**👋🏻 {member.mention} has joined the server!**", f"**👋🏻 {member.mention} has just hopped in!**", f"**👋🏻 {member.mention}, welcome to the party.**"))


"""
By Vitness:
it's how i see we can make these functions better, use it if it's ok (didn't test it). It is almost same i guess


@commands.command()
async def welcome(self, ctx, toggler="Toggle", channel: discord.TextChannel = None):
    if toggler not in {"Toggle", "on", "off"}:
        raise commands.BadArgument

    with open('welcomes.json', 'r') as file:
        servers = json.load(file)

    id = ctx.guild.id
    if id in servers:
        if toggler == "on":
            servers[id]["status"] = "on"
        elif toggler == "off":
            servers[id]["status"] = "off"
        elif toggler == "Toggle":
            servers[id]["status"] = not servers[id]["status"]
    else:
        if channel is None:
            channel = ctx.guild.system_channel
        if toggler == "Toggle":
            toggler = "on"
        servers[id] = {"status": toggler, "channel": channel.id}
    await ctx.send(f"Welcomer is `{servers[id]['status']}` now in `{channel.name}`.")

    with open('welcomes.json', 'w') as f:
        json.dump(servers, f)


@commands.Cog.listener()
async def on_member_join(self, member):
    with open('welcomes.json', 'r') as file:
        servers = json.load(file)
        
    if member.guild.id in servers:
        if servers[member.guild.id]["status"] == "on":
            channel = await self.client.fetch_channel(servers[member.guild.id]["channel"])
            await channel.send(f"**👋🏻 {member.mention} has joined the server!**")
"""
#total: 1