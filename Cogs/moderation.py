import discord
from discord.ext import commands
import asyncio
import json
import emoji
import re
class Moderation(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Moderation Cog loaded!")

    
  #[KICK]
  @commands.command(aliases=["kc","kik","kic"])
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, member: discord.Member, *, reason="no reason"):
    await member.kick(reason=reason)
    await ctx.send(f"> <:yes:984360144047571014> **{member}** has been kicked for {reason}.", delete_after=10)
    await ctx.message.delete(delay=10)

  #[BAN]
  @commands.command(aliases=["b","ba","bn"])
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx, member: discord.Member, *, reason="no reason"):
    await member.ban(reason=reason)
    await ctx.send(f"> <:yes:984360144047571014> **{member}** has been banned for {reason}.", delete_after=10)
    await ctx.message.delete(delay=10)
    
  #[UNBAN]
  @commands.command(aliases=["unb","unba","unbn","nban"])
  @commands.has_permissions(ban_members=True)
  async def unban(self, ctx, *, member: str):
    BanList = await ctx.guild.bans()
    MemberName, MemberDiscrim = member.split('#')
    for BanEntry in BanList:
      user = BanEntry.user
      if (MemberName,MemberDiscrim) == (user.name,user.discriminator): 
        await ctx.guild.unban(user)
        await ctx.send(f"> <:yes:984360144047571014> **{user.mention}** has been unbanned.", delete_after=10)
        await ctx.message.delete(delay=10)
        return
        
  #[CLEAR]
  @commands.command(aliases=["purge","pr","cl","pg","purg"])
  @commands.has_permissions(manage_messages=True)
  async def clear(self, ctx, number: int=2):
    await ctx.channel.purge(limit = number)
    channel = ctx.channel
    if number == 1: 
      await ctx.send(f"> <:yes:984360144047571014> **{number}** message have been cleared in **{channel.mention}**.", delete_after=10)
      await ctx.message.delete(delay=10)
    else: 
      await ctx.send(f"> <:yes:984360144047571014> **{number}** messages have been cleared in **{channel.mention}**.", delete_after=10)
      await ctx.message.delete(delay=10)

  #[TEMPBAN]
  # removed for now, check code.txt in "other" folder


#[LOCK & UNLOCK]
  @commands.command(aliases=["lck", "lk"])
  @commands.has_permissions(manage_channels=True)
  async def lock(self, ctx, channel : discord.TextChannel=None):
      channel = channel or ctx.channel
      overwrite = channel.overwrites_for(ctx.guild.default_role)
      overwrite.send_messages = False
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
      await ctx.send(f">>> 🔒 Channel **{channel}** is locked for `{ctx.guild.default_role}`.",delete_after=10)

  
  @commands.command(aliases=["unlck", "ulk"])
  @commands.has_permissions(manage_channels=True)
  async def unlock(self, ctx, channel : discord.TextChannel=None):
      channel = channel or ctx.channel
      overwrite = channel.overwrites_for(ctx.guild.default_role)
      overwrite.send_messages = True
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
      await ctx.send(f">>> 🔓 Channel **{channel}** is unlocked.",delete_after=10)


# [MUTE & UNMUTE]
  @commands.has_permissions(manage_roles = True)
  @commands.command(aliases = ["mt"])
  async def mute(self, ctx, member: discord.Member, *, reason=None):
      file = "mutes"
      with open(f'{file}.json', 'r+') as f:
        mutes = json.load(f)
      guild = ctx.guild
      yesorno = 0
      for role in guild.roles:
          if role.name == "Muted":
              yesorno = 1
              await member.add_roles(role)
             # mutes[str(ctx.message.guild)] = {}
             # mutes[str(ctx.message.guild)]["1"] = {}
             # mutes[str(ctx.message.guild)]["1"]['member'] = str(member.id)
             # mutes[str(ctx.message.guild)]["1"]['time'] = "indefinitely"
              await ctx.send(f">>> 🔇 **{member}** was muted indefinitely.",delete_after=10)
    
              return
      if yesorno == 0:
          guild = ctx.guild
          perms = discord.Permissions(send_messages = False, view_channel = True)
          await guild.create_role(name="Muted", permissions = perms)
          await member.add_roles("Muted")
         # mutes[str(ctx.message.guild)] = {}
         # mutes[str(ctx.message.guild)]["1"] = {}
         # mutes[str(ctx.message.guild)]["1"]['member'] = str(member.id)
         # mutes[str(ctx.message.guild)]["1"]['time'] = "indefinitely"
          await ctx.send(f">>> 🔇 **{member}** was muted indefinitely, reason: `{reason}`. *Muted* role created because no muted role was found in the server*.",delete_after=10)

  @commands.has_permissions(manage_roles = True)
  @commands.command(aliases = ["umt"])
  async def unmute(self, ctx, member: discord.Member):
    with open("mutes.json", 'r+') as f:
      mutes = json.load(f)
    guild = ctx.guild
    for role in guild.roles:
      if role.name == "Muted":
        await member.remove_roles(role)
       # mutes[str(ctx.message.guild)] = {}
       # mutes[str(ctx.message.guild)]["1"] = {}
       # mutes[str(ctx.message.guild)]["1"]['member'] = str(member.id)
       # mutes[str(ctx.message.guild)]["1"]['time'] = "indefinitely"
        await ctx.send(f">>> 🔊 **{member}** was unmuted.",delete_after=10)

