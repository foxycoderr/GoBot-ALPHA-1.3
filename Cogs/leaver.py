import discord
from discord.ext import commands
import json

class Leaver(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Leave Cog loaded!")
  @commands.has_permissions(manage_channels=True)
  @commands.command()
  async def leave(self, ctx, toggler = "Toggle", channel : discord.TextChannel = None):
    with open('leave.json', 'r') as f:
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
          await ctx.send("Leaver has been turned `on`.",delete_after=10)
        else:
          servers[str(ctx.message.guild.id)]["status"] = "off"
          await ctx.send("Leaver has been turned `off`.",delete_after=10)
      else:
        if final == True:
          servers[str(ctx.message.guild.id)] = {}
          servers[str(ctx.message.guild.id)]["status"] = "on"
          servers[str(ctx.message.guild.id)]["channel"] = str(channel.id)
          await ctx.send("Leaver has been turned `on`.",delete_after=10)
        else:
          await ctx.send("Leaver is already `off`.",delete_after=10)

      
    with open('leave.json', 'w') as f:
      json.dump(servers, f)
        
 
  @commands.Cog.listener()
  async def on_member_remove(self, member):
    with open('leave.json', 'r') as f:
      servers = json.load(f)
      
    if str(member.guild.id) in servers:
      if servers[str(member.guild.id)]["status"] == "on":
        channel = await self.client.fetch_channel(servers[str(member.guild.id)]["channel"])
        await channel.send(f"**☹ {str(member)} has left the server!**")

  #total: 1