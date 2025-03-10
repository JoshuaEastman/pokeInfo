import os
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command(name='clear')
    @commands.has_role('Dev 💎') # Restrict to dev role
    async def clear(self, ctx, arg=10):
        await ctx.channel.purge(limit=arg)

async def setup(bot):
    await bot.add_cog(General(bot))