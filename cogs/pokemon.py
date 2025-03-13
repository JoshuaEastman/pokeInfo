import os
import discord
from discord.ext import commands
from utils.pokemon import get_pokemon_data
from utils.pokemon import merge_sprites

# Helper function to map Pokémon names to the API naming convention
def match_api_naming(map_string):
        if map_string.lower() == "zygarde" or map_string.lower() == "zygarde-50" or map_string.lower() == "zygarde-10" or map_string.lower() == "zygarde-100":
            mapped_string = "718"
        elif map_string.lower() == "mr. mime":
            mapped_string = "mr-mime"
        elif map_string.lower() == "mime jr." or map_string.lower() == "mime jr":
            mapped_string = "mime-jr"
        else:
            trans_map = str.maketrans({"♂": "-m", "♀": "-f", "é": "e"})
            mapped_string = map_string.translate(trans_map)
        return mapped_string

class PokemonInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if os.getenv('BOT_ENV') == 'production':
            self.channel_id = int(os.getenv('CMDS_CHANNEL_ID'))
        else:
            self.channel_id = int(os.getenv('PERSONAL_CHANNEL_ID'))

    # Command to get abilities of a Pokémon
    # Returns name of pokemon and shows standard and hidden abilities   
    @commands.command(name="pokeinfo", help="Enter ~pokeinfo and name a pokemon to get a brief description of that pokemon. Example: ~pokeinfo pikachu")
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

            # Create the Serebii URL dynamically
            gen = pokemon["generation"]
            match gen:
                case "I" | "II" | "III" | "IV" | "V" | "VI":
                    serebii_url = f"https://www.serebii.net/pokedex-xy/{pokemon['id']:03d}.shtml"
                case "VII":
                    serebii_url = f"https://www.serebii.net/pokedex-sm/{pokemon['id']:03d}.shtml"
                case "VIII":
                    serebii_url = f"https://www.serebii.net/pokedex-swsh/{pokemon['id']:03d}.shtml"
                case "IX":
                    serebii_url = f"https://www.serebii.net/pokedex-sv/{pokemon['id']:03d}.shtml"
                case _:
                    serebii_url = f"https://www.serebii.net" # Default to Serebii homepage

            # Merge sprites
            merged_image = await merge_sprites(pokemon["id"])
            file = discord.File(merged_image, filename="sprite.png")

            
            # Create a discord embed
            embed = discord.Embed(
                title=f"#{pokemon['id']} - {pokemon['name']}",
                url=serebii_url,
                color=discord.Color.blue(),
            )
            embed.add_field(name="Generation", value=f"Gen {pokemon['generation']}", inline=True)
            embed.add_field(name="Types", value=", ".join(pokemon["types"]), inline=True)
            embed.add_field(name="Height", value=f"{pokemon['height']} m", inline=True)
            embed.add_field(name="Weight", value=f"{pokemon['weight']} kg", inline=True)
            
            # Add regular abilities
            embed.add_field(name="Abilities", value=", ".join(pokemon["abilities"]), inline=False)

            # Add hidden abilities
            if pokemon["hidden_abilities"]:
                embed.add_field(name="Hidden Abilities", value=", ".join(pokemon["hidden_abilities"]), inline=False)

            # Only show first 10 moves
            moves_preview = ", ".join(pokemon["moves"][:10]) + "..."
            embed.add_field(name="Moves (Sample)", value=moves_preview, inline=False)

            # Pokemon sprite
            embed.set_image(url="attachment://sprite.png")

            # Serebii URL
            embed.add_field(name="More Info", value=f"[Serebii Entry]({serebii_url})", inline=False)

            await channel.send(embed=embed, file=file)


async def setup(bot):
    await bot.add_cog(PokemonInfo(bot))