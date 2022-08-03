#Loading Cog....

import discord
from discord.ext import commands
import json

class Reactions(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Reactions Cog loaded!")

  @commands.command(aliases=["rr", "reaction", "role"])
  @commands.has_permissions(manage_roles=True)
  async def reactionrole(self, ctx, channel : discord.TextChannel, emoji, role : discord.Role, *, message : str):
    file = "reaction_roles"
    

    with open(f'{file}.json', 'r') as f:
      values = json.load(f) 

    mess = await channel.send(message)
    
    values[str(mess.id)] = {}
    values[str(mess.id)]["1"] = {}
    values[str(mess.id)]["1"]['emoji'] = emoji
    values[str(mess.id)]["1"]['role'] = str(role)
    values[str(mess.id)]["1"]['guild'] = str(ctx.message.guild)
    
    with open("reaction_roles.json","w") as f:
      json.dump(values,f)
    
    
    await mess.add_reaction(emoji)
    await ctx.send(f">>> ✅ **Created reaction role with ID {mess.id} for {role.mention} with the emoji {emoji} in {channel}.**", delete_after=10)
    await ctx.message.delete(delay=10)

  #-------------Reaction added------------
  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    file = "reaction_roles"
    

    with open(f'{file}.json', 'r') as f:
      values = json.load(f)

    # if payload.message_id != self.target_message_id:
    #    return

    guild = self.client.get_guild(payload.guild_id)
    
    if not payload.member.bot:
      if str(payload.message_id) in values:
        for i in range (len(values[str(payload.message_id)])+1):
          if i != 0:
            if str(payload.emoji) == values[str(payload.message_id)][str(i)]['emoji']:
              guild = self.client.get_guild(payload.guild_id)
              role = discord.utils.get(guild.roles, name=values[str(payload.message_id)][str(i)]['role'])
              await payload.member.add_roles(role)
              await payload.member.send(f">>> :information_source: You were given the **{str(role)}** in **{str(guild)}**.")

  #--------Reaction removed--------
  @commands.Cog.listener()
  async def on_raw_reaction_remove(self, payload):
    file = "reaction_roles"
    

    with open(f'{file}.json', 'r') as f:
      values = json.load(f)

    # if payload.message_id != self.target_message_id:
    #    return

    guild = self.client.get_guild(payload.guild_id)
    
    
    if str(payload.message_id) in values:
      for i in range (len(values[str(payload.message_id)])+1):
        if i != 0:
          if str(payload.emoji) == values[str(payload.message_id)][str(i)]['emoji']:
            guild = self.client.get_guild(payload.guild_id)
            role = discord.utils.get(guild.roles, name=values[str(payload.message_id)][str(i)]['role']) # role = guild.get_role(role_id)
            member = await guild.fetch_member(str(payload.user_id))
            await member.remove_roles(role)
            await member.send(f">>> :information_source: You were removed from the **{str(role)}** in **{str(guild)}**.")



  @commands.command(aliases=["rradd", "addreaction", "addrole"]) 
  @commands.has_permissions(manage_roles=True)
  async def addrr(self, ctx, id, emoji, channel : discord.TextChannel, role : discord.Role): 
    file = "reaction_roles"
    

    with open(f'{file}.json', 'r') as f:
      values = json.load(f)
    already_exists = False
    if id in values:
      already_exists = True
    if already_exists == False:
      mess = id
      values[str(mess)] = {}
      values[str(mess)]["1"] = {}
      values[str(mess)]["1"]['emoji'] = emoji
      values[str(mess)]["1"]['role'] = str(role)
      values[str(mess)]["1"]['guild'] = str(ctx.message.guild)
    else:
      mess = id
      values[str(mess)][len(values[str(mess)])+1] = {}
      values[str(mess)][len(values[str(mess)])]['emoji'] = emoji
      values[str(mess)][len(values[str(mess)])]['role'] = str(role)
      values[str(mess)][len(values[str(mess)])]['guild'] = str(ctx.message.guild)
    
    with open("reaction_roles.json","w") as f:
      json.dump(values,f)
    
    mess1 = await channel.fetch_message(id)
    await mess1.add_reaction(emoji)
    await ctx.send(f">>> <:yes:984360144047571014> **Created reaction role with ID {mess} for {role.mention} with the emoji {emoji} in {channel}.**", delete_after=10)
    await ctx.message.delete(delay=10)
















  
#total in reactions.py: 2