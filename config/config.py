import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class DotDict(dict):
    def __getattr__(self, attr):
        return self.get(attr)
    
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def check_env():
    env_path = ".env"
    # Check if .env file exists and return True
    if os.path.isfile(env_path):
        load_dotenv()
        return True

    # Return false if there is no .env file
    return False

if check_env():
    logger.info("Environment variables loaded from .env file.")
    discord_token = os.getenv("DISCORD_TOKEN")
else:
    logger.warning("Environment variables loaded from system environment.")
    discord_token = os.environ["DISCORD_TOKEN"]


config = DotDict({
    "discord_token": discord_token
})