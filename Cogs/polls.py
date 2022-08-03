from discord.ext import commands


class Polls(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Polls Cog loaded!")
    
  @commands.command(aliases=["poll"])
  @commands.has_permissions(manage_roles=True)
  async def pstart(self, ctx, choice : int = None):
    choices = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    if choice == None:
      if ctx.message.reference:
        msg = ctx.message.reference.resolved
      else: 
        await ctx.message.delete()
        return await ctx.send("**❌ No reference was given.**", delete_after = 7) 
      await msg.add_reaction("✅")
      await msg.add_reaction("❌")
      await ctx.send(f"**✅ Created poll with 2 choices.**", reference = msg)
      return
    if type(choice) != int:
      return await ctx.send("**❌ Invalid choices number.**", delete_after = 7)
      
    if choice > 10 or choice < 1:
      await ctx.message.delete()
      return await ctx.send("**❌ Invalid choices number.**", delete_after = 7)
    if ctx.message.reference:
      msg = ctx.message.reference.resolved
    else: 
      await ctx.message.delete()
      return await ctx.send("**❌ No reference was given.**", delete_after = 7)   
    for i in range(choice):
      await msg.add_reaction(choices[i])
    await ctx.send(f"**✅ Created poll with {choice} choices**", delete_after = 4, reference = msg)
    await ctx.message.delete()
    #total in polls.py: 1 
