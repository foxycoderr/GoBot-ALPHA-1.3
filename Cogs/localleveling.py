import discord
import json
import random
#from discord import File
from discord.ext import commands
from typing import Optional
#from easy_pil import Editor
from PIL import Image, ImageFont, ImageDraw, ImageColor
import io
import re
import requests
async def level_maker(background,avatar,username,current_exp:int,level:int,max_exp:int,bar_color:str, rank:int, cx, userr):
    with open ("locallevels.json", "r")as f:
      data = json.load(f)
    avatar = Image.open(io.BytesIO(requests.get(avatar).content)).resize((120, 120))
    if data[str(cx.guild.id)][str(userr.id)][3] == -1:
      img = avatar.copy()
      img = img.convert("RGB")
      img = img.resize((1, 1), resample=0)
      dominant_color = img.getpixel((0, 0))
      overlay = Image.new("RGBA", (590, 140), (*dominant_color, 50))
      background = Image.new("RGBA", (640, 190), dominant_color)
      background.paste(overlay,(25,25),overlay)     
    elif data[str(cx.guild.id)][str(userr.id)][3] == 0:
      dominant_color = data[str(cx.guild.id)][str(userr.id)][4]
      dominant_color = ImageColor.getcolor(dominant_color, "RGB")
      overlay = Image.new("RGBA", (590, 140), (*dominant_color, 50))
      background = Image.new("RGBA", (640, 190), dominant_color)
      background.paste(overlay,(25,25),overlay)
    elif data[str(cx.guild.id)][str(userr.id)][3] == 1:
      pass #bob

    myFont = ImageFont.truetype("./assets/font.ttf",40)
    draw = ImageDraw.Draw(background)

    draw.text((177,(190/2) - 35), username,font=myFont, fill="white",stroke_width=1,stroke_fill=(0, 0, 0))
    bar_exp = (current_exp/max_exp)*420
    if bar_exp <= 50:
        bar_exp = 50    

    try:
        if current_exp >= 100000:
            current_exp = str(current_exp)[0:3] + "." + str(current_exp)[3] + "k"
    
        if max_exp >= 100000:
            max_exp = str(max_exp)[0:3] + "." + str(max_exp)[3] + "k"
    except Exception:
        pass
    
    
    try:
        if current_exp >= 10000:
            current_exp = str(current_exp)[0:2] + "." + str(current_exp)[2] + "k"
    
        if max_exp >= 10000:
            max_exp = str(max_exp)[0:2] + "." + str(max_exp)[2] + "k"
    except Exception:
        pass
    


    try:
        if current_exp >= 1000:
            current_exp = str(current_exp)[0]+"."+str(current_exp)[1]+"k"
    
        if max_exp >= 1000:
            max_exp = str(max_exp)[0]+"."+str(max_exp)[1]+"k"
    except Exception:
        pass

    myFont = ImageFont.truetype("./assets/font.ttf",30)
    draw.text((177,(190/2)+30), f"Level {level}",font=myFont, fill="white",stroke_width=1,stroke_fill=(0, 0, 0))
    draw.text((475,(190/2)-25), f"Rank #{rank}",font=myFont, fill="white",stroke_width=1,stroke_fill=(0, 0, 0))
    draw.text((475,(190/2)+30), f"{current_exp}/{max_exp}",font=myFont, fill="white",stroke_width=1,stroke_fill=(0, 0, 0))
    
    mask_im = Image.open("./assets/mask_circle.jpg").convert('L').resize((120,120))
    background.paste(avatar, (35, 35), mask_im)
    
    im = Image.new("RGBA", (420, 11), (*dominant_color, 0))
    draw = ImageDraw.Draw(im, "RGBA")
    draw.rounded_rectangle((0, 0, 420, 10), 30, fill=(255,255,255,50))
    draw.rounded_rectangle((0, 0, bar_exp, 10), 30, fill=bar_color)
    background.paste(im, (170, 105))
    f= open("./level.png", "wb") 
    background.save(f, "PNG")
    return "./level.png"

