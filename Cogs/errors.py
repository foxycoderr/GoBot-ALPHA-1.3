import discord
from discord.ext import commands

class Errors(commands.Cog):
  def __init__(self, client):
    self.client = client

  
  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Errors Cog loaded!")
    
  @commands.Cog.listener()
  async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):

      if isinstance(error, commands.CommandNotFound):
          message = ">>> <:no:984361059420880896> **The command that you tried to use does not exist, please refer to our documentation <https://docs.google.com/document/d/13pOQINkxeKjstf_fr4stBy3KWS52-UekLbFh6oR_whc/edit?usp=sharing> for more info on comands!**"
      elif isinstance(error, commands.MissingPermissions):
          message = f">>> <:no:984361059420880896> **You are missing the required permissions (`{error.missing_perms}`)to run this command!**"
      elif isinstance(error, commands.UserInputError): 
          message = ">>> <:no:984361059420880896> **Invalid arguments given, please refer to our documentation <https://docs.google.com/document/d/13pOQINkxeKjstf_fr4stBy3KWS52-UekLbFh6oR_whc/edit?usp=sharing> for more info on comands!**"
      else:
          message = ">>> <:no:984361059420880896> **Oh no!** An unknown error occured while running the command. Please refer to our documentation <https://docs.google.com/document/d/13pOQINkxeKjstf_fr4stBy3KWS52-UekLbFh6oR_whc/edit?usp=sharing>, check that you are using the command correctly, and try again." 

      await ctx.send(message, delete_after=10)
      await ctx.message.delete(delay=10)
    #total in errors.py: LOL 0