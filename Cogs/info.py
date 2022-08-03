import discord
from discord_ui import Components, UI, Button
from discord.ext import commands
import json



class Info(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  
  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Info Cog loaded!")

    
  @commands.command()
  async def help(self, ctx):
    def get_prefix(guildd):
      with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
      return prefixes[str(guildd)]

      
    Embed = discord.Embed(title="GoBot Commands", description=f"The default prefix of GoBot is `?`. This server's prefix is `{get_prefix(ctx.guild.id)}`.", colour=0x00d1c6, timestamp = ctx.message.created_at)
    Embed.add_field(name="📖 Command List", value="[Click here](https://docs.google.com/document/d/13pOQINkxeKjstf_fr4stBy3KWS52-UekLbFh6oR_whc/edit?usp=sharing)")
    Embed.add_field(name="💻 Official Website", value="[Click here](https://galguard.webflow.io)")
    Embed.add_field(name="📄 Privacy Statement", value="[Click here](https://docs.google.com/document/d/18L_0WKUgec8iYUksnTr-DRRuPe_k_3rtk3lN9HQ6850/edit?usp=sharing)")
    Embed.add_field(name="👋🏼 Invite link", value="[Click here](https://discord.com/api/oauth2/authorize?client_id=963457369310916678&permissions=8&scope=bot)")
    await ctx.send(embed=Embed)
           
  
     
  @commands.command()
  async def info(self, ctx):
    def get_value(file:str, value:str):
      with open(f'{file}.json', 'r') as f:
          values = json.load(f)
      return values[str(f"{value}")]


    file = "commands"
    value1 = "commands"
    value2 = "users"
    Embed = discord.Embed(title="🤖 Bot Information", description=f"Note that the bot is still in development.", colour=0x00d1c6, timestamp = ctx.message.created_at)
    Embed.add_field(name="🖥️ Version:",value="1.3", inline=False)
    Embed.add_field(name="🔢 Number of commands:",value="`51`", inline=False)
    Embed.add_field(name="🕒 Last update:",value="22/07/2022", inline=False)
    Embed.add_field(name="📃 Change Logs Page:",value="[Click here](https://docs.google.com/document/d/1hEYtR_Gz1CJO_Q2uDYY_05OFcCYBlZAlV0zVTE-6bW8/edit?usp=sharing)", inline=False)
    Embed.add_field(name="💻 Website:",value="[Click here](https://galguard.webflow.io)", inline=False)
    Embed.add_field(name="📨 Commands used",value=f"`{get_value(file, value1)}`", inline=False)
    Embed.add_field(name="🧑🏼 Unique Users",value=f"`{get_value(file, value2)}`", inline=False)
    await ctx.send(embed=Embed)

  @commands.command(aliases = ["srv", "server", "server_info"])
  async def serverinfo(self, ctx):
    role_count = len(ctx.guild.roles)
    list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]
  
    sqer = discord.Embed(title=f"📃 Information about {ctx.guild.name}", description="Below is some information about this server.", color=0x00d1c6, timestamp = ctx.message.created_at)
    sqer.add_field(name='🔤 Name', value=f"{ctx.guild.name}", inline = False) 
    sqer.add_field(name='🧑🏽 Member Count', value=f"{ctx.guild.member_count}", inline = False) 
    sqer.add_field(name='✅ Verification Level', value=f"{ctx.guild.verification_level}", inline = False) 
    sqer.add_field(name='👑 Highest Role', value=f"{ctx.guild.roles[-2]}", inline = False) 
    sqer.add_field(name='🔢 Number of Roles', value=str(role_count), inline = False) 
    sqer.set_footer(text=ctx.message.author) 
    sqer.set_thumbnail(url = ctx.guild.icon_url)
    await ctx.send(embed=sqer)

  @commands.command(aliases = ["mi", "member", "mb"])
  async def memberinfo(self, ctx, member: discord.Member):
    roles = [role for role in member.roles]
    sqer = discord.Embed(title=f"📃 Information about **{member}**", color=0x00d1c6, timestamp = ctx.message.created_at)
    sqer.add_field(name='🔤 Name', value=f"{member}", inline = False) 
    sqer.add_field(name='💻 Discord ID', value=f"{member.id}", inline = False) 
    sqer.add_field(name='🔖 Server nickname', value=f"{member.display_name}", inline = False)
    sqer.add_field(name='😄 Account created at:', value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline = False)
    sqer.add_field(name='👋🏽 Joined server at:', value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline = False)
    sqer.add_field(name=f'📑 Roles ({len(roles)})', value=", ".join([role.mention for role in roles]), inline = False)
    sqer.add_field(name='👑 Top role', value=f"{member.top_role.mention}", inline = False)
    sqer.add_field(name='🤖 Bot?', value=member.bot, inline = False)
     
    sqer.set_thumbnail(url = member.avatar_url)
    await ctx.send(embed=sqer)

  @commands.command()
  async def getid(self, ctx, user : discord.Member):
    await ctx.send(f">>> **{user.mention}**'s Discord ID is `{user.id}`")
#total in info.py: 5