#[TEMPMUTE]

  @commands.has_permissions(manage_roles = True)
  @commands.command(aliases = ["tmute", "tmt", "tempm", "tm"])
  async def tempmute(self, ctx, member : discord.Member, time : float, *, reason="None"):
    
    guild = ctx.guild
    yn = 0 # yes or no
    for role in guild.roles:
      if role.name == "Muted":
        yn = 1
        await member.add_roles(role)
        #mutes[str(ctx.message.guild)] = {}
        #mutes[str(ctx.message.guild)]["1"] = {}
        #mutes[str(ctx.message.guild)]["1"]['member'] = str(member.id)
        #mutes[str(ctx.message.guild)]["1"]['time'] = f"{str(time)} minutes"
        await ctx.send(f">>> 🔇 **{member}** was muted for {time} minutes. Reason: `{reason}`.",delete_after=10)
    if yn == 0:
      guild = ctx.guild
      perms = discord.Permissions(send_messages = False, view_channel = True)
      await guild.create_role(name="Muted", permissions = perms)
      await member.add_roles("Muted")
    

     # mutes[str(ctx.message.guild)] = {}
    #  mutes[str(ctx.message.guild)]["1"] = {}
     # mutes[str(ctx.message.guild)]["1"]['member'] = str(member.id)
      #mutes[str(ctx.message.guild)]["1"]['time'] = str(time)
      await ctx.send(f">>> 🔇 {member.mention} was muted for `{time}` minutes. Reason: `{reason}`. *Muted* role created because no muted role was found in the server*.",delete_after=10)
    tempmute=time*60
    
    await asyncio.sleep(tempmute)
    guild = ctx.guild
    for role1 in guild.roles:
      if role1.name == "Muted":
        await member.remove_roles(role1)
    #mutes[str(ctx.message.guild)] = {}
   # mutes[str(ctx.message.guild)]["1"] = {}
  #  mutes[str(ctx.message.guild)]["1"]['member'] = str(member.id)
  #  mutes[str(ctx.message.guild)]["1"]['time'] = str("Unmuted")
    await ctx.send(f">>> 🔊 {member.mention} was unmuted after {time} minutes!",delete_after=10) # Let's try this
    
# [MUTES]
  @commands.command(aliases = ["mts"])
  async def mutes(self, ctx):
    mutes = discord.Embed(title="🔇 Muted members", color = 0x00d1c6)
    guild = ctx.guild
    yes = False
    for role1 in guild.roles:
      if role1.name == "Muted":
        role = role1
    for member in guild.members:
      if (role in member.roles):
        mutes.add_field(name=f"{member}", value="Muted")
        yes = True
    if (yes == False):
      mutes.add_field(name="There's no", value="**muted members!**")
    await ctx.send(embed = mutes,delete_after=60)
  
# [SLOWMODE]
  @commands.command(aliases = ["sm"])
  @commands.has_permissions(manage_channels = True)
  async def slowmode(self, ctx, time: str="0s"):
    seconds = 0 
    type = "s"
    if(time.isnumeric()):
      seconds = int(time)
    elif(time[:-1].isnumeric()):
      if(time[-1] == "s"):
        seconds = int(time[:-1])
      elif(time[-1] == "m"):
        seconds = int(time[:-1])*60
        type = "m"
      elif(time[-1] == "h"):
        seconds = int(time[:-1])*60*60
        type = "h"
    if(seconds < 0):
      seconds *= -1
    if(seconds > 21600):
      await ctx.send(f":x: **Slowmode delay should be less than `6 hours`.**", delete_after = 10)
    elif(seconds == 0):
      await ctx.channel.edit(slowmode_delay = seconds)
      await ctx.send(f"<:yes:984360144047571014> Slowmode was deactivated.", delete_after = 10)
    else:
      await ctx.channel.edit(slowmode_delay = seconds)
      if type == "s":
        await ctx.send(f"<:yes:984360144047571014> Slowmode was set to `{seconds}` seconds.", delete_after = 10)
      elif type == "m":
        await ctx.send(f"<:yes:984360144047571014> Slowmode was set to `{int(seconds/60)}` minutes.", delete_after = 10)
      else:
        await ctx.send(f"<:yes:984360144047571014> Slowmode was set to `{int(seconds/3600)}` hours.", delete_after = 10)
           

