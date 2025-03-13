import os
import discord
import random
import asyncio
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

    @commands.command(name='coinflip', help='Flip a coin')
    async def coinflip(self, ctx):
        coin = random.choice(['Heads', 'Tails'])
        await ctx.send(f'{coin}!')

    # @commands.command(name='clear_channel', help='Clears the channel of messages')
    # async def clear_channel(self, ctx):
    #     await ctx.channel.purge()

    # @commands.command(name='clearuser', help='Clears messages from a specific user')
    # @commands.has_permissions(manage_messages=True)
    # async def clearuser(self, ctx, user: discord.User, limit: int=1000):
    #     allowed_user_id = os.getenv('PERSONAL_USER_ID')
    #     if ctx.author.id == int(allowed_user_id):
    #         # Avoid rate limits by processing in batches
    #         deleted = 0

    #         async for message in ctx.channel.history(limit=limit):
    #             if message.author == user:
    #                 await message.delete()
    #                 deleted += 1
    #                 # To avoid rate limits, add a small delay between deletions
    #                 await asyncio.sleep(1)

    #         await ctx.send(f"Deleted {deleted} messages from {user.mention}.", delete_after=5)
    #     else:
    #         await ctx.send("You are not authorized to use this command.")

async def setup(bot):
    await bot.add_cog(General(bot))