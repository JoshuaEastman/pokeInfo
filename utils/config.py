import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Dictionary class to allow dot notation access
class DotDict(dict):
    """A dictionary that allows dot notation access to its keys."""

    def __getattr__(self, item):
        if item in self:
            return self[item]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

# Create a dictionary to hold the .env variables
config = DotDict({
    "DISCORD_TOKEN": os.getenv("DISCORD_TOKEN"),
})