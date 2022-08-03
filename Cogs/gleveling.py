import discord
import json
import random

#from discord import File
from discord.ext import commands
from typing import Optional
#from easy_pil import Editor



class Leveling(commands.Cog):
  def __init__(self, client):
    self.client = client
   

  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Leveling Cog loaded!")

  @commands.Cog.listener()
  async def on_message(self,message):
    
    def get_prefix(message):
      with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
      return prefixes[str(message.guild.id)]
      
    commandss = [c.name for c in self.client.commands]
    
    bool = False
    
    for i in range (len(commandss)):
      if message.content.startswith(get_prefix(message)) and commandss[i] in message.content:
        bool = True
        
    if bool==True:
      if not message.author.bot:
        with open("levels.json", "r") as f:
          data = json.load(f)
        with open("commands.json", "r") as f:
          data1 = json.load(f)
        commands_used_total=data1["commands"]
        commands_used_total=int(commands_used_total)
        commands_used_total += 1
        data1["commands"]=str(commands_used_total)
        with open("commands.json","w")as f:
              json.dump(data1,f)



        
        if str(message.author.id) in data:
          xp = data[str(message.author.id)]['xp']
          level = data[str(message.author.id)]['level']
          no_of_commands = data[str(message.author.id)]['commands']
          totalxp = data[str(message.author.id)]['totalxp']
          
          randnum=random.randint(20, 50)
          incr_xp = xp+randnum
          new_level = int(incr_xp/100)
          no_of_commands = no_of_commands+1
          data[str(message.author.id)]['xp']=incr_xp
          data[str(message.author.id)]['commands']=no_of_commands
          data[str(message.author.id)]['totalxp']=totalxp+randnum

          with open("levels.json","w")as f:
            json.dump(data,f)
          if new_level > level:
            await message.author.send(f">>> **GGs** {message.author.mention}, you are now on level `{new_level}` in **GoBot** usage 🔥")
            data[str(message.author.id)]['level']=new_level
            data[str(message.author.id)]['xp']=0
            
            with open("levels.json","w")as f:
              json.dump(data,f)
  
              """for i in range(len(level)):
                if new_level == level_num[i]:
                  #await message.author.add_roles(discord.utils.get(message.author.guild.roles, name = level[i]))
  
                  mbed = discord.Embed(title = f"{message.other}You just got the role {level[i]}", color=message.author.color)
                  mbed.set_thumbnail(url=message.author.avatar_url)
                  await message.channel.send(embed = mbed)
                  """
  
        else:
          data[str(message.author.id)] = {}
          data[str(message.author.id)]['xp']= 0
          data[str(message.author.id)]['level']= 1
          data[str(message.author.id)]['commands']= 0
          data[str(message.author.id)]['totalxp']= 0

          with open("levels.json", "w") as f:
            json.dump(data,f)
          with open("commands.json", "r") as f:
            data2 = json.load(f)
          users=data2["users"]
          users=int(users)
          users += 1
          data2["users"]=str(users)
          with open("commands.json","w")as f:
            json.dump(data2,f)

  @commands.command(name="grank")
  async def grank(self,ctx: commands.Context, user: Optional[discord.Member]):
    userr = user or ctx.author
    
    with open ("levels.json", "r")as f:
      data = json.load(f)
    if not str(userr.id) in data:
      data[str(userr.id)] = {}
      data[str(userr.id)]['xp']= 0
      data[str(userr.id)]['level']= 1
      data[str(userr.id)]['commands']= 0
      data[str(userr.id)]['totalxp']= 0

      with open("levels.json","w")as f:
              json.dump(data,f)
      
    level = data[str(userr.id)]["level"]
    commandss = data[str(userr.id)]["commands"]
    total_xp = data[str(userr.id)]["totalxp"]
    
    next_level_up_xp = (level+1)*100
    xp_need = next_level_up_xp
    xp_have = data[str(userr.id)]["xp"]
    
    percentage = int(((xp_have*100/xp_need)))
    """background = editor("900300p1") 
    profile = await load_image_async(str(userr.avatar_url))
    #profile = editor(profile).resize((150,150)).circle_image()
    
    poppins = font.poppins(size=40)
    poppins_small = font.poppins(size=30)
  
    background.paste(profile.image,(30,30))
    background.rectangle((30,220),width=650,height=40,fill="#fff",radius = 20)
    #background.bar(
      #(30,220),
      #max_width=650,
      #height = 40,
      #percentage = percentage,
      #fill = "#ff9933",
      #radius = 20
    #)
    background.text((220,40), str(userr.name),font = poppins,color = "#ff9933" )
    background.rectange((220,40),width = 350,height = 2,fill = "#ff9933")
    background.text(
      (200,130),
      f"Level: {level}"
      + f"xp: {xp}/ {(level+1)*100}",
      font=poppins_small,
      color="#ff9933",
    )
    card = File(fp=background.image_bytes, filename = "900300p1")"""
    card=discord.Embed(title="🌎 Global GoBot Usage", description="Below are your stats of usage of GoBot globally (not only in this server).", color=0x00d1c6)
    card.add_field(name="📨 Commands sent:", value = int(commandss))
    card.add_field(name="👾 Level:", value = int(level), )
    card.add_field(name="🆙 XP needed to level up:", value = f"{int(xp_need)-int(xp_have)}")
    card.add_field(name="📈 Percentage to next level:", value = f"{int(percentage)}%")
    card.add_field(name="💰 XP collected:", value = int(total_xp))
    await ctx.send(embed=card)

#total in gleveling.py: 1
    