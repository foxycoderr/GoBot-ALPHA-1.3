import discord
from discord.ext import commands
import random
import os
from requests import get
import json
import asyncio
from requests import request
class Fun(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Memes Cog loaded!")

  """@commands.Cog.listener()
  async def on_message(self, message):         
    emojis = message.guild.emojis
    if (random.randint(1, 100) <= 6 and not message.author.bot):
      await message.add_reaction(random.choice(emojis))"""
# [MEMES]
  @commands.command(aliases = ["mem","mm", "mee"])
  async def meme(self, ctx):
    content = get("https://meme-api.herokuapp.com/gimme").text
    data = json.loads(content,)
    meme = discord.Embed(title=f"{data['title']}", description="This is your own personal meme. Ha ha 🤣", colour = 0x487799, timestamp = ctx.message.created_at)
    meme.set_image(url=f"{data['url']}")
    await ctx.send(embed=meme)


# [8-BALL]
  @commands.command(aliases = ["8ball", "8-ball", "8bl"])
  async def ball(self, ctx):
      result = discord.Embed(title="🎱 8-Ball", description="🪄 Rolling your ball...", color=0x487799, timestamp = ctx.message.created_at)
      res1 = "❌ Obviously not."
      res2 = "😃 Of course!"
      res3 = "🤔 Hmm ... I don't know."
      res4 = "😒 I don't think so."
      res5 = "✅ Well, I think so."
      res6 = "⛔ Simply put ... no." # Its 8-ball not 6-ball
      results = [res1, res2, res3, res4, res5, res6]
      res = random.choice(results)

      result.add_field(name="Result:", value=str(res))
      await ctx.message.channel.send(embed=result)

# [GIFS]
  @commands.command(aliases = ["fed", "food", "fd"])
  async def feed(self, ctx, member: discord.Member):
    joke = discord.Embed(title="Feeding time!", description=f"{ctx.message.author} fed {member}!", color=0x00d1c6, timestamp = ctx.message.created_at)
    j1 = "https://appetitetoplay.com/sites/default/files/styles/1200x630_2x/public/2019-03/goat-3017394_1920.jpg?itok=js9fdBYT"
    j2 = "https://www.resqct.org/images-blog/content/147/Responsible%20feeding%201-min.jpg"
    j3 = "https://www.dacsa.com/wp-content/uploads/2019/08/cabra.jpg"
    j4 = "https://images.unsplash.com/photo-1619869254964-bdb48f5ed5e1?ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8ZmVlZGluZyUyMGFuaW1hbHN8ZW58MHx8MHx8&ixlib=rb-1.2.1&w=1000&q=80"
    j5 = "https://www.slowfood.com/wp-content/uploads/2016/06/Mangalica_Breed_Pig-1024x683.png"
    j6 = "https://ugc.futurelearn.com/uploads/images/dd/f6/header_ddf6b560-c986-42d7-af3b-04d3dc0b272e.jpg"
    j7 = "https://images.unsplash.com/photo-1618760439064-9c608de98e4e?ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8ZmVlZGluZyUyMGFuaW1hbHN8ZW58MHx8MHx8&ixlib=rb-1.2.1&w=1000&q=80"
    gifs = [j1, j2, j3, j4, j5, j6]
    joke.set_image(url=random.choice(gifs))
    await ctx.send(embed=joke)

  @commands.command(aliases = ["kl", "kil"])
  async def kill(self, ctx, member: discord.Member):
    joke = discord.Embed(title="One shot. One kill.", description=f"{ctx.message.author} just murdered {member}!", color=0x00d1c6, timestamp = ctx.message.created_at)
    j1 = "https://www.gamespot.com/a/uploads/screen_kubrick/1574/15747411/3740969-desktopscreenshot2020.09.30-11.05.15.68.jpg"
    j2 = "https://www.windowscentral.com/sites/wpcentral.com/files/styles/large/public/article_images/2020/09/among-us-kill-death-6549.jpg"
    j3 = "https://filmdaily.co/wp-content/uploads/2020/10/imposter-lede--1300x720.jpg"
    j4 = "https://static3.srcdn.com/wordpress/wp-content/uploads/2020/10/Among-Us-Gun-Kill-Animation.jpg?q=50&fit=crop&w=740&h=370&dpr=1.5"
    gifs = [j1, j2, j3, j4]
    joke.set_image(url=random.choice(gifs))
    await ctx.send(embed=joke)



# [DICE]
  @commands.command(aliases = ["die", "di"])
  async def dice(self, ctx, number=1):
      result = discord.Embed(title="🎲 Dice roller", description="🪄 Rolling your dice...", color=0x00d1c6, timestamp = ctx.message.created_at)
      res1 = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Terning1.svg/180px-Terning1.svg.png"
      res2 = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Terning2.svg/180px-Terning2.svg.png"
      res3 = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Terning3.svg/180px-Terning3.svg.png"
      res4 = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Terning4.svg/180px-Terning4.svg.png"
      res5 = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Terning5.svg/180px-Terning5.svg.png"
      res6 = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Terning6.svg/180px-Terning6.svg.png"
      number = int(number)
      results = [res1, res2, res3, res4, res5, res6]
      if number > 5:
        number = 5
      res = random.choice(results)
      result.set_thumbnail(url=str(res))
      await ctx.message.delete(delay=0)
      result.add_field(name="No. of dice rolled", value = number)
      num2 = 1
      result.set_footer(text=f"Index of current dice: {num2}")
      message = await ctx.message.channel.send(embed=result)
      for i in range (number-1):
        res = random.choice(results)
        result.set_thumbnail(url=str(res))
        num2 += 1
        result.set_footer(text=f"Index of current dice: {num2}")
        await asyncio.sleep(3)
        await message.edit(embed=result)
# [COINFLIP]
  @commands.command(aliases = ["cflip", "coinfl", "cf"])
  async def coinflip(self, ctx):
    res = ["Heads", "Tails"]
    await ctx.send(f"🪙 You flipped **{random.choice(res)}**!")

# [FUN FACT]
  @commands.command()
  async def fact(self, ctx):
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    response = request("GET", url)  
    data = json.loads(response.text)
    useless_fact = data['text']
    await ctx.send(useless_fact)

#total in fun.py: 7
# Thinking... 