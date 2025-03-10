import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands
import requests

# Discord Bot Config
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)
intents.message_content = True

# Load Environment Variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv('CHANNEL_ID')

# Command to get abilities of a Pokémon
# Returns name of pokemon and shows standard and hidden abilities
@bot.command(name="ability", help="Enter !ability and name a pokemon to get available abilities. Example: !ability pikachu")
async def pokemon(ctx, arg):
    # Command only allowed in specific channel
    if ctx.channel.id == int(CHANNEL):
        channel = bot.get_channel(int(CHANNEL))
        arg = arg.lower() # Ensure lowercase for API call

        # Url for request
        url = f"https://pokeapi.co/api/v2/pokemon/{arg}"

        # Request data from API
        try:
            response = requests.get(url)
            
            # Check if response is valid
            if response.status_code == 404:
                await channel.send("Pokémon not found. Maybe in a future generation?")
                return
            
            # Parse JSON
            data = response.json()

            # Init empty lists
            standard = []
            hidden = []

            # Parse Abilities and append them to respective lists
            for ability in data['abilities']:
                if ability['is_hidden'] == False:
                    standard.append(ability)
                elif ability['is_hidden'] == True:
                    hidden.append(ability)
        
            # Format ability lists
            default_abilities = ("### Standard:\n" + "\n".join([f"`{ability['ability']['name']}`" for ability in standard]))
            hidden_abilities = ("### Hidden:\n" + "\n".join([f"`{ability['ability']['name']}`" for ability in hidden]))

            # Send message
            await channel.send(f"## Abilities for {arg.capitalize()}\n\n{default_abilities}\n{hidden_abilities}")

        except:
            await channel.send("An error occurred. Please try again.") # Generic error message
    else:
        await ctx.send("This command is not allowed in this channel.") # Feedback for user

# Start Bot
bot.run(TOKEN)