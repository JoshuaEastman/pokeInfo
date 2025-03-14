import os
import discord
from discord.ext import commands
from utils.pokemonInfoUtil import get_pokemon_data, match_api_naming, generate_stat_bar

min_max_text = "Min values are calculated with hindering nature, 0 IVs, and 0 EVs. Max values are calculated with beneficial nature, 31 IVs, and 252 EVs."

class PokemonStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if os.getenv('BOT_ENV') == 'production':
            self.channel_id = int(os.getenv('CMDS_CHANNEL_ID'))
        else:
            self.channel_id = int(os.getenv('PERSONAL_CHANNEL_ID'))

        # Command to get the base stats of a Pokemon
    @commands.command(name="pokestats", help=" - Enter ~pokestats and name of a pokemon to get the base stats for that pokemon. Example: ~pokestats pikachu.")
    @commands.has_permissions(manage_messages=True)
    async def pokestats(self, ctx, *, pokemon_name):
        if ctx.channel.id == self.channel_id:
            channel = self.bot.get_channel(self.channel_id)

            # Match the Pokémon name to the API naming convention
            pokemon_api_name = match_api_naming(pokemon_name)

            # Fetch and display information about a Pokemon
            pokemon = await get_pokemon_data(pokemon_api_name)
            if not pokemon:
                await ctx.send(f"Pokemon '{pokemon_name}' not found.")
                return

            # Create a discord embed
            embed = discord.Embed(
                title=f"#{pokemon['id']} - {pokemon['name']}",
                color=discord.Color.blue(),
            )

            # Build the inline formatted stats as a single field
            stats_text = ""
            for stat_name, stat_data in pokemon["stats"].items():
                # Format the stat row
                stats_text += (
                    f"**{stat_name.replace('-', ' ').title()}** - "
                    f"{stat_data['value']}\n"
                    f"{stat_data['bar']}\n"
                    f"**Min/Max:** {stat_data['min-100']}/{stat_data['max-100']}\n\n"
                )

            embed.add_field(name="", value=stats_text, inline=False)
            embed.add_field(name="", value=f"*{min_max_text}*", inline=False)

            embed.set_thumbnail(url=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon['id']}.png")

            await channel.send(embed=embed, delete_after=(60*5)) # Delete message after 5 minutes
            await channel.send("This message will self-destruct in 5 minutes.", delete_after=(60*5))
            await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(PokemonStats(bot))
    print("PokemonStats cog is loaded")