import discord
import random
from discord.ext import commands
from discord.ui import Button, View

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

    @commands.command(name='embed_buttons', help='Sends an embed with multiple buttons')
    async def embed_buttons(self, ctx):
        # Initial embed message with instructions
        embed = discord.Embed(
            title="Choose an Embed",
            description="Click on a button below to see a different embed.",
            color=discord.Color.green()
        )

        # Create initial view with three buttons
        view = EmbedButtonsView()

        # Send the initial embed with the buttons
        await ctx.send(embed=embed, view=view)


class EmbedButtonsView(View):
    def __init__(self):
        super().__init__()

    # Button 1: Displays Embed 1
    @discord.ui.button(label="Embed 1", style=discord.ButtonStyle.primary, custom_id="embed_1")
    async def embed_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Acknowledge the interaction
        await interaction.response.defer()

        # Create and update the message with Embed 1
        embed = discord.Embed(
            title="Embed 1",
            description="This is the first embed.",
            color=discord.Color.red()
        )
        await interaction.message.edit(embed=embed, view=self)

    # Button 2: Displays Embed 2
    @discord.ui.button(label="Embed 2", style=discord.ButtonStyle.primary, custom_id="embed_2")
    async def embed_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Acknowledge the interaction
        await interaction.response.defer()

        # Create and update the message with Embed 2
        embed = discord.Embed(
            title="Embed 2",
            description="This is the second embed.",
            color=discord.Color.blue()
        )
        await interaction.message.edit(embed=embed, view=self)

    # Button 3: Displays Embed 3
    @discord.ui.button(label="Embed 3", style=discord.ButtonStyle.primary, custom_id="embed_3")
    async def embed_3(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Acknowledge the interaction
        await interaction.response.defer()

        # Create and update the message with Embed 3
        embed = discord.Embed(
            title="Embed 3",
            description="This is the third embed.",
            color=discord.Color.green()
        )
        await interaction.message.edit(embed=embed, view=self)

async def setup(bot):
    await bot.add_cog(General(bot))
    print("General cog is loaded")