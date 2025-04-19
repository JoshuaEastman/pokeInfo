import random
import logging
from discord.ext import commands

logger = logging.getLogger(__name__)

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help='Responds with Pong!')
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command(name='roll', help='Roll a d20')
    async def roll(self, ctx):
        await ctx.send(f'You rolled a {random.randint(1, 20)}')

    @commands.command(name='coinflip', help='Flip a coin')
    async def coinflip(self, ctx):
        coin = random.choice(['Heads', 'Tails'])
        await ctx.send(f'{coin}!')

async def setup(bot):
    await bot.add_cog(General(bot))
    logger.info("General cog loaded")