import discord
import json
import requests
from discord.ext import commands
from PIL import Image, ImageOps
from io import BytesIO


class LLeaderboard(commands.Cog):
  def __init__(self, client):
    self.client = client
   

  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Leaderboard Cog loaded!")
  
  @commands.command(name="lb")
  async def lb(self, ctx):
    with open("locallevels.json", "r") as f:
      data = json.load(f)
    card = discord.Embed(title="**:trophy: Server Leaderboard :trophy:**", color=0x00d1c6)
    
    ranks = sorted(data[str(ctx.guild.id)], key=lambda x: data[str(ctx.guild.id)][str(x)][2], reverse=True)
    
    first, second, third, fourth, fifth = ranks[0], ranks[1], ranks[2], ranks[3], ranks[4]
    
    
    
    first, second, third, fourth, fifth = await self.client.fetch_user(first), await self.client.fetch_user(second), await self.client.fetch_user(third), await self.client.fetch_user(fourth),await self.client.fetch_user(fifth)

    #mask = Image.open('mask.png').convert('L')
    #image = Image.new('RGB', (256 * 3, 256))
    #for i, user in enumerate([first, second, third]):
        #img = Image.open(BytesIO(requests.get(user.avatar_url).content)).resize((246, 246))
        #image.paste(img, (i * 256, 5))
    #image = ImageOps.fit(image, image.size, centering=(0.5, 0.5))
    #image.putalpha(mask)
    #border = Image.open("border.png")
    #image.paste(border, (0, 0), border)
    #with BytesIO() as bytes_io:
        #image.save(bytes_io, 'PNG')
        #bytes_io.seek(0)
        #file = discord.File(fp=bytes_io, filename="image.png")
    card.add_field(name="🥇 #1:",
                   value=f"**{first.mention}:** `level {data[str(ctx.guild.id)][str(first.id)][1]}` ", inline=False)
    card.add_field(name="🥈 #2:",
                   value=f"**{second.mention}:** `level {data[str(ctx.guild.id)][str(second.id)][1]}` ", inline=False)
    card.add_field(name="🥉 #3:",
                   value=f"**{third.mention}:** `level {data[str(ctx.guild.id)][str(third.id)][1]}` ", inline=False)
    card.add_field(name="#4:",
                   value=f"**{fourth.mention}:** `level {data[str(ctx.guild.id)][str(fourth.id)][1]}` ", inline=False)
    card.add_field(name="#5:",
                   value=f"**{fifth.mention}:** `level {data[str(ctx.guild.id)][str(fifth.id)][1]}` ", inline=False)
    

    #card.set_image(url="attachment://image.png")
    await ctx.send(embed=card)
  #total: 1