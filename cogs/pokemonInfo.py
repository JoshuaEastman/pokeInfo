import os
import discord
import logging
from discord.ext import commands
from utils.pokemonInfoUtil import get_pokemon_data, merge_sprites, match_api_naming
from utils.envCheck import load_env
from views.pokemonInfoViews import InfoView

logger = logging.getLogger(__name__)

class PokemonInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if load_env():
            self.channel_id = int(os.getenv('CMDS_CHANNEL_ID'))
        else:
            clean_channel_value = os.environ['CMDS_CHANNEL_ID'].strip('"')
            self.channel_id = int(clean_channel_value)

    @commands.command(name="pokeinfo", help="Get Pokémon info and stats with toggle buttons. Example: ~pokeinfo pikachu")
    async def pokeinfo(self, ctx, *, pokemon_name):
        if ctx.channel.id != self.channel_id:
            return

        # Normalize Pokémon name for API
        pokemon_api_name = match_api_naming(pokemon_name)
        pokemon = await get_pokemon_data(pokemon_api_name)

        if not pokemon:
            await ctx.send(f"Pokemon '{pokemon_name}' not found.")
            return

        # Merge front/back sprites if available
        merged_image = await merge_sprites(pokemon["id"])
        file = discord.File(merged_image, filename="sprite.png") if merged_image else None

        view = InfoView(pokemon, file=file, user_id=ctx.author.id)
        embed = view.embed

        await ctx.send(embed=embed, file=file, view=view, delete_after=(60 * 5))  # Auto delete after 5 min

async def setup(bot):
    await bot.add_cog(PokemonInfo(bot))
    logger.info("PokemonInfo cog loaded")
