import os
import discord
from discord.ext import commands
from utils.pokemonInfoUtil import get_pokemon_data, merge_sprites, match_api_naming
from utils.envCheck import load_env

class PokemonInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if load_env():
            if os.getenv('BOT_ENV') == 'production':
                self.channel_id = int(os.getenv('CMDS_CHANNEL_ID'))
            else:
                self.channel_id = int(os.getenv('PERSONAL_CHANNEL_ID'))
        else:
            if os.getenv('BOT_ENV') == 'production':
                self.channel_id = int(os.environ.get('CMDS_CHANNEL_ID'))

    # Command to get abilities of a Pokémon 
    @commands.command(name="pokeinfo", help=" - Enter ~pokeinfo and name a pokemon to get a brief description of that pokemon. Example: ~pokeinfo pikachu")
    @commands.has_permissions(manage_messages=True)
    async def pokeinfo(self, ctx, *, pokemon_name):
        if ctx.channel.id == self.channel_id:
            channel = self.bot.get_channel(self.channel_id)

            # Match the Pokémon name to the API naming convention
            pokemon_api_name = match_api_naming(pokemon_name)

            # Fetch and display information about a Pokemon
            pokemon = await get_pokemon_data(pokemon_api_name)
            if not pokemon:
                await ctx.send(f"Pokemon '{pokemon_name}' not found.")
                return

            # Create url from base_id
            database_url = f"https://pokemondb.net/pokedex/{pokemon['base_id']}"

            # Merge sprites
            merged_image = await merge_sprites(pokemon["id"])
            if merged_image != None:
                file = discord.File(merged_image, filename="sprite.png")
            else:
                file = None

            # Create a discord embed
            embed = discord.Embed(
                title=f"#{pokemon['id']} - {pokemon['name']}",
                url=database_url,
                color=discord.Color.blue(),
            )
            embed.add_field(name="Generation", value=f"Gen {pokemon['generation']}", inline=True)
            embed.add_field(name="Types", value=", ".join(pokemon["types"]), inline=True)
            embed.add_field(name="Height", value=f"{pokemon['height']} m", inline=True)
            embed.add_field(name="Weight", value=f"{pokemon['weight']} kg", inline=True)
            
            # Add regular abilities
            embed.add_field(name="Abilities", value=", ".join(pokemon["abilities"]), inline=True)

            # Add hidden abilities
            if pokemon["hidden_abilities"]:
                embed.add_field(name="Hidden Abilities", value=", ".join(pokemon["hidden_abilities"]), inline=True)

            # Display Pokémon Varieties
            if pokemon["varieties"]:
                varieties_display = ", ".join(pokemon["varieties"])
                embed.add_field(name="Varieties", value=varieties_display, inline=False)

            # Only show first 10 moves
            moves_preview = ", ".join(pokemon["moves"][:10]) + "..."
            embed.add_field(name="Moves (Sample)", value=moves_preview, inline=False)

            # Pokemon sprite
            if file != None:
                embed.set_image(url="attachment://sprite.png")

            # Serebii URL
            embed.add_field(name="More Info", value=f"[Pokemon Database]({database_url})", inline=False)

            await channel.send(embed=embed, file=file, delete_after=(60*5)) # Delete message after 5 minutes
            await channel.send("This message will self-destruct in 5 minutes.", delete_after=(60*5))
            await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(PokemonInfo(bot))
    print("PokemonInfo cog is loaded")