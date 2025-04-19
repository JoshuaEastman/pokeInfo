import discord
from discord.ext import commands

class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()
        self.hidden_cogs = {"TTS"}  # Hidden cogs in help message.

    async def send_bot_help(self, mapping):
        ctx = self.context
        embed = discord.Embed(
            title="📖 Help Menu",
            description="Here are the available commands:",
            color=discord.Color.blurple()
        )

        for cog, command_list in mapping.items():
            # Skip hidden cogs
            if cog and cog.qualified_name in self.hidden_cogs:
                continue

            filtered = await self.filter_commands(command_list, sort=True)
            if not filtered:
                continue

            # Use cog name or "No Category"
            cog_name = cog.qualified_name if cog else "No Category"
            command_descriptions = []

            for command in filtered:
                command_descriptions.append(
                    f"`{ctx.clean_prefix}{command.name}` - {command.short_doc or 'No description'}"
                )

            embed.add_field(
                name=cog_name,
                value="\n".join(command_descriptions),
                inline=False
            )

        await ctx.send(embed=embed)