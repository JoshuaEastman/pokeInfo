import os
import discord
from discord.ext import commands
from utils.pokemon import get_pokemon_data

class PokemonInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(os.getenv('DEV_CHANNEL_ID'))

    # Command to get abilities of a Pokémon
    # Returns name of pokemon and shows standard and hidden abilities   
    @commands.command(name="ability", help="Enter !ability and name a pokemon to get available abilities. Example: !ability pikachu")
    async def pokemon(self, ctx, *, pokemon_name):
        if ctx.channel.id == self.channel_id:
            channel = self.bot.get_channel(self.channel_id)
            print(f"'Ability' command used in {channel.name}")

            """Fetch and display information about a Pokemon"""
            pokemon = await get_pokemon_data(pokemon_name)
            if not pokemon:
                await ctx.send(f"Pokemon '{pokemon_name}' not found.")
                return
            
            # Create a discord embed
            embed = discord.Embed(
                title=f"#{pokemon['id']} - {pokemon['name']}",
                color=discord.Color.blue(),
            )
            embed.add_field(name="Types", value=", ".join(pokemon["types"]), inline=True)
            embed.add_field(name="Height", value=f"{pokemon['height']} m", inline=True)
            embed.add_field(name="Weight", value=f"{pokemon['weight']} kg", inline=True)
            embed.add_field(name="Abilities", value=", ".join(pokemon["abilities"]), inline=False)

            # Only show first 10 moves
            moves_preview = ", ".join(pokemon["moves"][:10]) + "..."
            embed.add_field(name="Moves (Sample)", value=moves_preview, inline=False)


            # Pokemon sprite
            sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon['id']}.png"
            embed.set_thumbnail(url=sprite_url)

            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(PokemonInfo(bot))