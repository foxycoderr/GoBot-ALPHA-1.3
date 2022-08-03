import discord
from discord.ext import commands
from google_translate_py import Translator
from googletrans import Translator


class Translate(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Translator Cog loaded!")


  @commands.command(aliases = ["trans", "trs", "tr"])
  async def translate(ctx, lang, *, thing):
    translator = Translator()
    translation = translator.translate(thing, dest=ctx)
    await ctx.send(f">>> **📃 Original text:** {thing}**\n🌎 Translated Text: **{translation}")