class LocalLeveling(commands.Cog):
  def __init__(self, client):
    self.client = client
   
  
  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Leveling Cog loaded!")

  @commands.Cog.listener()
  async def on_message(self, message):
    
    def get_prefix(message):
      with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
      return prefixes[str(message.guild.id)]
      

    if not message.author.bot:
      with open("locallevels.json", "r") as f:
        data = json.load(f)
   
      if str(message.guild.id) in data:
        if str(message.author.id) in data[str(message.guild.id)]:
          xp = data[str(message.guild.id)][str(message.author.id)][0]
          level = data[str(message.guild.id)][str(message.author.id)][1]
          totalxp = data[str(message.guild.id)][str(message.author.id)][2]
          
          randnum=random.randint(20, 50)
          incr_xp = xp+randnum
          new_level = int(incr_xp/100)
          data[str(message.guild.id)][str(message.author.id)][0]=incr_xp
          data[str(message.guild.id)][str(message.author.id)][2]=totalxp+randnum

          with open("locallevels.json","w")as f:
            json.dump(data,f)
          if new_level > level:
            await message.channel.send(f">>> **GGs** {message.author.mention}, you are now on level `{new_level}` 🔥", delete_after=20)
            data[str(message.guild.id)][str(message.author.id)][1]=new_level
            data[str(message.guild.id)][str(message.author.id)][0]=0
            
            with open("locallevels.json","w")as f:
              json.dump(data,f)
  
        else:
          print("BOBBBB")
          data[str(message.guild.id)][str(message.author.id)] = [0,1,0, -1, 'o']
          with open("locallevels.json","w")as f:
            json.dump(data,f)
      else:
        data[str(message.guild.id)] = {str(message.author.id):[0, 1, 0, -1, 'o']}
        with open("locallevels.json", "w") as f:
          json.dump(data,f)

  @commands.command(name="rank")
  async def rank(self,ctx: commands.Context, user: Optional[discord.Member]):
    userr = user or ctx.author
    if userr.bot: 
      return
    with open ("locallevels.json", "r")as f:
      data = json.load(f)
    if not str(ctx.guild.id) in data:
      data[str(ctx.guild.id)] = {}
    if not str(userr.id) in data[str(ctx.guild.id)]:
      data[str(ctx.guild.id)][str(userr.id)] = [0, 1, 0, -1, 'o']
    ranks = sorted(data[str(ctx.guild.id)], key=lambda x: data[str(ctx.guild.id)][str(x)][2], reverse=True)
    with open("locallevels.json","w") as f:
      json.dump(data,f) 
    level = data[str(ctx.guild.id)][str(userr.id)][1]
    rank = ranks.index(str(userr.id)) + 1
    next_level_up_xp = (level+1)*100
    xp_need = next_level_up_xp
    xp_have = data[str(ctx.guild.id)][str(userr.id)][0]
    
    await level_maker(userr.avatar_url, userr.avatar_url,userr.name,xp_have,level,xp_need,"#00ff00", rank, ctx, userr)
    file = discord.File("./level.png", filename="level.png")
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
    await ctx.send(file=file)

  @commands.command(name="rank_color")
  async def rank_color(self,ctx: commands.Context, color : str = None):
    with open("locallevels.json", "r") as f:
      data = json.load(f)
    HEX_COLOR_REGEX = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    def is_hex_color(input_string):
      regexp = re.compile(HEX_COLOR_REGEX)
      if regexp.search(input_string):
        return True
      return False
    if str(ctx.guild.id) not in data:
      data[str(ctx.guild.id)] = {}
    if str(ctx.author.id) not in data[str(ctx.guild.id)]:
      data[str(ctx.guild.id)][str(ctx.author.id)] = [0, 1, 0, -1, 'o']
    if color == None:
      data[str(ctx.guild.id)][str(ctx.author.id)][3] = -1
      data[str(ctx.guild.id)][str(ctx.author.id)][4] = 'o'
      await ctx.send("**Rank card color has been set to default.**", delete_after = 10)
    elif is_hex_color(color) == True:
      data[str(ctx.guild.id)][str(ctx.author.id)][3] = 0
      if len(data[str(ctx.guild.id)][str(ctx.author.id)]) == 5:
        data[str(ctx.guild.id)][str(ctx.author.id)][4] = color
      else:
        data[str(ctx.guild.id)][str(ctx.author.id)].append(color)
      await ctx.send(f"**Rank card color has been set to {color}.**", delete_after = 10)
    else:
      await ctx.send(f"**Invalid input.**", delete_after = 10)
    with open("locallevels.json","w") as f:
      json.dump(data,f)
#total in localleveling.py: 2
    