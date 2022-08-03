import discord
from discord.ext import commands
from google_translate_py import Translator
import random
import re

class Math(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Math Cog loaded!")

    
# [CALCULATOR]
  @commands.command(aliases=["cal", "calc"])
  async def calculate(self, ctx, expression : str):
    expressionBackup = expression
    nums = re.split('[!-/]+', expression)
    operators = re.split('[0-9]+', expression)
    # print(*nums)
    # print(*operators)

    curr = 0
    next = nums[0]
    
    """for i in range(len(operators)):
      if operators[i] == "+":
        curr = curr + int(nums[i])
      if operators[i] == "-":
        curr = curr - int(nums[i])
      if operators[i] == "*":
        curr = curr * int(nums[i])
      if operators[i] == "/":
        curr = curr / int(nums[i])"""

    # print(curr)
    # print(eval(expression))

    expression = expression.replace(" ", "")
    
    if not re.search("[a-zA-Z]", expression):
      if "^" in expression or "**" in expression:
        expression = expression.replace("^", "**")
        limit = 10
      else:
        limit = 50

    
      if len(expression) <= limit:
        
        try:
          await ctx.send(f">>> 🧮 **Input:** `{expressionBackup}` \n🔢 **Result:** `{eval(expression)}`")
        except ZeroDivisionError:
          await ctx.send(f">>> <:no:984361059420880896> Can't divide by zero!",delete_after=10)

      else:
        await ctx.send("> <:no:984361059420880896> **Your calculation is too long!**",delete_after=10)
    else:
      await ctx.send("> <:no:984361059420880896> **Invalid input!**",delete_after=10)
        
    
      
# [RNG]
  @commands.command(aliases=["rng","rand"])
  async def random(self, ctx,num1=-9999999, num2=9999999):
    num1 = int(num1)
    num2 = int(num2)
    res = random.randint(num1, num2)
    await ctx.send(f">>> 🔢 **{res}** is a random number from  **{num1}** to **{num2}**.")

  #total in math.py: 2