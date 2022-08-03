import discord
import json
import requests
from discord.ext import commands
from PIL import Image, ImageOps
from io import BytesIO


class Leaderboard(commands.Cog):
  def __init__(self, client):
    self.client = client
   

  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Leaderboard Cog loaded!")
  
  @commands.command(name="glb")
  async def glb(self, ctx):
    with open("levels.json", "r") as f:
      data = json.load(f)
    card = discord.Embed(title="**:trophy: Global Leaderboard :trophy:**", color=0x00d1c6)
    first, second, third = sorted(data, key=lambda x: data[x]["totalxp"], reverse=True)[:3]
    first, second, third = await self.client.fetch_user(first), await self.client.fetch_user(second), await self.client.fetch_user(third)

    mask = Image.open('mask.png').convert('L')
    image = Image.new('RGB', (256 * 3, 256))
    for i, user in enumerate([first, second, third]):
        img = Image.open(BytesIO(requests.get(user.avatar_url).content)).resize((246, 246))
        image.paste(img, (i * 256, 5))
    image = ImageOps.fit(image, image.size, centering=(0.5, 0.5))
    image.putalpha(mask)
    border = Image.open("border.png")
    #image.paste(border, (0, 0), border)
    with BytesIO() as bytes_io:
        image.save(bytes_io, 'PNG')
        bytes_io.seek(0)
        file = discord.File(fp=bytes_io, filename="image.png")
    card.add_field(name="🥇 #1:",
                   value=f"**{first}**:\n`{data[str(first.id)]['commands']}` commands")
    card.add_field(name="🥈 #2:",
                   value=f"**{second}**:\n`{data[str(second.id)]['commands']}` commands")
    card.add_field(name="🥉 #3:",
                   value=f"**{third}**:\n`{data[str(third.id)]['commands']}` commands")

    card.set_image(url="attachment://image.png")
    await ctx.send(file=file, embed=card)
  #total: 1