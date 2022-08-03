import discord
import json
from discord.ext import commands
from time import time
import asyncio
from random import randint
from math import ceil
class Tic(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Tic-Tac-Toe Cog loaded!")

  @commands.command(aliases=["tic", "tac", "toe", "ttt"])
  async def tictactoe(self, ctx, p2 = None):
    if p2 == None:
      await ctx.send("> :x: **No player/square name given!**")
    else:
      p1 = ctx.message.author
      try:
        p2 = int(p2)
      except ValueError:
        pass
      with open("tictactoe.json", "r") as f: 
        data = json.loads(f.read())
      i = 0
      while (i < len(data)):
        if time() - data[i][3] > 180:
          del data[i]
          i -= 1
        i += 1
      with open("tictactoe.json", "w") as f:
        json.dump(data,f)
      n = 0
      for i in range(len(data)):
          if p1.id in data[i]:
            datatmp = i
            print("test0")
            n = 1
            break
      if (ctx.message.mentions and n == 0):
        
        p2 = ctx.message.mentions[0]
      
        for i in range(len(data)):
          if p2.id in data[i]:
            n = 1
            break
        if n == 0:
          
          embedt = discord.Embed(title="❌ Tic-Tac-Toe! ⭕", description=f"{ctx.message.author.mention} invited {ctx.message.mentions[0].mention} to the game!", color = 0x00d1c6)
          embedt.set_footer(text="Do you want to play? React with <:yes:984360144047571014>") 
          message = await ctx.send(embed = embedt)
          await message.add_reaction("<:yes:984360144047571014>")
          #Next we need to react on reactions (??)
          #If reaction is ✅ we start the game
          #else we cancel it
          new_msg = await ctx.channel.fetch_message(message.id)
          tmpvar = 0
          tmpvar1 = 0
          check = lambda reaction, user: self.client.user != user and reaction.message == new_msg
          timer = time()
          while time() - timer < 60:
            if (tmpvar and tmpvar1):
              break
            res = await self.client.wait_for("reaction_add", check=check)
            if res:
              if res[1] == p1:
                tmpvar = 1
              if res[1] == p2:
                tmpvar1 = 1
          with open("tictactoe.json", "r") as f: 
            data = json.loads(f.read())
          for i in range(len(data)):
            if p2.id in data[i] or p1.id in data[i]:
              n = 1
              break  
          if (n == 1 and time() - timer < 60):
            await ctx.channel.send(">>> **<:no:984361059420880896> Sorry, you or your partner hasn't finished their previous game.**", reference = new_msg)
          elif (tmpvar == 1 and tmpvar1 == 1 and time() - timer < 60): 
            turn = randint(1,2)
            x = turn
            d = [p1.id, p2.id, [[":black_large_square:",":black_large_square:",":black_large_square:"],[":black_large_square:",":black_large_square:",":black_large_square:"],[":black_large_square:",":black_large_square:",":black_large_square:"]], round(time()), turn, x]
            data.append(d)
            with open("tictactoe.json", "w") as f:
              json.dump(data,f)
            await ctx.channel.send(">>> **<:yes:984360144047571014> Tic-Tac-Toe between {} and {} begins:\n{}{}{}\n{}{}{}\n{}{}{}**".format(p1.mention, p2.mention, d[2][0][0], d[2][0][1], d[2][0][2], d[2][1][0], d[2][1][1], d[2][1][2], d[2][2][0], d[2][2][1], d[2][0][2])) # tictactoe.json 
            if turn == 1:
              await ctx.channel.send(">>> **It's {} turn!**".format(p1.mention))
            else:
              await ctx.channel.send(">>> **It's {} turn!**".format(p2.mention))
          else:
            await ctx.channel.send(f">>> **<:no:984361059420880896> Sorry {p1.mention} and {p2.mention}, not both of you want to play.**", reference = new_msg)
            data.remove(d)
        else:
          await ctx.channel.send(f">>> **<:no:984361059420880896> Sorry {p1.mention}, {p2.mention} hasn't finished his(her) previous game.**", reference = new_msg)
      elif (type(p2) == int and n == 1):
        p2 = int(p2)
        print("test1")
        if (((p1.id == data[datatmp][0] and data[datatmp][4] == 1) or (p1.id == data[datatmp][1] and data[datatmp][4] == 2))):
          if (p2 > 0 and p2 < 10):
            v1 = ceil(p2 / 3.0) - 1
            p2 = p2 % 3 - 1
            if (data[datatmp][2][v1][p2] == ":black_large_square:"):
              if data[datatmp][data[datatmp][5]-1] == p1.id:
                data[datatmp][2][v1][p2] = '❌'
              else:
                data[datatmp][2][v1][p2] = '⭕'
              if data[datatmp][4] == 1:
                data[datatmp][4] = 2
              else:  
                data[datatmp][4] = 1
              data[datatmp][3] = round(time())
              await ctx.channel.send(">>> **<:yes:984360144047571014> Current field:\n{}{}{}\n{}{}{}\n{}{}{}**".format(data[datatmp][2][0][0], data[datatmp][2][0][1], data[datatmp][2][0][2], data[datatmp][2][1][0], data[datatmp][2][1][1], data[datatmp][2][1][2], data[datatmp][2][2][0], data[datatmp][2][2][1], data[datatmp][2][2][2])) # Attention: too many ifs
              if (data[datatmp][2][0][0] == data[datatmp][2][0][1] == data[datatmp][2][0][2] and data[datatmp][2][0][0] != ":black_large_square:"):
                  await ctx.channel.send(f">>> **🥇 {p1.mention} has won!!!**",delete_after=20)
                  del data[datatmp]
              elif (data[datatmp][2][1][0] == data[datatmp][2][1][1] == data[datatmp][2][1][2] and data[datatmp][2][1][0] != ":black_large_square:"):
                await ctx.channel.send(f">>> **🥇 {p1.mention} has won!!!**",delete_after=20)
                del data[datatmp]
              elif (data[datatmp][2][2][0] == data[datatmp][2][2][1] == data[datatmp][2][2][2] and data[datatmp][2][2][0] != ":black_large_square:"):
                await ctx.channel.send(f">>> **🥇 {p1.mention} has won!!!**",delete_after=20)
                del data[datatmp]
              elif (data[datatmp][2][0][0] == data[datatmp][2][1][0] == data[datatmp][2][2][0] and data[datatmp][2][0][0] != ":black_large_square:"):
                await ctx.channel.send(f">>> **🥇 {p1.mention} has won!!!**",delete_after=20)
                del data[datatmp]
              elif (data[datatmp][2][0][1] == data[datatmp][2][1][1] == data[datatmp][2][2][1] and data[datatmp][2][0][1] != ":black_large_square:"):
                await ctx.channel.send(f">>> **🥇 {p1.mention} has won!!!**",delete_after=20)
                del data[datatmp]
              elif (data[datatmp][2][0][2] == data[datatmp][2][1][2] == data[datatmp][2][2][2] and data[datatmp][2][0][2] != ":black_large_square:"):
                await ctx.channel.send(f">>> **🥇 {p1.mention} has won!!!**",delete_after=20)
                del data[datatmp]
              elif (data[datatmp][2][0][0] == data[datatmp][2][1][1] == data[datatmp][2][2][2] and data[datatmp][2][0][0] != ":black_large_square:"):
                await ctx.channel.send(f">>> **🥇 {p1.mention} has won!!!**",delete_after=20)
                del data[datatmp]
              elif (data[datatmp][2][0][2] == data[datatmp][2][1][1] == data[datatmp][2][2][0] and data[datatmp][2][0][2] != ":black_large_square:"):
                await ctx.channel.send(f">>> **🥇 {p1.mention} has won!!!**",delete_after=20)
                del data[datatmp]
              elif ":black_large_square:" not in data[datatmp][2][0] and ":black_large_square:" not in data[datatmp][2][1] and ":black_large_square:" not in data[datatmp][2][2]:
                if data[datatmp][0] == p1.id:
                  await ctx.channel.send(f">>> ⚖️ **{p1.mention} and {ctx.guild.get_member(data[datatmp][1]).mention} have played a draw!**",delete_after=20)
                  
                else:
                  await ctx.channel.send(f">>> ⚖️ **{p1.mention} and {ctx.guild.get_member(data[datatmp][0]).mention} have played a draw!**",delete_after=20)
                del data[datatmp]
              else:
                if data[datatmp][0] == p1.id:
                  await ctx.channel.send(">>> **It's {} turn!**".format(ctx.guild.get_member(data[datatmp][1]).mention),delete_after=60)
                else:
                  await ctx.channel.send(">>> **It's {} turn!**".format(ctx.guild.get_member(data[datatmp][0]).mention),delete_after=60)
            else:
              await ctx.channel.send(f">>> ** <:no:984361059420880896> This square isn't free, {p1.mention}.**",delete_after=30)
          else:
            await ctx.channel.send(f">>> ** <:no:984361059420880896> Your number is incorrect, {p1.mention}.**",delete_after=30)
        else:
          await ctx.channel.send(f">>> ** <:no:984361059420880896> It isn't your turn, {p1.mention}.**",delete_after=10)
      elif (type(p2) == int and n == 0):
        await ctx.channel.send(f">>> ** <:no:984361059420880896> You aren't playing at the moment, {p1.mention}.**",delete_after=10)
      elif (ctx.message.mentions and n == 1):
        await ctx.channel.send(">>> ** <:no:984361059420880896> Sorry, you haven't finished your previous game.**",delete_after=10)
      elif (type(p2 == str) and n == 1):
        if (p2 == "terminate" or p2 == "stop"):
          if (p1.id == data[datatmp][0]):
            await ctx.channel.send(">>> **<:yes:984360144047571014> Game between {} and {} was successfully terminated.**".format(p1.mention, ctx.guild.get_member(data[datatmp][1]).mention),delete_after=20)
          else:
            await ctx.channel.send(">>> **<:yes:984360144047571014> Game between {} and {} was successfully terminated.**".format(p1.mention, ctx.guild.get_member(data[datatmp][0]).mention),delete_after=20)
          del data[datatmp]
        
      
      with open("tictactoe.json", "w") as f:
        json.dump(data,f)

 #total: 1   