import os
import requests
from discord.ext import commands

class Pokemon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(os.getenv('DEV_CHANNEL_ID'))

    # Command to get abilities of a Pokémon
    # Returns name of pokemon and shows standard and hidden abilities   
    @commands.command(name="ability", help="Enter !ability and name a pokemon to get available abilities. Example: !ability pikachu")
    async def pokemon(self, ctx, arg):
        CHANNEL = os.getenv('DEV_CHANNEL_ID')
        # Command only allowed in specific channel
        if ctx.channel.id == self.channel_id:
            channel = self.bot.get_channel(self.channel_id)
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
            print(ctx.channel.id)

async def setup(bot):
    await bot.add_cog(Pokemon(bot))