import discord
import json
from discord.ext import commands

class Counting(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Counting Cog loaded!")
  @commands.has_permissions(manage_channels=True)
  @commands.command()
  async def counting(self, ctx, setting, channel:discord.TextChannel=None):
    with open ('counting.json', 'r') as f:
      data = json.load(f)
    
    if setting == "setup":
      try:
        if not ctx.message.guild.id in data:
          data[ctx.message.guild.id] = {}
          data[ctx.message.guild.id]["channel_id"] = channel.id
          data[ctx.message.guild.id]["last_number"] = 0
          data[ctx.message.guild.id]["last_counter_id"] = 0
          await ctx.send(f"✅ **Successfully set up counting in {channel.mention}!**")
        else:
          await ctx.send("❌ **Counting is already set up in this server!** Use `?counting channel #channel` to change the counting channel.")
      except:
        await ctx.send("❌ **It seems like you didn't give a valid channel.** If this error continues, run `?counting shutdown`.")
        
    elif setting == "channel":
      try:
        with open ('counting.json', 'r') as f:
          data = json.load(f)
        if str(ctx.message.guild.id) in data:
          data[str(ctx.message.guild.id)]["channel_id"] = channel.id
          await ctx.send(f"✅ **Sucessfully changed counting channel to {channel.mention}!**")
        else:
          await ctx.send("❌ **Counting is not set up yet!** Run `?counting setup #channel` first.")
      except:
        await ctx.send("❌ **It seems like you didn't give a valid channel.** If this error continues, run `?counting shutdown`.")
        
    elif setting == "shutdown":
      try:
        # index = data.index(str(ctx.message.guild.id))
        data.pop(str(ctx.message.guild.id))
        await ctx.send("✅ **Successfully deleted counting in this server.** Run `?counting setup` to set it up again.")
      except:
        await ctx.send("❌ **It seems like your server does not have counting!**")
        
    else:
      await ctx.send("❌ **Invalid setting!** You can run `?counting` with settings `setup #channel` (to set up counting), `channel #channel` (to change the counting channel), and `shutdown` (to turn counting off).")
      
    with open ('counting.json', 'w') as f:
      json.dump(data, f)

# fully running & tested code until here

  @commands.Cog.listener()
  async def on_message(self, message):
    # open file
    # check if the guild is in counting
    # check if the channel is counting
    # check if the message is an integer
    # check if author is not the last_counter
    # check if the number is the next one after the last_number
    # update last_counter and last_number
    # send aknowldgement
    # write all new data

    with open ('counting.json', 'r') as f:
      data = json.load(f)
      
    if message.content.isnumeric():
      if str(message.guild.id) in data:
        if message.channel.id == data[str(message.guild.id)]["channel_id"]:
          if message.author.id != data[str(message.guild.id)]["last_counter_id"]:
            if int(message.content) == data[str(message.guild.id)]["last_number"] + 1:
              await message.add_reaction("✅")
              data[str(message.guild.id)]["last_counter_id"] = message.author.id
              data[str(message.guild.id)]["last_number"] = int(message.content)
            else:
              await message.channel.send("❌ **Wrong number!**")
              await message.add_reaction("❌")
              data[str(message.guild.id)]["last_counter_id"] = 0
              data[str(message.guild.id)]["last_number"] = 0
          else:
            await message.channel.send("❌ **You can't count twice!**")
            await message.add_reaction("❌")
            data[str(message.guild.id)]["last_counter_id"] = 0
            data[str(message.guild.id)]["last_number"] = 0
            
    with open ('counting.json', 'w') as f:
      json.dump(data, f)

#total in counting.py: 1