# [AUTOMOD]
  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    with open('automod.json', 'r') as f:
      prefixes = json.load(f)
      prefixes[str(guild.id)] = 'off'
    with open('automod.json', 'w') as f:
      json.dump(prefixes, f, indent=4)

  @commands.Cog.listener()
  async def on_guild_remove(self, guild): 
      with open('automod.json', 'r') as f:
        prefixes = json.load(f)
        prefixes.pop(str(guild.id))
      with open('automod.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
  

      
  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def automod(self, ctx, msg = None, param = None):
    with open('automod.json', 'r') as f:
      prefixes = json.load(f)
      if str(ctx.guild.id) not in prefixes:
          prefixes[str(ctx.guild.id)] = ["off", "off", "off", -1, "off", -1, "off"]
      if msg == None:
        toggle = prefixes[str(ctx.guild.id)][0]
        if toggle == "on":
          await ctx.send(f"> <:yes:984360144047571014> **Automod has been turned `off`.**", delete_after = 10)
          prefixes[str(ctx.guild.id)][0] = "off"
        elif toggle == "off":
          await ctx.send(f"> <:yes:984360144047571014> **Automod has been turned `on`.**", delete_after = 10)
          prefixes[str(ctx.guild.id)][0] = "on"
      elif msg == "links":
        toggle = prefixes[str(ctx.guild.id)][1]
        if toggle == "on":
          await ctx.send(f"> <:yes:984360144047571014> **Link Killer has been turned `off`.**", delete_after = 10)
          prefixes[str(ctx.guild.id)][1] = "off"
        elif toggle == "off":
          await ctx.send(f"> <:yes:984360144047571014> **Link Killer has been turned `on`.**", delete_after = 10)
          prefixes[str(ctx.guild.id)][1] = "on"
      elif msg == "emojis":
        try:
          param = int(param)
        except TypeError:
          pass
        if param == None:
          num = prefixes[str(ctx.guild.id)][3]
          if num != -1:
            toggle = prefixes[str(ctx.guild.id)][2]
            if toggle == "on":
              await ctx.send(f"> <:yes:984360144047571014> **Emoji Slayer has been turned `off`.**", delete_after = 10)
              prefixes[str(ctx.guild.id)][2] = "off"
            elif toggle == "off":
              await ctx.send(f"> <:yes:984360144047571014> **Emoji Slayer has been turned `on`.**", delete_after = 10)
              prefixes[str(ctx.guild.id)][2] = "on"
          else:
            await ctx.send(">>> **<:no:984361059420880896> You need to specify maximum number of emojis in a message.**", delete_after = 10)
        elif type(param) != int:
          await ctx.send(">>> **<:no:984361059420880896> Invalid arguments were given.**", delete_after = 10)
        elif param < 0:
          await ctx.send(">>> **<:no:984361059420880896> Maximum emojis number can't be below 0.**", delete_after = 10)
        else:
          prefixes[str(ctx.guild.id)][3] = param
          await ctx.send(f"> <:yes:984360144047571014> **Maximum number of emojis in a message was set to {param}.**", delete_after = 10)
      elif msg == "mentions":
        try:
          param = int(param)
        except TypeError:
          pass
        if param == None:
          num = prefixes[str(ctx.guild.id)][5]
          if num != -1:
            toggle = prefixes[str(ctx.guild.id)][4]
            if toggle == "on":
              await ctx.send(f"> <:yes:984360144047571014> **Mention Destroyer has been turned `off`.**", delete_after = 10)
              prefixes[str(ctx.guild.id)][4] = "off"
            elif toggle == "off":
              await ctx.send(f"> <:yes:984360144047571014> **Mention Destroyer has been turned `on`.**", delete_after = 10)
              prefixes[str(ctx.guild.id)][4] = "on"
          else:
            await ctx.send(">>> **<:no:984361059420880896> You need to specify maximum number of mentions in a message.**", delete_after = 10)
        elif type(param) != int:
          await ctx.send(">>> **<:no:984361059420880896> Invalid arguments were given.**", delete_after = 10)
        elif param < 0:
          await ctx.send(">>> **<:no:984361059420880896> Maximum mention number can't be below 0.**", delete_after = 10)
        else:
          prefixes[str(ctx.guild.id)][5] = param
          await ctx.send(f"> <:yes:984360144047571014> **Maximum number of mentions in a message was set to {param}.**", delete_after = 10)
      elif msg == "caps":
        toggle = prefixes[str(ctx.guild.id)][6]
        if toggle == "on":
          await ctx.send(f"> <:yes:984360144047571014> **CAPS Banisher has been turned `off`.**", delete_after = 10)
          prefixes[str(ctx.guild.id)][6] = "off"
        elif toggle == "off":
          await ctx.send(f"> <:yes:984360144047571014> **CAPS Banisher has been turned `on`.**", delete_after = 10)
          prefixes[str(ctx.guild.id)][6] = "on"
      else:
        await ctx.send(">>> **<:no:984361059420880896> Invalid arguments were given.**", delete_after = 10)
    with open('automod.json', 'w') as f:
      json.dump(prefixes, f)

      
  #[AUTOMOD_ADD] 
  @commands.command(aliases=["addmd", "autoadd", "addauto"])
  @commands.has_permissions(administrator=True) 
  async def automod_add(self, ctx, message = None):
    if message != None:
      with open('automod_lists.json', 'r') as f:
        data = json.load(f)  
      if str(ctx.guild.id) not in data:
        data[str(ctx.guild.id)] = []
      for i in map(str,message.split(",")):
        data[str(ctx.guild.id)].append(i)
      await ctx.send(f"> <:yes:984360144047571014> **Added to auto moderation list.**", delete_after = 10)
      with open('automod_lists.json', 'w') as f:
        json.dump(data, f)
    else:
      await ctx.send(">>> **<:no:984361059420880896> No arguments were given.**", delete_after = 10)

      
  #[AUTOMOD_REMOVE]
  @commands.command(aliases=["rmmd", "autodel", "delauto"]) 
  @commands.has_permissions(administrator=True) 
  async def automod_rm(self, ctx, message = None):
    if message != None:
      with open('automod_lists.json', 'r') as f:
        data = json.load(f)
      if str(ctx.guild.id) not in data:
        data[str(ctx.guild.id)] = []
      text = ''
      for i in map(str,message.split(",")):
        if i in data[str(ctx.guild.id)]:
          data[str(ctx.guild.id)].remove(i)
          text += i + ", "
      if text != '':
        text = text[:-2]
        text = f"> <:yes:984360144047571014> **Removed `{text}` from auto moderation list: **"
        await ctx.send(text, delete_after = 10)
      else:
        await ctx.send(">>> **<:no:984361059420880896> None of the arguments were removed from auto moderation list.**", delete_after = 10)
      with open('automod_lists.json', 'w') as f:
        json.dump(data, f)
    else:
      await ctx.send(">>> **<:no:984361059420880896> No arguments were given.**", delete_after = 10)

      
  #[AUTOMOD_LIST]
  @commands.command(aliases=["lsmd", "autols", "lsauto"]) 
  async def automod_list(self, ctx, param = None):
    if param == None:
      with open('automod_lists.json', 'r') as f:
        data = json.load(f) 
      if str(ctx.guild.id) not in data:
        data[str(ctx.guild.id)] = []
      text = data[str(ctx.guild.id)]
      await ctx.send("**⛔ List of banned words:** `" + '`, `'.join(text) + "`", delete_after = 55)
    elif param.startswith("s"):
      with open('automod.json', 'r') as f:
        data = json.load(f)
      embed = discord.Embed(title = "🛠️ Server automod settings", color=0x00d1c6, timestamp=ctx.message.created_at)

      if str(ctx.guild.id) in data:
        embed.add_field(name="Automod:", value=f"`{data[str(ctx.guild.id)][0]}`", inline = False)
        embed.add_field(name="Link Killer:", value=f"`{data[str(ctx.guild.id)][1]}`", inline = False)
        embed.add_field(name="Emoji Slayer:", value=f"`{data[str(ctx.guild.id)][2]}`", inline = False)
        embed.add_field(name="Mention Destroyer:", value=f"`{data[str(ctx.guild.id)][4]}`", inline = False)
        embed.add_field(name="CAPS Banisher:", value=f"`{data[str(ctx.guild.id)][6]}`", inline = False)
        embed.add_field(name="Emoji Cap:", value=f"`{data[str(ctx.guild.id)][3]}`", inline = False)
        embed.add_field(name="Mention Cap:", value=f"`{data[str(ctx.guild.id)][5]}`", inline = True)
      else:
        embed.add_field(name="Automod:", value=f"`off`", inline = True)
        embed.add_field(name="Link Killer:", value=f"`off`", inline = True)
        embed.add_field(name="Emoji Slayer:", value=f"`off`", inline = True)
        embed.add_field(name="Mention Destroyer:", value=f"`off`", inline = True)
        embed.add_field(name="CAPS Banisher:", value=f"`off`", inline = True)
        embed.add_field(name="Emoji Cap:", value=f"`None`", inline = True)
        embed.add_field(name="Mention Cap:", value=f"`None`", inline = True)

      
      """text = "> 🛠️ **Server automod settings:**\n\n"
      if str(ctx.guild.id) in data:
        text += "**Automod**: " + "`" + data[str(ctx.guild.id)][0] + "`" + "\n**Link destroyer**: " + "`" + data[str(ctx.guild.id)][1] + "`" + "\n**Emoji destroyer**: " + "`" + data[str(ctx.guild.id)][2] + "`" + "\n**Mention destroyer**: " + "`" + data[str(ctx.guild.id)][4] + "`"
        if data[str(ctx.guild.id)][3] != -1:
          text += "\n**Maximum emojis per message**: " + "`" + str(data[str(ctx.guild.id)][3]) + "`"
        else:
          text += "\n**Maximum emojis per message:** `unspecified`"
        if data[str(ctx.guild.id)][5] != -1:
          text += "\n**Maximum mentions per message:** " + "`" + str(data[str(ctx.guild.id)][5]) + "`"
        else:
          text += "\n**Maximum mentions per message: `unspecified`**"
      else:
        text += "**Automod:** `off`" + "\n**Link destroyer:** `off`" + "\n**Emoji destroyer:** `off`" + "\n**Mention destroyer:** `off`" """
      await ctx.send(embed=embed, delete_after=30)




      
    else:
      await ctx.send(">>> **<:no:984361059420880896> Invalid arguments were given.**", delete_after = 10) 

    
  #[MESSAGE HANDLER] (not command)
  @commands.Cog.listener()
  async def on_message(self, message):
    with open('automod.json', 'r') as f:
      prefixes = json.load(f)
    if str(message.guild.id) not in prefixes:
        prefixes[str(message.guild.id)] = ["off", "off", "off", -1, "off", -1, "off"]
    if prefixes[str(message.guild.id)][1] == "on" and not message.author.bot and ("https://" in message.content or "http://" in message.content):
      member = message.author
      await message.channel.send(f">>> ⛔ **No links, {member.mention}.**", delete_after = 10)
      await message.delete()
    elif prefixes[str(message.guild.id)][4] == "on" and not message.author.bot:
      if len(message.raw_mentions) > prefixes[str(message.guild.id)][5]:
        member = message.author
        await message.channel.send(f">>> ⛔ **Too many mentions, {member.mention}.**", delete_after = 10)
        await message.delete()
    elif prefixes[str(message.guild.id)][2] == "on" and not message.author.bot:
      emj_cnt = 0
      for i in emoji.demojize(message.content).split(":"):
        i = ":" + i + ":"
        if emoji.is_emoji(emoji.emojize(i)):
          emj_cnt += 1
        if emj_cnt > prefixes[str(message.guild.id)][3]:
          member = message.author
          await message.channel.send(f">>> ⛔ **Too many emojis, {member.mention}.**", delete_after = 10)
          await message.delete()
          break
    elif prefixes[str(message.guild.id)][6] == "on" and not message.author.bot:
      cps_cnt = 0
      for i in message.content:
        if i >= "A" and i <= "Z":
          cps_cnt += 1
      if cps_cnt / len(message.content) * 100.0 > 65 and len(message.content) > 5:
          member = message.author
          await message.channel.send(f">>> ⛔ **No CAPS, {member.mention}.**", delete_after = 10)
          await message.delete()
    elif prefixes[str(message.guild.id)][0] == "on" and not message.author.bot:
      with open('automod_lists.json', 'r') as f:
        banned_words = json.load(f)
      if str(message.guild.id) not in banned_words:
        banned_words[str(message.guild.id)] = []
      cnt = message.content.lower() 
      words = banned_words[str(message.guild.id)]
      for i in re.split('[ ?!|\,._;:]', cnt):
        if i in words and not message.content.startswith(str(await self.client.get_prefix(message))): 
          member = message.author
          await message.channel.send(f">>> ⛔ **Watch your language, {member.mention}.**", delete_after = 10)
          await message.delete()
          break
    
      



  
  
        



#total in moderation.py: 15