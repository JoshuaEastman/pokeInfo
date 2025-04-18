import os
import discord
import logging
from discord.ext import commands
from config.config import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TOKEN = config.discord_token

# Discord Bot Config
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='~', intents=intents)

# Load Cogs (command categories)
COG_FOLDER = "cogs"

async def load_cogs():
    for filename in os.listdir(COG_FOLDER):
        if filename.endswith('.py') and not filename.startswith('_'):
            await bot.load_extension(f'{COG_FOLDER}.{filename[:-3]}')

@bot.event
async def on_ready():
    # Uncomment the below line to make the bot invisible and offline
    # await bot.change_presence(status=discord.Status.invisible)
    logger.info(f'Logged in as {bot.user.name} - {bot.user.id}')

async def setup_hook():
    await load_cogs()

# Start Bot
if __name__ == "__main__":
    bot.setup_hook = setup_hook
    bot.run(TOKEN)