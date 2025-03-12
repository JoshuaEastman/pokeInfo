import os
import random
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help='Responds with Pong!')
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command(name='roll', help='Roll a d20')
    async def roll(self, ctx):
        await ctx.send(f'You rolled a {random.randint(1, 20)}')

async def setup(bot):
    await bot.add_cog(General(bot))