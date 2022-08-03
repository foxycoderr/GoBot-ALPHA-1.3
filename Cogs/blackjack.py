import discord
from discord.ext import commands
import random
import json
import datetime
class Blackjack(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("✅ Blackjack Cog loaded!")

  @commands.command(aliases=["bj"])
  async def blackjack(self, ctx, other_player:discord.Member):
    # setting variables
    guild_id = ctx.guild.id
    player1 = ctx.message.author
    player2 = other_player
    player1_id = player1.id
    player2_id = player2.id
    player1_score = random.randint(4, 20) # simplified for now, you cannot instantly win
    player2_score = random.randint(4, 20)

    # checks if both got 21
    if player1_score == player2_score and player1_score == 21:
      case = random.randint(0, 1)
      if case == 0:
        player1_score -= 1
      else:
        player2_score -= 1

    # uploading all game data
    with open('blackjack.json', 'r') as f:
      games = json.load(f)
    game_id = len(games)

    games[game_id] = {}
    games[game_id]["player1_id"] = player1_id
    games[game_id]["player2_id"] = player2_id
    games[game_id]["player1_score"] = player1_score
    games[game_id]["player2_score"] = player2_score
    games[game_id]["player1_status"] = "hitting"
    games[game_id]["player2_status"] = "hitting"
    games[game_id]["guild_id"] = guild_id

    with open('blackjack.json', 'w') as f:
      json.dump(games, f)
                        
    # sending people their scores
    await player1.send(f"Your score is currently at `{player1_score}`. Send `hit` or `stand` here to continue.")
    await player2.send(f"Your score is currently at `{player2_score}`. Send `hit` or `stand` here to continue.")


# seems to be OK until here




  
  @commands.Cog.listener()
  async def on_message(self, message):
    print("BP 0")
    author = message.author.id
    # checking if member is hitting or standing
    if message.content.lower() == "hit":
      print("BP 1")
      with open('blackjack.json', 'r') as f:
        games = json.load(f)
      last_id = len(games)

      for game in reversed(games):
        if games[game]["player1_id"] == author:
          guild_id = games[game]["guild_id"]
          guild = await self.client.fetch_guild(guild_id)

          games[game]["player1_score"] += random.randint(4, 11)
          # send player1 aknowledgement

          player1 = await guild.fetch_member(games[game]["player1_id"])
          await player1.send(f"You **HIT!** Your new sum is `{games[game]['player1_score']}`.")
          if games[game]["player1_score"] >= 21:
            # DM player2 he won
            player2 = guild.fetch_member(games[game]["player2_id"])
            await player2.send("You **WON!** Your opponent went over `21`.")
            # DM player1 he lost
            await player1.send("You **LOST!** You went over `21`.")
            # Remove game info from file
            finished_game_index = games.index(game)
            games.pop(finished_game_index)
            break
            
        elif games[game]["player2_id"] == author:
          guild_id = games[game]["guild_id"]
          guild = await self.client.fetch_guild(guild_id)
          
          games[game]["player2_score"] += random.randint(4, 11)
          # send player2 aknowledgement

          player2 = await guild.fetch_member(games[game]["player2_id"])
          await player2.send(f"You **HIT!** Your new sum is `{game['player2_score']}`.")
          if games[game]["player2_score"] >= 21:
            # DM player1 he won
            player1 = guild.fetch_member(games[game]["player1_id"])
            await player2.send("You **WON!** Your opponent went over `21`.")
            # DM player2 he lost
            await player2.send("You **LOST!** You went over `21`.")
            # Remove game info from file
            finished_game_index = games.index(game)
            games.pop(finished_game_index)
            break

            
      # writing all changes
      with open('blackjack.json', 'w') as f:
        json.dump(games, f)




    
    if message.content.lower() == "stand":
      with open('blackjack.json', 'r') as f:
        games = json.load(f)
      last_id = len(games)

      for game in reversed(games):
        if games[game]["player1_id"] == author:
          with open('blackjack.json', 'r') as f:
            games = json.load(f)
          games[game]["player1_status"] = "standing"
          if games[game]["player2_status"] == "standing":
            if games[game]["player1_score"] > games["player2_score"]:
              guild_id = games[game]["guild_id"]
              guild = await client.fetch_guild(guild_id)
              player1 = await guild.fetch_member(games[game]["player1_id"])
              player2 = await guild.fetch_member(games[game]["player2_id"])
              await player1.send(f"You **WON!** Your final score is `{games[game]['player1_score']}`, and your opponent's is `{games[game]['player2_score']}`.")
              await player2.send(f"You **LOST!** Your final score is `{games[game]['player2_score']}`, and your opponent's is `{games[game]['player1_score']}`.")
              
            elif games[game]["player2_score"] > games[game]["player1_score"]:
              guild_id = games[game]["guild_id"]
              guild = await client.fetch_guild(guild_id)
              player1 = await guild.fetch_member(games[game]["player1_id"])
              player2 = await guild.fetch_member(games[game]["player2_id"])
              await player2.send(f"You **WON!** Your final score is `{games[game]['player2_score']}`, and your opponent's is `{games[game]['player1_score']}`.")
              await player1.send(f"You **LOST!** Your final score is `{games[game]['player1_score']}`, and your opponent's is `{games[game]['player2_score']}`.")

            else:
              guild_id = games[game]["guild_id"]
              guild = await client.fetch_guild(guild_id)
              player1 = await guild.fetch_member(games[game]["player1_id"])
              player2 = await guild.fetch_member(games[game]["player2_id"])
              player1.send(f"It's a **DRAW!** You both scored `{games[game]['player1_score']}`.")
              player2.send(f"It's a **DRAW!** You both scored `{games[game]['player1_score']}`.")
          break

              
        elif games[game]["player2_id"] == author:
          with open('blackjack.json', 'r') as f:
            games = json.load(f)
          games[game]["player2_status"] = "standing"
          if games[game]["player1_status"] == "standing":
            if games[game]["player2_score"] > games[game]["player1_score"]:
              guild_id = games[game]["guild_id"]
              guild = await client.fetch_guild(guild_id)
              player2 = await guild.fetch_member(games[game]["player2_id"])
              player1 = await guild.fetch_member(games[game]["player1_id"])
              await player2.send(f"You **WON!** Your final score is `{games[game]['player2_score']}`, and your opponent's is `{games[game]['player1_score']}`.")
              await player1.send(f"You **LOST!** Your final score is `{games[game]['player1_score']}`, and your opponent's is `{games[game]['player2_score']}`.")
              
            elif games[game]["player1_score"] > games[game]["player2_score"]:
              guild_id = games[game]["guild_id"]
              guild = await client.fetch_guild(guild_id)
              player2 = await guild.fetch_member(games[game]["player2_id"])
              player1 = await guild.fetch_member(games[game]["player1_id"])
              await player1.send(f"You **WON!** Your final score is `{games[game]['player1_score']}`, and your opponent's is `{games[game]['player2_score']}`.")
              await player2.send(f"You **LOST!** Your final score is `{games[game]['player2_score']}`, and your opponent's is `{games[game]['player1_score']}`.")

            else:
              guild_id = games[game]["guild_id"]
              guild = await client.fetch_guild(guild_id)
              player1 = await guild.fetch_member(games[game]["player1_id"])
              player2 = await guild.fetch_member(games[game]["player2_id"])
              player1.send(f"It's a **DRAW!** You both scored `{games[game]['player1_score']}`.")
              player2.send(f"It's a **DRAW!** You both scored `{games[game]['player1_score']}`.")
          break

            
      # writing all changes
      with open('blackjack.json', 'w') as f:
        json.dump(games, f)