import discord
from discord.ext import commands
import requests
import json


class Util(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Utility Cog loaded!")

    @commands.command(aliases=["weather", "wthr", "wttr"])
    async def getweather(self, ctx, *, city=None):
        if city != None:
            text = 'http://api.weatherapi.com/v1/current.json?key=9f11fd87b121459fb8c71013221206&q=' + city + '&aqi=yes'
        else:
            return await ctx.channel.send(
                ">>> ** <:no:984361059420880896> Error 404, city wasn't found.**"
            )
        if requests.get(text).status_code != 400:
            r = requests.get(text).text
            r = json.loads(r)
            embed = discord.Embed(title="Weather in " + r["location"]["name"],
                                  color=0x487799)
            embed.add_field(name="⌚ Current time: ",
                            value=r["location"]["localtime"])
            embed.add_field(name="🌡️ Temperature °C: ",
                            value=r["current"]["temp_c"])
            embed.add_field(name="🌡️ Temperature °F: ",
                            value=r["current"]["temp_f"])
            embed.add_field(name="🌦️ Condition: ",
                            value=r["current"]["condition"]["text"])
            embed.set_thumbnail(url="http:" +
                                r["current"]["condition"]["icon"])
            embed.add_field(name="💨 Wind speed: ",
                            value=str(r["current"]["wind_mph"]) + " mph")
            embed.add_field(name="📟 Pressure: ",
                            value=str(r["current"]["pressure_mb"]) + " mb")
            embed.add_field(name="☔ Precipitation: ",
                            value=str(r["current"]["precip_in"]) + " in")
            embed.add_field(name="💧 Humidity: ",
                            value=str(r["current"]["humidity"]) + " %")
            embed.add_field(name="🌫️ US-EPA Index (air qualiy): ",
                            value=r["current"]["air_quality"]["us-epa-index"])
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send(
                ">>> ** <:no:984361059420880896> Error 404, city wasn't found.**",
                delete_after=10)

    @commands.command(aliases=["time"])
    async def gettime(self, ctx, *, city=None):
        if city != None:
            text = 'http://api.weatherapi.com/v1/current.json?key=9f11fd87b121459fb8c71013221206&q=' + city + '&aqi=yes'
        else:
            return await ctx.channel.send(
                ">>> ** <:no:984361059420880896> Error 404, city wasn't found.**",
                delete_after=10)
        if requests.get(text).status_code != 400:
            r = requests.get(text).text
            r = json.loads(r)
            print(r)
            text = "**Current time in ** _" + r["location"]["name"] + ", " + r[
                "location"]["region"] + "_:  **" + r["location"][
                    "localtime"] + "**"
            hours = int(r["location"]["localtime"][-5:-3])
            print(hours)
            hours = hours % 12
            minutes = int(r["location"]["localtime"][-2:-1])
            print(minutes)
            emojis = [['🕛', '🕧'], ['🕐', '🕜'], ['🕑', '🕝'], ['🕒',
                                                           '🕞'], ['🕓', '🕟'],
                      ['🕔', '🕠'], ['🕕', '🕡'], ['🕖', '🕢'], ['🕗', '🕣'],
                      ['🕘', '🕤'], ['🕙', '🕥'], ['🕚', '🕦']]
            if (minutes >= 3):
                text = emojis[hours][1] + " " + text
            else:
                text = emojis[hours][0] + text
            await ctx.channel.send(text)
        else:
            await ctx.channel.send(
                ">>> ** <:no:984361059420880896> Error 404, city wasn't found.**",
                delete_after=10)

    @commands.command(aliases=["memb", "mbr"])
    async def members(self, ctx, role=None):
        try:
            role = role[3:-1]
            role = int(role)
            embed = discord.Embed(title="**" + ctx.guild.get_role(role).name +
                                  "**",
                                  color=0x487799,
                                  timestamp=ctx.message.created_at)
            text = ''
            n = 0
            for i in ctx.guild.get_role(role).members:
                f = ctx.guild.get_member(i.id)
                text = text + f.mention + ", "
                n += 1
            text = text[:-2]
            embed.add_field(name="👥 **Members: **", value=text, inline=False)
            embed.add_field(name="🔢 **Total member count:** ",
                            value=n,
                            inline=False)
            await ctx.send(embed=embed)
        except:
            await ctx.channel.send(
                ">>> ** <:no:984361059420880896> Incorrect input.**")

    @commands.command()
    async def avatar(self, ctx, *, member:discord.Member=None):
        if member != None:
            try:
                member = int(member)
            except Exception:
                pass
            if type(member) == int:
                member = await self.client.fetch_user(member)
            try:
                member = discord.member(member)
            except Exception:
                pass
            await ctx.send(f"**👤 {member.mention}'s avatar:**")
            await ctx.send(member.avatar_url)
        else:
            await ctx.send(f"**👤 Your avatar:**")
            await ctx.send(ctx.message.author.avatar_url)

    @commands.command(aliases=["set_nick", "nickname", "setnick", "nick"])
    @commands.has_permissions(change_nickname=True)
    async def set_nickname(self, ctx, *, nick: str = None):
        if nick != None:
            await ctx.send(f"**👤 Your nickname has been set to {nick}.**",
                           delete_after=10)
            await ctx.author.edit(nick=nick)
        else:
            await ctx.send(
                f"**👤 Your nickname has been set to {ctx.author.name}.**",
                delete_after=10)
            await ctx.author.edit(nick=ctx.author.name)
#total: 5