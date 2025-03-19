import os
import discord
from discord.ext import commands
from utils.envCheck import load_env

if load_env():
    if os.getenv('BOT_ENV') == 'production':
        TOKEN = os.getenv('DISCORD_TOKEN')
    else:
        TOKEN = os.getenv('TESTING_TOKEN')
else:
    if os.environ['BOT_ENV'] == 'production':
        TOKEN = os.environ['DISCORD_TOKEN']

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
    # Uncomment this line to make the bot invisible and offline
    # await bot.change_presence(status=discord.Status.invisible)
    print(f'{bot.user.name} has connected to Discord!')

async def setup_hook():
    await load_cogs()

# Start Bot
if __name__ == "__main__":
    bot.setup_hook = setup_hook
    bot.run(TOKEN)